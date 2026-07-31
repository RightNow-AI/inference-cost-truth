"""Check the hand-written claims in the README against the data files.

Run:  py scripts/verify_readme_claims.py

The README tables are generated from JSON by build_readme.py, so they match the
data by construction. The prose does not. The TL;DR table, the tokenizer spread
figures, and the reasoning worked example are typed by a human and are exactly
where a stale or invented number would survive unnoticed.

Each claim below is asserted against the data files. Any mismatch is a failure.
"""

from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def find_api(prov, provider, model, tier="standard"):
    for r in prov["rows"]:
        if (
            r.get("provider") == provider
            and str(r.get("model_name")) == model
            and r.get("service_tier") == tier
            and not r.get("long_context_tier")
        ):
            return r
    return None


def find_selfhost(sh, model_startswith, gpu, provider):
    for r in sh["rows"]:
        if (
            str(r["model"]).startswith(model_startswith)
            and r["gpu_model"] == gpu
            and r["gpu_provider"] == provider
        ):
            return r
    return None


def main() -> int:
    prov = load("providers.json")
    sh = load("self-host.json")
    tok = load("tokenizers.json")
    fails, checks = [], 0

    def check(label, got, want):
        nonlocal checks
        checks += 1
        if got != want:
            fails.append(f"{label}: README says {want}, data says {got}")

    # --- TL;DR closed-vendor claims
    for provider, model, cin, cout in [
        ("OpenAI", "gpt-5.6-sol", 5.0, 30.0),
        ("Anthropic", "Claude Sonnet 5", 2.0, 10.0),
        ("DeepSeek", "deepseek-v4-flash", 0.14, 0.28),
    ]:
        r = find_api(prov, provider, model)
        if r is None:
            fails.append(f"TL;DR: {provider} {model} not found in providers.json")
            checks += 1
            continue
        check(f"TL;DR {model} input", num(r.get("input_per_1m")), cin)
        check(f"TL;DR {model} output", num(r.get("output_per_1m")), cout)

    # --- TL;DR hosted-open claims
    for provider, needle, cin, cout in [
        ("DeepInfra", "deepseek-ai/DeepSeek-V3.2", 0.26, 0.38),
        ("Novita AI", "openai/gpt-oss-120b", 0.05, 0.25),
    ]:
        hit = next(
            (
                r
                for r in prov["rows"]
                if r.get("provider") == provider
                and str(r.get("model_name")) == needle
            ),
            None,
        )
        if hit is None:
            fails.append(f"TL;DR: {provider} {needle} not found")
            checks += 1
            continue
        check(f"TL;DR {needle}@{provider} input", num(hit.get("input_per_1m")), cin)
        check(f"TL;DR {needle}@{provider} output", num(hit.get("output_per_1m")), cout)

    # --- TL;DR self-host claims (90% utilization)
    for start, gpu, provider, want in [
        ("DeepSeek-R1", "B200", "RunPod", 4.89),
        ("Llama-3.3-70B", "H200", "RunPod", 1.98),
    ]:
        r = find_selfhost(sh, start, gpu, provider)
        if r is None:
            fails.append(f"TL;DR self-host {start} {gpu} {provider} not found")
            checks += 1
            continue
        check(
            f"TL;DR self-host {start} @90%",
            round(r["cost_per_1m_by_utilization"]["90pct"], 2),
            want,
        )

    # --- tokenizer spread
    eng = [
        r["english_tokens_per_1000_chars"] for r in tok["rows"] if r["measured"]
    ]
    code = [r["code_tokens_per_1000_chars"] for r in tok["rows"] if r["measured"]]
    check("tokenizer english min", round(min(eng), 2), 179.97)
    check("tokenizer english max", round(max(eng), 2), 185.39)
    check("tokenizer code min", round(min(code), 2), 261.63)
    check("tokenizer code max", round(max(code), 2), 287.06)
    check(
        "tokenizer english spread %",
        round((max(eng) / min(eng) - 1) * 100, 1),
        3.0,
    )
    check(
        "tokenizer code spread %",
        round((max(code) / min(code) - 1) * 100, 1),
        9.7,
    )
    check("tokenizer corpus english chars", tok["corpus"]["english_chars"], 739)
    check("tokenizer corpus code chars", tok["corpus"]["code_chars"], 1376)

    # --- reasoning worked example arithmetic
    rate = num(find_api(prov, "OpenAI", "gpt-5.6-sol").get("output_per_1m"))
    check("worked example rate", rate, 30.0)
    check("worked example billed cost", round(4300 / 1e6 * rate, 3), 0.129)
    check("worked example visible cost", round(300 / 1e6 * rate, 3), 0.009)
    check("worked example ratio", round(4300 / 300, 1), 14.3)

    # --- TL;DR self-host cells now quote MI355X, re-assert them
    for start, gpu, provider, u90, u30 in [
        ("DeepSeek-R1", "MI355X", "Vultr", 1.97, 5.91),
        ("Llama-3.3-70B", "MI355X", "Vultr", 0.82, 2.47),
    ]:
        r = find_selfhost(sh, start, gpu, provider)
        if r is None:
            fails.append(f"TL;DR self-host {start} {gpu} {provider} not found")
            checks += 1
            continue
        u = r["cost_per_1m_by_utilization"]
        check(f"TL;DR {start} MI355X @90%", round(u["90pct"], 2), u90)
        check(f"TL;DR {start} MI355X @30%", round(u["30pct"], 2), u30)

    # --- the headline honesty claim, asserted like-for-like on exact model ids.
    # A fuzzy match here would pull in distills and quietly make the API look
    # ten times better than it is, so the ids are exact.
    # (hosted model id -> canonical key the self-host model must CONTAIN).
    # Never match on a family prefix: "llama" also matches llama_13b, and
    # pricing a 13B model against a 70B API price reverses the conclusion.
    HEAD = {
        "deepseek-ai/deepseek-r1-0528": "deepseek-r1-0528",
        "minimaxai/minimax-m3": "minimax-m3",
        "meta-llama/llama-3.3-70b-instruct": "llama-3.3-70b",
    }
    import re as _re

    def _key(x):
        return _re.sub(r"[^a-z0-9.]+", "-", str(x).lower())
    api_wins_at_30 = 0
    compared = 0
    for mid, shkey in HEAD.items():
        hosted = [
            num(r.get("output_per_1m"))
            for r in prov["rows"]
            if r.get("category") == "B_hosted_open_api"
            and r.get("service_tier") in (None, "standard")
            and str(r.get("model_name", "")).lower().replace("-turbo", "") == mid
            and num(r.get("output_per_1m"))
        ]
        rows = [r for r in sh["rows"] if shkey in _key(r["model"])]
        if not hosted or not rows:
            continue
        compared += 1
        best30 = min(r["cost_per_1m_by_utilization"]["30pct"] for r in rows)
        if min(hosted) < best30:
            api_wins_at_30 += 1
    checks += 1
    if compared == 0:
        fails.append("headline claim: no like-for-like pairs could be compared")
    elif api_wins_at_30 != compared:
        fails.append(
            f"headline claim: README says the API is cheaper in EVERY comparison "
            f"at 30% utilization, but that holds in only {api_wins_at_30} of "
            f"{compared} pairs"
        )

    print(f"checked {checks} claims")
    if fails:
        print(f"FAILURES ({len(fails)}):")
        for f in fails:
            print(f"  {f}")
        return 1
    print("all README prose claims match the data files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
