"""Generate README.md tables directly from the data files.

Run:  py scripts/build_readme.py

The README prose lives in README.template.md. Every table is generated here
from the JSON under data/, so the two cannot drift apart. That is the whole
reason this script exists: a README table retyped by hand goes stale the first
time a price changes and nobody notices.

Placeholders in the template look like {{TABLE:name}} and are replaced with the
generated markdown.
"""

from __future__ import annotations

import json
import pathlib
import re
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
LANES = ROOT.parent
VERIFIED = "2026-07-31"

# Non-text and withdrawn models are excluded from the README tables. They are
# still in providers.json; this only controls what gets rendered.
EXCLUDE = re.compile(
    r"retired|deprecated|robotics|computer use|classifier|ocr|embed|voxtral|"
    r"whisper|moderation|image|tts|stt|audio|transcribe|realtime|search|"
    r"rerank|guard|vision-only",
    re.I,
)


def load(p):
    return json.loads((DATA / p).read_text(encoding="utf-8"))


def lane(name):
    f = LANES / f"ict-{name}" / "findings.json"
    if not f.exists():
        return []
    payload = json.loads(f.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    for k in ("rows", "findings", "data"):
        if isinstance(payload.get(k), list):
            return payload[k]
    return next((v for v in payload.values() if isinstance(v, list)), [])


def num(v):
    if v is None or isinstance(v, bool):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def money(v, dash="not documented"):
    n = num(v)
    if n is None:
        return dash
    if n == int(n) and abs(n) >= 1:
        return f"${int(n)}"
    return f"${n:g}"


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def t_api_closed(prov):
    rows = [
        r for r in prov["rows"]
        if r["category"] == "A_closed_vendor_api"
        and r.get("service_tier") == "standard"
        and not r.get("long_context_tier")
        and not EXCLUDE.search(str(r.get("model_name")))
        and num(r.get("input_per_1m")) is not None
        and num(r.get("output_per_1m")) is not None
    ]
    seen, out = set(), []
    for r in sorted(rows, key=lambda r: (r["provider"], -num(r["output_per_1m"]))):
        key = (r["provider"], r["model_name"])
        if key in seen:
            continue
        seen.add(key)
        out.append([
            r["provider"],
            f"`{r['model_name']}`",
            money(r.get("input_per_1m")),
            money(r.get("cached_input_per_1m")),
            money(r.get("cache_write_per_1m")),
            money(r.get("output_per_1m")),
            money(r.get("batch_output_per_1m"), "--"),
            f"[src]({r['source_url']})",
        ])
    return table(
        ["Vendor", "Model", "Input /1M", "Cached in", "Cache write",
         "Output /1M", "Batch out", "Source"],
        out,
    )


def t_api_hosted(prov):
    rows = [
        r for r in prov["rows"]
        if r["category"] == "B_hosted_open_api"
        and num(r.get("input_per_1m")) is not None
        and num(r.get("output_per_1m")) is not None
    ]
    fams = {
        "DeepSeek-V3.2": "deepseek-v3.2",
        "DeepSeek-R1-0528": "deepseek-r1-0528",
        "Qwen3-235B-A22B-Instruct-2507": "qwen3-235b-a22b-instruct-2507",
        "Kimi-K2-Instruct": "kimi-k2-instruct",
        "gpt-oss-120b": "gpt-oss-120b",
        "Llama-3.3-70B-Instruct": "llama-3.3-70b-instruct",
        "MiniMax-M3": "minimax-m3",
        "GLM-4.7": "glm-4.7",
    }
    out = []
    for label, needle in fams.items():
        hits = [
            r for r in rows
            if needle in str(r["model_name"]).lower().replace("_", "-")
        ]
        for r in sorted(hits, key=lambda r: num(r["output_per_1m"]))[:6]:
            out.append([
                label,
                r["provider"],
                f"`{str(r['model_name'])[:44]}`",
                money(r.get("input_per_1m")),
                money(r.get("cached_input_per_1m"), "not offered"),
                money(r.get("output_per_1m")),
                r.get("quantization") or "not stated",
                f"[src]({r['source_url']})",
            ])
    return table(
        ["Model family", "Provider", "Model id", "Input /1M", "Cached in",
         "Output /1M", "Quant", "Source"],
        out,
    )


def t_tokenizers(tok):
    out = []
    for r in tok["rows"]:
        if r["measured"]:
            out.append([
                f"`{r['tokenizer']}`",
                r["kind"],
                r["english_tokens"],
                f"{r['english_tokens_per_1000_chars']:.2f}",
                r["code_tokens"],
                f"{r['code_tokens_per_1000_chars']:.2f}",
            ])
        else:
            note = str(r["notes"]).replace("not measured: ", "")
            out.append([
                f"`{r['tokenizer']}`", r["kind"], "not measured", "not measured",
                "not measured", note[:58],
            ])
    return table(
        ["Tokenizer", "Source", "English tokens", "English /1k chars",
         "Code tokens", "Code /1k chars"],
        out,
    )


def t_selfhost(sh):
    out = []
    for r in sh["rows"]:
        u = r["cost_per_1m_by_utilization"]
        out.append([
            r["model"][:30],
            f"{r['gpu_count']}x {r['gpu_model']}",
            r["gpu_provider"],
            f"${r['gpu_hourly_per_gpu']:g}",
            f"{r['throughput_tok_per_s']:,.0f}",
            "cited" if not r["throughput_measured"] else "measured",
            f"${u['10pct']:.2f}",
            f"${u['30pct']:.2f}",
            f"${u['60pct']:.2f}",
            f"${u['90pct']:.2f}",
        ])
    return table(
        ["Model", "GPUs", "Rental", "$/GPU/hr", "Tok/s total", "Throughput",
         "10% util", "30% util", "60% util", "90% util"],
        out,
    )


def t_caching(rows):
    out = []
    for r in rows:
        if r.get("topic") != "prompt_caching":
            continue
        out.append([
            r["provider"],
            str(r.get("cache_read_price_or_discount"))[:42],
            str(r.get("cache_write_surcharge"))[:34],
            str(r.get("cache_ttl"))[:38],
            str(r.get("min_cacheable_prefix_tokens"))[:30],
            str(r.get("automatic_or_explicit")),
            f"[doc]({r.get('doc_url')})" if r.get("doc_url") else "--",
        ])
    return table(
        ["Provider", "Cache read", "Cache write", "TTL", "Min prefix",
         "Mode", "Doc"],
        out,
    )


def t_batch(rows):
    out = []
    for r in rows:
        if r.get("topic") != "batch_async":
            continue
        out.append([
            r["provider"],
            str(r.get("offered")),
            str(r.get("discount_percent"))[:26],
            str(r.get("turnaround_sla"))[:34],
            str(r.get("restrictions"))[:60],
            f"[doc]({r.get('doc_url')})" if r.get("doc_url") else "--",
        ])
    return table(
        ["Provider", "Offered", "Discount", "Turnaround", "Restrictions", "Doc"],
        out,
    )


def t_reasoning(rows):
    out = []
    for r in rows:
        if r.get("topic") != "reasoning_tokens":
            continue
        out.append([
            r["provider"],
            str(r.get("billed_as_output")),
            str(r.get("visible_to_caller"))[:26],
            f"`{str(r.get('usage_field_name'))[:52]}`",
            str(r.get("effort_levels"))[:56],
            f"[doc]({r.get('doc_url')})" if r.get("doc_url") else "--",
        ])
    return table(
        ["Provider", "Billed as output", "Visible", "Usage field",
         "Effort levels", "Doc"],
        out,
    )


def t_breakeven(be, sh):
    """Break-even against a few representative APIs, not all 2208 pairs."""
    picks = [
        ("DeepSeek", "deepseek-v4-flash"),
        ("Anthropic", "Claude Sonnet 5"),
        ("OpenAI", "gpt-5.6-terra"),
        ("Google Gemini", "Gemini 3.6 Flash"),
    ]
    out = []
    for row in be["rows"]:
        if (row["api_provider"], row["api_model"]) not in picks:
            continue
        cap = row["monthly_output_capacity_by_utilization"]
        reach = row["reachable_at_utilization"]
        out.append([
            row["self_host_model"][:26],
            f"{row['gpu_count']}x {row['gpu_model']}",
            f"${row['monthly_fixed_usd']:,.0f}",
            f"{row['api_provider']} `{row['api_model']}`",
            f"${row['api_output_per_1m']:g}",
            f"{row['break_even_output_tokens_per_month'] / 1e6:,.0f}M",
            f"{cap['30pct'] / 1e6:,.0f}M",
            "yes" if reach["30pct"] else "no",
            "yes" if reach["90pct"] else "no",
        ])
    return table(
        ["Self-host model", "GPUs", "Fixed $/mo", "Compared to API",
         "API out /1M", "Break-even tokens/mo", "Capacity @30%",
         "Beats API @30%?", "Beats API @90%?"],
        out,
    )


def t_stack():
    """Runnable stack. Rendered only from verified registry data."""
    p = LANES / "ict-models" / "stack.json"
    if not p.exists():
        return (
            "_Not yet published. Every docker tag in this section has to be "
            "proven to exist against the registry API before it goes in, and "
            "that verification is still running. A pasted command that 404s is "
            "the worst possible failure for this repo._"
        )
    payload = json.loads(p.read_text(encoding="utf-8"))
    items = payload if isinstance(payload, list) else payload.get("stack", [])
    blocks = []
    for s in items:
        cmd = str(s.get("docker_run", "")).strip()
        bench = str(s.get("benchmark_command", "")).strip()
        blocks.append(
            f"### `{s.get('model_id')}`\n\n"
            f"[model card]({s.get('hf_url')}) | "
            f"{s.get('gpu_count', '?')}x {s.get('recommended_gpu')} on "
            f"[{s.get('gpu_rental_provider')}]({s.get('gpu_rental_provider_url')}) | "
            f"{s.get('inference_engine')} | {s.get('quantization')}\n\n"
            f"{s.get('recommended_gpu_reason', '')}\n\n"
            f"```bash\n{cmd}\n```\n\n"
            f"Reproduce a throughput number on it:\n\n```bash\n{bench}\n```\n\n"
            f"Image `{s.get('image')}:{s.get('tag')}` confirmed to exist at "
            f"[{s.get('registry_api_url')}]({s.get('registry_api_url')})."
        )
    return "\n\n".join(blocks)


def main() -> int:
    prov = load("providers.json")
    tok = load("tokenizers.json")
    sh = load("self-host.json")
    be = load("break-even.json")
    bm = lane("billing-mechanics")

    tables = {
        "API_CLOSED": t_api_closed(prov),
        "API_HOSTED": t_api_hosted(prov),
        "TOKENIZERS": t_tokenizers(tok),
        "SELFHOST": t_selfhost(sh),
        "CACHING": t_caching(bm),
        "BATCH": t_batch(bm),
        "REASONING": t_reasoning(bm),
        "BREAKEVEN": t_breakeven(be, sh),
        "STACK": t_stack(),
    }

    tpl = (ROOT / "README.template.md").read_text(encoding="utf-8")
    out = tpl
    for name, md in tables.items():
        token = "{{TABLE:%s}}" % name
        if token not in out:
            print(f"  WARNING: placeholder {token} not in template")
        out = out.replace(token, md)

    leftover = re.findall(r"\{\{TABLE:[A-Z_]+\}\}", out)
    if leftover:
        print(f"  WARNING: unfilled placeholders: {leftover}")

    (ROOT / "README.md").write_text(out, encoding="utf-8")
    print(f"README.md written ({len(out.splitlines())} lines)")
    for k, v in tables.items():
        print(f"  {k}: {len(v.splitlines()) - 2} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
