"""Derive self-hosting cost per 1M tokens, and the break-even against API prices.

Run:  py scripts/compute_costs.py
Reads:  data/self-host-inputs.json, data/providers.json
Writes: data/self-host.json, data/break-even.json

The formula, stated once and applied everywhere:

    cost_per_1M_tokens = (gpu_hourly_rate * gpu_count)
                         / (throughput_tok_per_s * 3600 * utilization)
                         * 1_000_000

Nothing here estimates what any provider pays to serve a model. This computes
what YOU would pay to rent the hardware and run the model yourself, from a
published GPU rate and a published throughput figure, both carried with their
sources.
"""

from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# Named here rather than inline so the sensitivity table and the headline rows
# can never drift apart.
UTILIZATION_LEVELS = [0.10, 0.30, 0.60, 0.90]

# Which utilization each published range endpoint corresponds to. Utilization
# is the assumption that moves the result most, by a factor of 9 across this
# range, so it is the one the range is built from.
RANGE_MAP = {"low": 0.90, "mid": 0.30, "high": 0.10}

HOURS_PER_MONTH = 24 * 30


def cost_per_1m(hourly_cost: float, throughput: float, utilization: float) -> float:
    """USD per 1M tokens. hourly_cost is for the whole deployment."""
    if throughput <= 0 or utilization <= 0:
        raise ValueError("throughput and utilization must be positive")
    tokens_per_hour = throughput * 3600.0 * utilization
    return hourly_cost / tokens_per_hour * 1_000_000


def build_self_host(inputs: dict) -> dict:
    rows = []
    for cfg in inputs["configs"]:
        thr = cfg["throughput_tok_per_s"]
        for rate in cfg["rates"]:
            hourly = rate["hourly_per_gpu"] * cfg["gpu_count"]
            by_util = {
                f"{int(u * 100)}pct": round(cost_per_1m(hourly, thr, u), 4)
                for u in UTILIZATION_LEVELS
            }
            row = {
                "id": f"{cfg['id']}::{rate['provider']}::{rate['tier']}",
                "model": cfg["model"],
                "gpu_model": cfg["gpu_model"],
                "gpu_count": cfg["gpu_count"],
                "engine": cfg.get("engine"),
                "engine_version": cfg.get("engine_version"),
                "precision": cfg.get("precision"),
                "batch_or_concurrency": cfg.get("batch_or_concurrency"),
                "input_len": cfg.get("input_len"),
                "output_len": cfg.get("output_len"),
                "throughput_tok_per_s": thr,
                "throughput_basis": cfg.get("throughput_basis"),
                "throughput_source_url": cfg.get("throughput_source_url"),
                "throughput_measured": cfg.get("throughput_measured", False),
                "gpu_provider": rate["provider"],
                "gpu_tier": rate["tier"],
                "gpu_hourly_per_gpu": rate["hourly_per_gpu"],
                "deployment_hourly": round(hourly, 4),
                "gpu_rate_source_url": rate["source_url"],
                "retrieved_on": rate["retrieved_on"],
                "cost_per_1m_by_utilization": by_util,
                "cost_per_1m_low": round(cost_per_1m(hourly, thr, RANGE_MAP["low"]), 4),
                "cost_per_1m_mid": round(cost_per_1m(hourly, thr, RANGE_MAP["mid"]), 4),
                "cost_per_1m_high": round(cost_per_1m(hourly, thr, RANGE_MAP["high"]), 4),
                "range_driver": (
                    "utilization: low=90%, mid=30%, high=10% of theoretical "
                    "continuous throughput"
                ),
                "measured": False,
                "notes": cfg.get("notes"),
            }
            rows.append(row)
    return {
        "formula": (
            "cost_per_1M_tokens = (gpu_hourly_rate * gpu_count) / "
            "(throughput_tok_per_s * 3600 * utilization) * 1000000"
        ),
        "utilization_levels": UTILIZATION_LEVELS,
        "range_map": RANGE_MAP,
        "excluded_from_model": inputs.get("excluded_from_model", []),
        "rows": rows,
    }


