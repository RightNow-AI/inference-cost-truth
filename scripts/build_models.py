"""Build data/models.json from the verified model-metadata lanes.

Run:  py scripts/build_models.py

Merges the models lane with the k3-glm lane. The full evidence_literal is
replaced by a truncated quote, as elsewhere.

active_params is left null wherever the official model card does not state it.
It is the field most often wrong in public comparisons because it is easy to
guess from a name and impossible to derive without the card.
"""

from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
LANES = ROOT.parent

SOURCES = [("models", None), ("k3-glm", "model_metadata")]
QUOTE_MAX = 200


def load(lane: str, key: str | None):
    p = LANES / f"ict-{lane}" / "findings.json"
    if not p.exists():
        p = LANES / f"ict-{lane}" / "models.json"
    if not p.exists():
        return []
    payload = json.loads(p.read_text(encoding="utf-8-sig"))
    if isinstance(payload, list):
        return payload
    if key and isinstance(payload.get(key), list):
        return payload[key]
    for k in ("rows", "findings", "data"):
        if isinstance(payload.get(k), list):
            return payload[k]
    return next((v for v in payload.values() if isinstance(v, list)), [])


def main() -> int:
    rows, seen = [], set()
    for lane, key in SOURCES:
        for r in load(lane, key):
            if not isinstance(r, dict):
                continue
            mid = r.get("model_id")
            if not mid or mid in seen:
                continue
            seen.add(mid)
            r = dict(r)
            lit = " ".join(str(r.pop("evidence_literal", "")).split())
            r.pop("_evidence", None)
            r["source_quote"] = lit[:QUOTE_MAX] + ("..." if len(lit) > QUOTE_MAX else "")
            r.setdefault("retrieved_on", "2026-07-31")
            r["measured"] = False
            rows.append(r)

    out = {
        "verified_on": "2026-07-31",
        "license": "CC-BY-4.0",
        "schema_note": (
            "active_params is null wherever the official card does not state "
            "it. It is never inferred from the model name."
        ),
        "rows": rows,
    }
    (DATA / "models.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8"
    )
    stated = sum(1 for r in rows if r.get("active_params"))
    print(f"models.json: {len(rows)} models, active_params stated on {stated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
