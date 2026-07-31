"""Measure tokens per 1000 characters for a fixed English paragraph and a fixed code file.

Run:  py scripts/measure_tokenizers.py
Writes: data/tokenizers.json

Every row is a real measurement produced by this script. Tokenizers that fail to
load are recorded with measured=false and the load error, never estimated.
"""

from __future__ import annotations

import json
import pathlib
import sys
import traceback

ROOT = pathlib.Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "tokenizer-corpus"

ENGLISH = (CORPUS / "english.txt").read_text(encoding="utf-8")
CODE = (CORPUS / "code.py").read_text(encoding="utf-8")

# HF tokenizer repos to attempt. Gated repos will fail without credentials;
# that failure is recorded, not worked around.
HF_CANDIDATES = [
    "Qwen/Qwen3-235B-A22B",
    "Qwen/Qwen2.5-72B-Instruct",
    "deepseek-ai/DeepSeek-V3",
    "deepseek-ai/DeepSeek-R1",
    "openai/gpt-oss-120b",
    "meta-llama/Llama-3.3-70B-Instruct",
    "moonshotai/Kimi-K2-Instruct",
    "zai-org/GLM-4.5",
    "google/gemma-3-27b-it",
]

TIKTOKEN_ENCODINGS = ["o200k_base", "cl100k_base"]

HF_KWARGS: dict[str, dict] = {}

# Mistral is measured with mistral-common, Mistral's own tokenizer library,
# not with transformers. Reason, verified 2026-07-31 on transformers 5.2.0:
# loading these repos through AutoTokenizer either emits "incorrect regex
# pattern ... will lead to incorrect tokenization", or silently returns a
# different count (164 tokens for the English sample via Magistral-Small-2509
# and Devstral-Small-2507, against 134 from mistral-common for the same text).
# The first-party library is treated as authoritative.
MISTRAL_REPOS = [
    "mistralai/Mistral-Small-3.1-24B-Instruct-2503",
    "mistralai/Magistral-Small-2509",
]

# Vendors that do not publish a downloadable tokenizer. Recorded explicitly so
# the normalisation table shows the gap instead of silently omitting them.
NO_PUBLIC_TOKENIZER = [
    (
        "Anthropic (Claude family)",
        "no downloadable tokenizer published; token counts are only obtainable "
        "from the authenticated /v1/messages/count_tokens endpoint",
        "https://docs.claude.com/en/docs/build-with-claude/token-counting",
    ),
    (
        "Google (Gemini family)",
        "no downloadable tokenizer published; token counts are only obtainable "
        "from the authenticated countTokens API method",
        "https://ai.google.dev/gemini-api/docs/tokens",
    ),
]


def per_1k(n_tokens: int, text: str) -> float:
    return round(n_tokens / len(text) * 1000, 2)


def record(name, kind, ok, eng_tokens=None, code_tokens=None, err=None, source=None):
    row = {
        "tokenizer": name,
        "kind": kind,
        "measured": ok,
        "source_url": source,
    }
    if ok:
        row.update(
            {
                "english_tokens": eng_tokens,
                "english_chars": len(ENGLISH),
                "english_tokens_per_1000_chars": per_1k(eng_tokens, ENGLISH),
                "code_tokens": code_tokens,
                "code_chars": len(CODE),
                "code_tokens_per_1000_chars": per_1k(code_tokens, CODE),
                "notes": None,
            }
        )
    else:
        row.update(
            {
                "english_tokens": None,
                "english_tokens_per_1000_chars": None,
                "code_tokens": None,
                "code_tokens_per_1000_chars": None,
                "notes": f"not measured: {err}",
            }
        )
    return row


def main() -> int:
    rows = []

    try:
        import tiktoken
    except Exception as exc:  # pragma: no cover
        print(f"tiktoken unavailable: {exc}", file=sys.stderr)
        tiktoken = None

    if tiktoken is not None:
        for enc_name in TIKTOKEN_ENCODINGS:
            try:
                enc = tiktoken.get_encoding(enc_name)
                rows.append(
                    record(
                        enc_name,
                        "tiktoken",
                        True,
                        len(enc.encode(ENGLISH)),
                        len(enc.encode(CODE)),
                        source="https://github.com/openai/tiktoken",
                    )
                )
                print(f"OK   tiktoken {enc_name}")
            except Exception as exc:
                rows.append(record(enc_name, "tiktoken", False, err=str(exc)[:200]))
                print(f"FAIL tiktoken {enc_name}: {exc}")

    try:
        from transformers import AutoTokenizer
    except Exception as exc:
        print(f"transformers unavailable: {exc}", file=sys.stderr)
        AutoTokenizer = None

    if AutoTokenizer is not None:
        for repo in HF_CANDIDATES:
            try:
                tok = AutoTokenizer.from_pretrained(
                    repo, trust_remote_code=False, **HF_KWARGS.get(repo, {})
                )
                rows.append(
                    record(
                        repo,
                        "huggingface",
                        True,
                        len(tok.encode(ENGLISH, add_special_tokens=False)),
                        len(tok.encode(CODE, add_special_tokens=False)),
                        source=f"https://huggingface.co/{repo}",
                    )
                )
                print(f"OK   hf {repo}")
            except Exception as exc:
                msg = str(exc).splitlines()[0][:200] if str(exc) else type(exc).__name__
                rows.append(
                    record(
                        repo,
                        "huggingface",
                        False,
                        err=msg,
                        source=f"https://huggingface.co/{repo}",
                    )
                )
                print(f"FAIL hf {repo}: {msg}")

    try:
        from mistral_common.tokens.tokenizers.mistral import MistralTokenizer

        for repo in MISTRAL_REPOS:
            try:
                tk = MistralTokenizer.from_hf_hub(repo).instruct_tokenizer.tokenizer
                row = record(
                    repo,
                    "mistral-common",
                    True,
                    len(tk.encode(ENGLISH, bos=False, eos=False)),
                    len(tk.encode(CODE, bos=False, eos=False)),
                    source=f"https://huggingface.co/{repo}",
                )
                row["notes"] = (
                    "measured with mistral-common (first-party); transformers "
                    "AutoTokenizer disagrees on these repos, see script comment"
                )
                rows.append(row)
                print(f"OK   mistral-common {repo}")
            except Exception as exc:
                msg = str(exc).splitlines()[0][:200]
                rows.append(record(repo, "mistral-common", False, err=msg))
                print(f"FAIL mistral-common {repo}: {msg}")
    except Exception as exc:
        print(f"mistral-common unavailable: {exc}", file=sys.stderr)

    for name, reason, url in NO_PUBLIC_TOKENIZER:
        rows.append(record(name, "none_published", False, err=reason, source=url))
        print(f"GAP  {name}: {reason.split(';')[0]}")

    out = {
        "corpus": {
            "english_file": "data/tokenizer-corpus/english.txt",
            "english_chars": len(ENGLISH),
            "code_file": "data/tokenizer-corpus/code.py",
            "code_chars": len(CODE),
        },
        "rows": rows,
    }
    dest = ROOT / "data" / "tokenizers.json"
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {dest}")
    print(f"measured: {sum(1 for r in rows if r['measured'])}/{len(rows)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        raise SystemExit(1)