def build_break_even(self_host: dict, providers: dict) -> dict:
    """Monthly output-token volume at which self-hosting beats an API price.

    Self-hosting is a fixed monthly bill regardless of volume. An API is purely
    variable. Break-even is therefore where fixed / volume == api unit price:

        break_even_tokens_per_month = monthly_fixed_cost / api_price_per_1M * 1e6

    Below that volume the API is cheaper. This is reported per utilization
    level because utilization does not change the fixed cost, only the ceiling
    on how many tokens the box can actually deliver.
    """
    def numeric(v):
        """Some vendor pages print prices as strings. Take only real numbers."""
        if isinstance(v, bool) or v is None:
            return None
        try:
            f = float(v)
        except (TypeError, ValueError):
            return None
        return f if f > 0 else None

    # Break-even is computed against the standard realtime tier only. Batch,
    # flex and fast tiers are separate products with different latency
    # contracts, and blending them into one comparison is exactly the error
    # this repo exists to avoid. Long-context tier rows are excluded for the
    # same reason: they price a different request shape.
    api_rows = []
    for r in providers.get("rows", []):
        if r.get("row_type", "serverless_per_token") != "serverless_per_token":
            continue
        if r.get("service_tier") not in (None, "standard"):
            continue
        if r.get("long_context_tier"):
            continue
        price = numeric(r.get("output_per_1m"))
        if price is None:
            continue
        api_rows.append({**r, "output_per_1m": price})
    out = []
    for sh in self_host["rows"]:
        monthly_fixed = sh["deployment_hourly"] * HOURS_PER_MONTH
        for api in api_rows:
            api_price = api["output_per_1m"]
            if api_price <= 0:
                continue
            be_tokens = monthly_fixed / api_price * 1_000_000
            capacity = {
                f"{int(u * 100)}pct": sh["throughput_tok_per_s"]
                * 3600
                * HOURS_PER_MONTH
                * u
                for u in UTILIZATION_LEVELS
            }
            out.append(
                {
                    "self_host_id": sh["id"],
                    "self_host_model": sh["model"],
                    "gpu_model": sh["gpu_model"],
                    "gpu_count": sh["gpu_count"],
                    "monthly_fixed_usd": round(monthly_fixed, 2),
                    "api_model": api["model_name"],
                    "api_provider": api["provider"],
                    "api_output_per_1m": api_price,
                    "break_even_output_tokens_per_month": round(be_tokens),
                    "monthly_output_capacity_by_utilization": {
                        k: round(v) for k, v in capacity.items()
                    },
                    "reachable_at_utilization": {
                        k: bool(v >= be_tokens) for k, v in capacity.items()
                    },
                    "note": (
                        "Below the break-even volume the API is cheaper. "
                        "'reachable' false means the box cannot physically emit "
                        "enough tokens at that utilization to ever break even "
                        "against this API price."
                    ),
                }
            )
    return {"hours_per_month": HOURS_PER_MONTH, "rows": out}


def main() -> int:
    inputs = json.loads((DATA / "self-host-inputs.json").read_text(encoding="utf-8"))
    self_host = build_self_host(inputs)
    (DATA / "self-host.json").write_text(
        json.dumps(self_host, indent=2) + "\n", encoding="utf-8"
    )
    print(f"self-host.json: {len(self_host['rows'])} rows")

    providers_path = DATA / "providers.json"
    if providers_path.exists():
        providers = json.loads(providers_path.read_text(encoding="utf-8"))
        be = build_break_even(self_host, providers)
        (DATA / "break-even.json").write_text(
            json.dumps(be, indent=2) + "\n", encoding="utf-8"
        )
        print(f"break-even.json: {len(be['rows'])} rows")
    else:
        print("providers.json missing, skipped break-even")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
