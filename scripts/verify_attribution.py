"""Third gate: check each price sits NEAR its model name in the raw page.

Run:  py scripts/verify_attribution.py <lane_dir> [<lane_dir> ...]

Gate 1 (verify_evidence) proves the quoted literal came from the saved page.
Gate 2 (verify_values) proves the number is inside that literal.

Neither catches the failure that actually matters at scale: a lane quotes a big
block of a pricing table and attaches the WRONG row's price to a model. Both
earlier gates pass, because the model name and the number are both genuinely on
the page, just not on the same line.

This gate locates the model name inside the raw evidence file and requires the
price to appear within a character window of it. On an HTML pricing table, one
table row is typically a few hundred to a couple of thousand characters, so a
correctly attributed price lands well inside the window and a price lifted from
a different row usually does not.

This is a heuristic, not a proof. It is tuned to surface rows for human review,
not to auto-approve them. Rows it cannot locate are reported as UNLOCATABLE
rather than silently passed.
"""

from __future__ import annotations

import html
import json
import pathlib
import re
import sys

WINDOW = 1500

# Fields to attribute, in priority order. Only the two that matter most are
# checked, to keep the review list actionable.
FIELDS = ["input_per_1m", "output_per_1m"]


def norm(s: str, join: str = " ") -> str:
    """Normalise page text for matching.

    `join` is what HTML tags collapse to. Both values are needed. React and
    Next.js server-render interpolated strings with `<!-- -->` separators, so a
    model id can appear in the raw HTML as `gpt-5<!-- -->.2`. Collapsing tags to
    a space turns that into `gpt-5 .2` and the name stops matching, which reads
    as a missing model when the page in fact contains it. Collapsing to the
    empty string recovers those, so callers try both.

    Tags are stripped BEFORE entity unescaping, and the order is load-bearing.
    Unescaping first turns `&lt;272K context length&gt;` into real angle
    brackets, which the tag regex then eats as if it were markup, deleting the
    model name and often a span of neighbouring text with it.
    """
    s = re.sub(r"<[^>]+>", join, s)
    s = html.unescape(s)
    s = re.sub(r"[\s_]+", " ", s)
    return s.lower()


def name_candidates(name: str) -> list[str]:
    """Search forms for a model name.

    Lanes annotate names with qualifiers the page does not contain, for example
    `gpt-5.5 (<272K context length)` or `Claude Opus 4.1 (deprecated)`. Strip
    the parenthetical and try the bare id too.
    """
    out = [name]
    bare = re.sub(r"\s*\([^)]*\)\s*", " ", name).strip()
    if bare and bare != name:
        out.append(bare)
    return [norm(c) for c in out] + [norm(c, join="") for c in out]


def price_forms(v: float) -> list[str]:
    out = set()
    for p in (0, 1, 2, 3, 4, 5, 6):
        f = f"{v:.{p}f}"
        if float(f) == v:
            out.add(f)
            if "." in f:
                out.add(f.rstrip("0").rstrip("."))
    for scaled in (v / 1000.0,):
        for p in range(0, 10):
            f = f"{scaled:.{p}f}"
            if float(f) == scaled:
                out.add(f)
    return sorted(out, key=len, reverse=True)


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

    for arg in argv:
        lane = pathlib.Path(arg)
        fp = lane / "findings.json"
        if not fp.exists():
            print(f"{lane.name}: no findings.json")
            continue
        rows = [r for r in iter_rows(json.loads(fp.read_text(encoding="utf-8"))) if isinstance(r, dict)]

        cache: dict[str, str] = {}
        ok = 0
        unlocatable = []
        far = []

        for i, row in enumerate(rows):
            name = row.get("model_name") or row.get("model") or row.get("gpu_model")
            ev = row.get("evidence_file")
            if not name or not ev:
                continue
            if ev not in cache:
                p = lane / ev
                if not p.exists():
                    p = lane / "evidence" / pathlib.Path(ev).name
                raw = p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""
                cache[ev] = (norm(raw), norm(raw, join="")) if raw else ("", "")
            spaced, tight = cache[ev]
            if not spaced:
                unlocatable.append((name, ev, "evidence file unreadable"))
                continue

            blob = None
            positions: list[int] = []
            for cand in name_candidates(name):
                for candidate_blob in (spaced, tight):
                    hits = [m.start() for m in re.finditer(re.escape(cand), candidate_blob)]
                    if hits:
                        blob, positions = candidate_blob, hits
                        break
                if positions:
                    break
            if not positions:
                unlocatable.append((name, ev, "model name not found in page"))
                continue

            checked = [f for f in FIELDS if isinstance(row.get(f), (int, float))]
            if not checked:
                continue

            near_all = False
            for pos in positions:
                seg = blob[max(0, pos - WINDOW) : pos + WINDOW]
                if all(
                    any(form in seg for form in price_forms(float(row[f])))
                    for f in checked
                ):
                    near_all = True
                    break
            if near_all:
                ok += 1
            else:
                vals = ", ".join(f"{f}={row[f]}" for f in checked)
                far.append((row.get("vendor") or row.get("provider"), name, vals, ev))

        print("=" * 72)
        print(
            f"{lane.name}: attributed={ok} | not_near_model={len(far)} | "
            f"unlocatable={len(unlocatable)} (window +/-{WINDOW} chars)"
        )
        for vendor, name, vals, ev in far[:40]:
            print(f"   REVIEW  [{vendor}] {name}: {vals}  ({ev})")
        if len(far) > 40:
            print(f"   ... and {len(far) - 40} more")
        for name, ev, why in unlocatable[:20]:
            print(f"   UNLOCATABLE  {name}: {why}  ({ev})")
        if len(unlocatable) > 20:
            print(f"   ... and {len(unlocatable) - 20} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
