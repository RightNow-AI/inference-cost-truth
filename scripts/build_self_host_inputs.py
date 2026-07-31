"""Build data/self-host-inputs.json from the verified throughput and GPU-rate lanes.

Run:  py scripts/build_self_host_inputs.py

No number in the output is typed by hand. Throughput comes from the throughput
lane, GPU rates come from the gpu-rental lane, and both carry their source URL.

THE PER-GPU CORRECTION, which is the single most important thing this script
does: SemiAnalysis InferenceX reports `output_tput_per_gpu`, aggregate output
throughput divided by GPU count. Feeding that straight into a whole-deployment
cost formula understates cost by exactly the GPU count, a 4x error on a 4-GPU
box. Rows sourced from that field are multiplied by gpu_count here and the
correction is recorded on the row.

Configs are only emitted when a surveyed provider actually publishes an
on-demand per-GPU rate for that exact GPU. AMD MI355X throughput data exists in
the throughput lane but no surveyed provider lists an MI355X hourly rate, so
those configs are deliberately dropped rather than costed against a guessed
rate.
"""

from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
LANES = ROOT.parent

# GPU model strings in the rental data that correspond to each benchmark GPU.
GPU_MATCH = {
    "B200": re.compile(r"\bB200\b", re.I),
    "B300": re.compile(r"\bB300\b", re.I),
    "H200": re.compile(r"\bH200\b", re.I),
    "H100": re.compile(r"\bH100\b", re.I),
    "MI355X": re.compile(r"\bMI355X\b", re.I),
    "MI300X": re.compile(r"\bMI300X\b", re.I),
}

# Tier labels that mean "pay this rate now, no commitment". Providers word it
# differently. Deliberately EXCLUDED: "starting_at", which is a marketing floor
# price rather than a rate you can actually book, and every reserved or spot
# tier, which belong in their own rows.
ON_DEMAND_TIERS = {"on_demand", "pay_as_you_go", "on_demand_vm"}

EXCLUDED = [
    "engineer time to build and operate the deployment",
    "model storage and image registry costs",
    "network egress",
    "cold start time and time spent loading weights",
    "idle time outside the assumed utilization",
    "on-call and incident response",
    "redundancy or replicas for uptime",
    "load balancer and gateway costs",
    "evaluation and regression testing of the self-hosted model",
]


def load(lane: str, key_hint: str | None = None):
    p = LANES / f"ict-{lane}" / "findings.json"
    payload = json.loads(p.read_text(encoding="utf-8-sig"))
    if isinstance(payload, list):
        return payload
    if key_hint and isinstance(payload.get(key_hint), list):
        return payload[key_hint]
    for k in ("rows", "findings", "data"):
        if isinstance(payload.get(k), list):
            return payload[k]
    return []


