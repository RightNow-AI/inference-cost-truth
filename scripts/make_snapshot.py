"""Freeze the current data files into one immutable dated snapshot.

Run:  py scripts/make_snapshot.py [YYYY-MM-DD]

Writes data/snapshots/<date>.json containing a copy of every data file, so a
citation to a snapshot date resolves to exactly the numbers that were published
on that date.

Refuses to overwrite an existing snapshot. A new verification round means a new
file. Past snapshots are never edited, because the point of a snapshot is that
someone who cited it can still see what they cited.
"""

from __future__ import annotations

import datetime as dt
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SNAPDIR = DATA / "snapshots"

FILES = [
    "providers.json",
    "self-host.json",
    "self-host-inputs.json",
    "models.json",
    "stack.json",
    "tokenizers.json",
    "break-even.json",
]


def main(argv: list[str]) -> int:
    date = argv[0] if argv else dt.date.today().isoformat()
    try:
        dt.date.fromisoformat(date)
    except ValueError:
        print(f"bad date: {date}, expected YYYY-MM-DD")
        return 2

    SNAPDIR.mkdir(parents=True, exist_ok=True)
    dest = SNAPDIR / f"{date}.json"
    if dest.exists():
        print(f"refusing to overwrite existing snapshot: {dest}")
        print("snapshots are immutable; use a different date")
        return 1

    payload = {
        "snapshot_date": date,
        "repo": "https://github.com/RightNow-AI/inference-cost-truth",
        "data_license": "CC-BY-4.0",
        "files": {},
    }
    missing = []
    for name in FILES:
        p = DATA / name
        if p.exists():
            payload["files"][name] = json.loads(p.read_text(encoding="utf-8"))
        else:
            missing.append(name)

    payload["files_missing_at_snapshot_time"] = missing
    dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    size_kb = dest.stat().st_size / 1024
    print(f"wrote {dest} ({size_kb:.0f} KB)")
    print(f"included: {list(payload['files'])}")
    if missing:
        print(f"missing:  {missing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
