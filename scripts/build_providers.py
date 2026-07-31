"""Merge the verified lane findings into data/providers.json.

Run:  py scripts/build_providers.py

Reads the gated findings.json from each research lane and normalises them into
one schema. Only rows that passed verify_evidence.py belong here, so this
script does not re-verify; it assumes the gate already ran and refuses to
invent anything.

The full evidence_literal is not published. It runs to tens of kilobytes of raw
HTML per row and would bloat the file without helping a reader. A truncated
quote is kept so a human can see what the number was read from, and the raw
captures stay in the lane worktrees.
"""

from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
LANES = ROOT.parent

RETRIEVED = "2026-07-31"
QUOTE_MAX = 220


def load(lane: str, name: str = "findings.json"):
    p = LANES / f"ict-{lane}" / name
    if not p.exists():
        return []
    payload = json.loads(p.read_text(encoding="utf-8-sig"))
    if isinstance(payload, list):
        return payload
    for key in ("rows", "findings", "data"):
        if isinstance(payload.get(key), list):
            return payload[key]
    for v in payload.values():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            return v
    return []


def quote(row: dict) -> str | None:
    lit = row.get("evidence_literal")
    if not lit:
        return None
    lit = " ".join(str(lit).split())
    return lit[:QUOTE_MAX] + ("..." if len(lit) > QUOTE_MAX else "")


def tier_of(notes: str | None) -> str:
    """Read the service tier the lane recorded in its notes."""
    n = (notes or "").lower()
    if "service tier: batch" in n or "batch tier" in n:
        return "batch"
    if "service tier: flex" in n:
        return "flex"
    if "service tier: fast" in n:
        return "fast"
    if "service tier: priority" in n:
        return "priority"
    if "service tier: standard" in n:
        return "standard"
    return "standard"


def is_long_context(notes: str | None) -> bool:
    return "long context" in (notes or "").lower()


def main() -> int:
    rows = []

    for r in load("pricing-closed"):
        notes = r.get("notes")
        rows.append(
            {
                "category": "A_closed_vendor_api",
                "row_type": "serverless_per_token",
                "provider": r.get("vendor"),
                "model_name": r.get("model_name"),
                "service_tier": tier_of(notes),
                "long_context_tier": is_long_context(notes),
                "input_per_1m": r.get("input_per_1m"),
                "cached_input_per_1m": r.get("cached_input_per_1m"),
                "cache_write_per_1m": r.get("cache_write_per_1m"),
                "output_per_1m": r.get("output_per_1m"),
                "batch_input_per_1m": r.get("batch_input_per_1m"),
                "batch_output_per_1m": r.get("batch_output_per_1m"),
                "context_window": r.get("context_window"),
                "is_reasoning_model": r.get("is_reasoning_model"),
                "quantization": None,
                "measured": False,
                "source_url": r.get("source_url"),
                "retrieved_on": r.get("retrieved_on") or RETRIEVED,
                "source_quote": quote(r),
                "notes": notes,
            }
        )

    for r in load("pricing-hosted"):
        rt = r.get("row_type") or "serverless_per_token"
        if rt == "dedicated_gpu_hour":
            rows.append(
                {
                    "category": "B_hosted_open_dedicated",
                    "row_type": "dedicated_gpu_hour",
                    "provider": r.get("provider"),
                    "model_name": r.get("model_name"),
                    "gpu_type": r.get("gpu_type"),
                    "gpu_hourly_rate": r.get("gpu_hourly_rate"),
                    "rate_scope": r.get("rate_scope"),
                    "measured": False,
                    "source_url": r.get("source_url"),
                    "retrieved_on": r.get("retrieved_on") or RETRIEVED,
                    "source_quote": quote(r),
                    "notes": r.get("notes"),
                }
            )
            continue
        rows.append(
            {
                "category": "B_hosted_open_api",
                "row_type": "serverless_per_token",
                "provider": r.get("provider"),
                "model_name": r.get("model_name"),
                # Read the tier the lane recorded. Hardcoding "standard" here
                # mislabelled 11 Fireworks rows that carry Priority-tier
                # prices, because Fireworks lists Standard and Priority as two
                # columns of the same table and the lane correctly emitted one
                # row per tier.
                "service_tier": tier_of(r.get("notes")),
                "long_context_tier": False,
                "input_per_1m": r.get("input_per_1m"),
                "cached_input_per_1m": r.get("cached_input_per_1m"),
                "cache_write_per_1m": None,
                "output_per_1m": r.get("output_per_1m"),
                "batch_input_per_1m": r.get("batch_input_per_1m"),
                "batch_output_per_1m": r.get("batch_output_per_1m"),
                "context_window": r.get("context_window"),
                "is_reasoning_model": None,
                "quantization": r.get("quantization"),
                "measured": False,
                "source_url": r.get("source_url"),
                "retrieved_on": r.get("retrieved_on") or RETRIEVED,
                "source_quote": quote(r),
                "notes": r.get("notes"),
            }
        )

    gpu = []
    # The gaps lane closed the AMD Instinct hole: the first round surveyed no
    # provider that published an on-demand per-GPU MI355X rate, so every AMD
    # throughput datapoint produced no cost row.
    gap_gpu = [
        r
        for r in load("gaps")
        if str(r.get("gap", "")).startswith(("GAP_1", "GAP_2"))
        and r.get("hourly_rate_usd") is not None
    ]
    for r in list(load("gpu-rental")) + gap_gpu:
        gpu.append(
            {
                "category": "C_gpu_rental",
                "provider": r.get("provider"),
                "gpu_model": r.get("gpu_model"),
                "hourly_rate_usd": r.get("hourly_rate_usd"),
                "per_gpu_or_per_node": r.get("per_gpu_or_per_node"),
                "gpus_per_node": r.get("gpus_per_node"),
                "tier": r.get("tier"),
                "commitment": r.get("commitment"),
                "vram_gb": r.get("vram_gb"),
                "region": r.get("region"),
                "measured": False,
                "source_url": r.get("source_url"),
                "retrieved_on": r.get("retrieved_on") or RETRIEVED,
                "source_quote": quote(r),
                "notes": r.get("notes"),
            }
        )

    out = {
        "verified_on": RETRIEVED,
        "license": "CC-BY-4.0",
        "repo": "https://github.com/RightNow-AI/inference-cost-truth",
        "schema_note": (
            "Every row carries source_url, retrieved_on, measured and notes. "
            "measured is false on every pricing row because a published price "
            "is an observation of a vendor page, not a measurement. Prices are "
            "USD per 1,000,000 tokens of that model's own tokens."
        ),
        "rows": rows,
        "gpu_rental_rows": gpu,
    }
    (DATA / "providers.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8"
    )
    print(f"providers.json: {len(rows)} token-price rows, {len(gpu)} gpu rental rows")
    from collections import Counter

    print("  categories:", dict(Counter(r["category"] for r in rows)))
    print("  tiers:", dict(Counter(r.get("service_tier") for r in rows)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