def main() -> int:
    thr_rows = (
        list(load("throughput", "findings"))
        + list(load("throughput2", "findings"))
        + list(load("throughput3", "findings"))
    )
    # The gaps lane supplies the AMD Instinct rates the first survey missed.
    gpu_rows = list(load("gpu-rental")) + [
        r
        for r in load("gaps")
        if str(r.get("gap", "")).startswith(("GAP_1", "GAP_2"))
        and r.get("hourly_rate_usd") is not None
    ]

    rates_by_gpu: dict[str, list[dict]] = {}
    for r in gpu_rows:
        if r.get("tier") not in ON_DEMAND_TIERS or r.get("per_gpu_or_per_node") != "per_gpu":
            continue
        rate = r.get("hourly_rate_usd")
        if not isinstance(rate, (int, float)):
            continue
        for key, pat in GPU_MATCH.items():
            if pat.search(str(r.get("gpu_model", ""))):
                rates_by_gpu.setdefault(key, []).append(
                    {
                        "provider": r.get("provider"),
                        "gpu_model_as_listed": r.get("gpu_model"),
                        "hourly_per_gpu": float(rate),
                        "tier": r.get("tier"),
                        "source_url": r.get("source_url"),
                        "retrieved_on": r.get("retrieved_on") or "2026-07-31",
                    }
                )

    # keep the cheapest and dearest published rate per GPU, so the published
    # cost range reflects real provider spread rather than one vendor's number
    for key, lst in rates_by_gpu.items():
        lst.sort(key=lambda x: x["hourly_per_gpu"])
        rates_by_gpu[key] = [lst[0], lst[-1]] if len(lst) > 1 else lst

    configs = []
    dropped = []
    for r in thr_rows:
        gpu_raw = str(r.get("gpu_model") or "")
        count = r.get("gpu_count")
        thr = r.get("throughput_tok_per_s")
        if not isinstance(count, int) or not isinstance(thr, (int, float)):
            dropped.append((r.get("model"), gpu_raw, "gpu_count or throughput missing"))
            continue

        key = next((k for k, pat in GPU_MATCH.items() if pat.search(gpu_raw)), None)
        if key is None or key not in rates_by_gpu:
            dropped.append(
                (r.get("model"), gpu_raw, "no surveyed provider publishes an on-demand per-GPU rate")
            )
            continue

        # The quoted source field name WINS over the lane's basis label.
        # Order matters and was learned the hard way: the first throughput lane
        # labelled basis "total_output" on rows whose own quoted literal reads
        # `"output_tput_per_gpu":371.92`. Trusting the label re-introduces a 4x
        # understatement on every 4-GPU box. The literal is the source's actual
        # field name, so it is the stronger evidence; the label is only used
        # when the literal does not settle it.
        lit = str(r.get("evidence_literal") or "")
        basis = str(r.get("throughput_basis") or "").lower()
        if "output_tput_per_gpu" in lit:
            per_gpu_source = True
        elif basis in ("per_gpu_output", "per_gpu"):
            per_gpu_source = True
        elif basis in ("total_output", "total_output_across_deployment"):
            per_gpu_source = False
        else:
            per_gpu_source = False
        total = thr * count if per_gpu_source else thr

        configs.append(
            {
                "id": f"{r.get('model')}-{count}x{key}".replace("/", "_").replace(" ", "-"),
                "model": r.get("model"),
                "gpu_model": key,
                "gpu_model_as_benchmarked": gpu_raw,
                "gpu_count": count,
                "engine": r.get("engine"),
                "engine_version": r.get("engine_version"),
                "precision": r.get("precision"),
                "batch_or_concurrency": r.get("batch_size_or_concurrency"),
                "input_len": r.get("input_len"),
                "output_len": r.get("output_len"),
                "throughput_tok_per_s": round(total, 2),
                "throughput_basis": "total_output_across_deployment",
                "throughput_source_field": (
                    "output_tput_per_gpu multiplied by gpu_count"
                    if per_gpu_source
                    else "source reported total output throughput directly"
                ),
                "per_gpu_correction_applied": per_gpu_source,
                "throughput_source_url": r.get("source_url"),
                "throughput_measured": False,
                "throughput_status": r.get("status"),
                "throughput_missing_fields": r.get("missing_fields") or [],
                "vendor_reported": r.get("vendor_reported"),
                "rates": rates_by_gpu[key],
                "notes": r.get("notes"),
            }
        )

    out = {
        "utilization_levels": [0.10, 0.30, 0.60, 0.90],
        "excluded_from_model": EXCLUDED,
        "configs": configs,
        "dropped_for_lack_of_a_published_rate": [
            {"model": m, "gpu": g, "reason": why} for m, g, why in dropped
        ],
    }
    (DATA / "self-host-inputs.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8"
    )
    print(f"configs: {len(configs)}   dropped: {len(dropped)}")
    for c in configs:
        print(
            f"  {c['model'][:30]:30} {c['gpu_count']}x{c['gpu_model']:5} "
            f"{c['throughput_tok_per_s']:>9} tok/s  "
            f"corrected={c['per_gpu_correction_applied']}  rates={len(c['rates'])}"
        )
    for m, g, why in dropped:
        print(f"  DROPPED {str(m)[:34]:34} {g[:22]:22} {why}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
