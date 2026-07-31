"""Mechanically check that every reported number really appears in its own evidence file.

Run:  py scripts/verify_evidence.py <lane_dir> [<lane_dir> ...]

For each row in <lane_dir>/findings.json this checks that the row's
`evidence_literal` occurs as a substring of <lane_dir>/<evidence_file>.

A row that passes means: someone downloaded that page and this exact string was
in it. A row that fails means the number was not found in the evidence supplied
for it, and it does not get published. This is deliberately dumb and
non-negotiable. It is the only defence against a plausible-looking invented
price.

Matching is tried in three passes, strictest first:
  1. exact substring
  2. whitespace-collapsed substring (HTML wraps and indents freely)
  3. digits-and-separators only (strips currency symbols and tag noise)
Pass 3 is reported separately because it is the weakest evidence.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

WS = re.compile(r"\s+")


def collapse(s: str) -> str:
    return WS.sub(" ", s).strip()


def digits_only(s: str) -> str:
    return re.sub(r"[^0-9.]", "", s)


def load_text(path: pathlib.Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


def iter_rows(payload):
    """findings.json may be a list, or a dict of named lists, or {"rows": [...]}."""
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


def verify_lane(lane: pathlib.Path) -> dict:
    fpath = lane / "findings.json"
    if not fpath.exists():
        return {"lane": lane.name, "error": "no findings.json"}

    try:
        payload = json.loads(fpath.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return {"lane": lane.name, "error": f"unparseable findings.json: {exc}"}

    cache: dict[str, str | None] = {}
    exact = weak = failed = skipped = 0
    failures = []

    rows = list(iter_rows(payload))
    i = -1
    while i + 1 < len(rows):
        i += 1
        row = rows[i]
        if not isinstance(row, dict):
            continue
        lit = row.get("evidence_literal")
        ev = row.get("evidence_file")

        # Some lanes cite one source per FIELD rather than one per row, and
        # emit parallel lists. Expand those into individual checks so every
        # quoted string is verified rather than the row being skipped.
        if isinstance(lit, list) or isinstance(ev, list):
            lits = lit if isinstance(lit, list) else [lit] * len(ev or [])
            evs = ev if isinstance(ev, list) else [ev] * len(lits)
            for sub_lit, sub_ev in zip(lits, evs):
                if sub_lit and sub_ev:
                    rows.append(
                        {
                            "evidence_literal": sub_lit,
                            "evidence_file": sub_ev,
                            "provider": row.get("provider"),
                        }
                    )
            continue
        label = (
            row.get("model_name")
            or row.get("gpu_model")
            or row.get("model")
            or row.get("provider")
            or row.get("topic")
            or f"row[{i}]"
        )
        if not lit or not ev:
            skipped += 1
            failures.append((label, ev, "MISSING evidence_file or evidence_literal"))
            continue

        if ev not in cache:
            p = lane / ev
            if not p.exists():
                alt = lane / "evidence" / pathlib.Path(ev).name
                p = alt if alt.exists() else p
            cache[ev] = load_text(p)
        blob = cache[ev]

        if blob is None:
            failed += 1
            failures.append((label, ev, "evidence file not found or unreadable"))
            continue

        if lit in blob:
            exact += 1
        elif collapse(lit) in collapse(blob):
            exact += 1
        elif digits_only(lit) and digits_only(lit) in digits_only(blob):
            weak += 1
        else:
            failed += 1
            failures.append((label, ev, f"literal not present: {lit[:70]!r}"))

    return {
        "lane": lane.name,
        "total": len(rows),
        "exact": exact,
        "weak": weak,
        "failed": failed,
        "missing_fields": skipped,
        "failures": failures,
    }


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    worst = 0
    for arg in argv:
        res = verify_lane(pathlib.Path(arg))
        print("=" * 72)
        if "error" in res:
            print(f"{res['lane']}: {res['error']}")
            worst = 1
            continue
        print(
            f"{res['lane']}: {res['total']} rows | "
            f"exact={res['exact']} weak={res['weak']} "
            f"FAILED={res['failed']} missing_fields={res['missing_fields']}"
        )
        for label, ev, why in res["failures"]:
            print(f"   REJECT  {label}  [{ev}]  {why}")
        if res["failed"] or res["missing_fields"]:
            worst = 1
    return worst


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
