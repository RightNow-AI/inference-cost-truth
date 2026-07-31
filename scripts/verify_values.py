"""Second gate: check each extracted NUMBER appears inside its own evidence_literal.

Run:  py scripts/verify_values.py <lane_dir> [<lane_dir> ...]

verify_evidence.py proves the quoted literal really came from the saved page.
That is necessary but not sufficient. If a lane quotes a 36 KB block of HTML,
"the literal is on the page" is nearly free and says nothing about whether
input_per_1m=1.25 is the right number for the model it is attached to.

This gate closes that loop: for every numeric field on a row, the value has to
appear as a string inside that row's evidence_literal. Together the two gates
give: literal is a substring of the page, AND the value is a substring of the
literal.

Rows that fail here are not automatically wrong. Unit conversions are the main
honest cause: a price printed per 1K tokens becomes a different string per 1M.
Those need a human to look, which is the point. Fabrications also land here.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

PRICE_FIELDS = [
    "input_per_1m",
    "cached_input_per_1m",
    "cache_write_per_1m",
    "output_per_1m",
    "batch_input_per_1m",
    "batch_output_per_1m",
    "hourly_rate_usd",
    "throughput_tok_per_s",
]
INT_FIELDS = ["context_window", "gpu_count", "input_len", "output_len", "vram_gb"]


def variants(v: float) -> list[str]:
    """String forms a number might legitimately take on a vendor page."""
    out = set()
    if v == int(v):
        i = int(v)
        out.update({str(i), f"{i:,}", f"{i}.0", f"{i}.00"})
        if i >= 1000:
            out.add(f"{i // 1000}K")
            out.add(f"{i // 1000}k")
        if i >= 1_000_000:
            out.add(f"{i // 1_000_000}M")
            out.add(f"{i // 1_000_000}m")
    s = repr(float(v))
    out.add(s)
    out.add(s.rstrip("0").rstrip("."))
    for p in range(0, 9):
        f = f"{v:.{p}f}"
        out.add(f)
        out.add(f.rstrip("0").rstrip(".") if "." in f else f)
    # per-1K and per-1B restatements of a per-1M price
    for scaled in (v / 1000.0, v * 1000.0):
        for p in range(0, 10):
            f = f"{scaled:.{p}f}"
            if float(f) == scaled:
                out.add(f)
                out.add(f.rstrip("0").rstrip(".") if "." in f else f)
    return [x for x in out if x and x not in {"0", "0.0"}]


def digits(s: str) -> str:
    return re.sub(r"[^0-9.]", "", s)


def check_row(row: dict) -> list[tuple[str, float, str]]:
    lit = row.get("evidence_literal") or ""
    bad = []
    for field in PRICE_FIELDS + INT_FIELDS:
        v = row.get(field)
        if v is None or isinstance(v, str) or isinstance(v, bool):
            continue
        try:
            v = float(v)
        except (TypeError, ValueError):
            continue
        if v == 0:
            continue
        if any(var in lit for var in variants(v)):
            continue
        if any(var in digits(lit) for var in variants(v) if digits(var) == var):
            continue
        bad.append((field, v, lit[:60].replace("\n", " ")))
    return bad


def iter_rows(payload):
    if isinstance(payload, list):
        yield from payload
    elif isinstance(payload, dict):
        for key in ("rows", "findings", "data"):
            if isinstance(payload.get(key), list):
                yield from payload[key]
                return
        for value in payload.values():
            if isinstance(value, list):
                yield from (v for v in value if isinstance(v, dict))


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    rc = 0
    for arg in argv:
        lane = pathlib.Path(arg)
        f = lane / "findings.json"
        if not f.exists():
            print(f"{lane.name}: no findings.json")
            rc = 1
            continue
        rows = list(iter_rows(json.loads(f.read_text(encoding="utf-8"))))
        clean = 0
        problems = []
        for i, row in enumerate(rows):
            if not isinstance(row, dict):
                continue
            bad = check_row(row)
            if bad:
                label = (
                    row.get("model_name")
                    or row.get("gpu_model")
                    or row.get("model")
                    or row.get("provider")
                    or f"row[{i}]"
                )
                problems.append((label, row.get("vendor") or row.get("provider"), bad))
            else:
                clean += 1
        print("=" * 72)
        print(f"{lane.name}: {len(rows)} rows | value_in_literal={clean} | needs_review={len(problems)}")
        for label, vendor, bad in problems[:60]:
            fields = ", ".join(f"{fn}={fv}" for fn, fv, _ in bad)
            print(f"   REVIEW  [{vendor}] {label}: {fields}")
        if len(problems) > 60:
            print(f"   ... and {len(problems) - 60} more")
        if problems:
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
