# Models lane findings

Retrieved on `2026-07-31`. Specifications below come from official Hugging Face cards/repos (or a linked official publisher artifact). OpenRouter's first-party models API is used only to establish that a hosted provider lists the model today.

The machine-readable truth is in:

- `models.json`: nineteen model records with per-field evidence.
- `stack.json`: exactly five self-hosting records, including verified image tags and reproducible benchmark commands.
- `findings.json`: flattened evidence ledger; every row has one `evidence_file` / `evidence_literal` pair.
- `evidence/http-status.json`: HTTP status manifest for every captured URL.

## Current hosted open-weight models, grouped by publisher/provider

### DeepSeek

| Model | Total | Active | Context | License |
|---|---:|---:|---:|---|
| `deepseek-ai/DeepSeek-V4-Flash` | 284B | 13B | 1M tokens | MIT |
| `deepseek-ai/DeepSeek-V4-Pro` | 1.6T | 49B | 1M tokens | MIT |

Both official cards state the active counts directly. No release date was stated on the captured cards.

### Qwen

| Model | Total | Active | Context | License |
|---|---:|---:|---:|---|
| `Qwen/Qwen3.6-35B-A3B` | 35B | 3B | 262,144 native | Apache-2.0 |
| `Qwen/Qwen3.5-397B-A17B` | 397B | 17B | 262,144 native | Apache-2.0 |

The card citations state April 2026 for Qwen3.6 and February 2026 for Qwen3.5.

### Meta

| Model | Total | Active | Context | License |
|---|---:|---:|---:|---|
| `meta-llama/Llama-4-Maverick-17B-128E-Instruct` | 400B | 17B | 1M tokens | Llama 4 Community License |
| `meta-llama/Llama-4-Scout-17B-16E-Instruct` | 109B | 17B | 10M tokens | Llama 4 Community License |

The cards state a model release date of April 5, 2025. The tokenizer files were gated, so tokenizer fields are null.

### Mistral AI

| Model | Total | Active | Context | License |
|---|---:|---:|---:|---|
| `mistralai/Mistral-Medium-3.5-128B` | 128B | 128B | 256k tokens | Modified MIT License |
| `mistralai/Mistral-Small-4-119B-2603` | 119B | 6.5B | 256k tokens | Apache 2.0 License |

Mistral Medium is explicitly described as dense, so active parameters equal total parameters per the mission rule.

### Z.ai / GLM

| Model | Total | Active | Context | License |
|---|---:|---:|---:|---|
| `zai-org/GLM-5.2` | null | null | 1M tokens | MIT |

The captured card and official release bundle do not state total or active parameters. The official release bundle states `2026-06-16`.

### Moonshot AI

| Model | Total | Active | Context | License |
|---|---:|---:|---:|---|
| `moonshotai/Kimi-K2-Instruct-0905` | 1T | 32B | 256K tokens | Modified MIT License |
| `moonshotai/Kimi-K2-Thinking` | 1T | 32B | 256K tokens | Modified MIT License |

The active parameter counts are copied directly from the cards. Exact release dates were not stated.

### MiniMax

| Model | Total | Active | Context | License |
|---|---:|---:|---:|---|
| `MiniMaxAI/MiniMax-M2.7` | null | null | 204800 tokens | NON-COMMERCIAL LICENSE |
| `MiniMaxAI/MiniMax-M2.5` | null | null | 196608 tokens | Modified-MIT |

Neither official card/repo states total or active parameters. The M2.5 model license states a version release date of `2026-02-13`.

### OpenAI

| Model | Total | Active | Context | License |
|---|---:|---:|---:|---|
| `openai/gpt-oss-120b` | 117B | 5.1B | 131072 tokens | Apache 2.0 |
| `openai/gpt-oss-20b` | 21B | 3.6B | 131072 tokens | Apache 2.0 |

Both cards explicitly state MXFP4 quantization of the MoE weights. Exact release dates were not stated on the cards.

### Google

| Model | Total | Active | Context | License |
|---|---:|---:|---:|---|
| `google/gemma-4-26B-A4B-it` | 25.2B | 3.8B | 256K tokens | Apache 2.0 |
| `google/gemma-4-31B-it` | 30.7B | 30.7B | 256K tokens | Apache 2.0 |

The 31B model is in the card's dense-model table, so active parameters equal total parameters per the mission rule.

### NVIDIA

| Model | Total | Active | Context | License |
|---|---:|---:|---:|---|
| `nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16` | 120B | 12B | Up to 1M tokens | NVIDIA Nemotron Open Model License |
| `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16` | 550B | 55B | Up to 1M tokens | OpenMDW License Agreement, version 1.1 |

The cards state release dates of March 11, 2026 and June 4, 2026 respectively.

## Runnable five-model stack

| Model | Recommended rental GPU | Engine / precision | Verified image |
|---|---|---|---|
| `openai/gpt-oss-20b` | 1 × Runpod L40S 48 GB | vLLM / MXFP4 | `vllm/vllm-openai:v0.26.0` |
| `openai/gpt-oss-120b` | 1 × Runpod H100 80 GB | vLLM / MXFP4 | `vllm/vllm-openai:v0.26.0` |
| `mistralai/Mistral-Small-4-119B-2603` | 2 × Runpod H100 80 GB | vLLM / FP8 | `vllm/vllm-openai:v0.26.0` |
| `Qwen/Qwen3.6-35B-A3B` | 8 × Runpod H100 80 GB | vLLM / BF16 | `vllm/vllm-openai:v0.26.0` |
| `nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16` | 8 × Runpod H100-80GB | vLLM / BF16 weights + FP8 KV cache | `vllm/vllm-openai:v0.18.1` |

The exact one-line server and benchmark commands are in `stack.json`. The benchmark command uses vLLM's official random-data serve benchmark with 1000 prompts, 1024 input tokens, and 128 output tokens. Docker Hub returned HTTP 200 for both exact tag endpoints, and the saved bodies contain the literals `"name":"v0.26.0"` and `"name":"v0.18.1"`.

## PAGES I COULD NOT FETCH

- `https://huggingface.co/api/models?pipeline_tag=text-generation&sort=trending&limit=100` — HTTP 400; the official API rejected `sort=trending`. The public trending HTML was captured successfully instead.
- `https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct/resolve/main/config.json` — HTTP 401; gated.
- `https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct/resolve/main/tokenizer_config.json` — HTTP 401; gated.
- `https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct/resolve/main/config.json` — HTTP 401; gated.
- `https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct/resolve/main/tokenizer_config.json` — HTTP 401; gated.
- `https://raw.githubusercontent.com/MiniMax-AI/MiniMax-M2.5/main/LICENSE` — HTTP 404; the repository uses `LICENSE-CODE` and `LICENSE-MODEL`.
- `https://huggingface.co/MiniMaxAI/MiniMax-M2.5/resolve/main/LICENSE` — HTTP 404; the card's generic target is absent. The official GitHub `LICENSE-MODEL` was captured successfully.
- `https://z.ai/blog/glm-5.2` — HTTP 200 but `NOT_IN_STATIC_HTML`; the page only referenced a JavaScript bundle. The official bundle was fetched and saved as `evidence/zai_glm_5_2_blog_bundle.js`.

## THINGS I COULD NOT VERIFY

- GLM-5.2 total parameters and active parameters: not stated in the official card or official release bundle.
- MiniMax-M2.7 total parameters and active parameters: not stated in the official card, config, README, or deployment guide.
- MiniMax-M2.5 total parameters and active parameters: not stated in the official card, config, README, or deployment guide.
- Meta Llama 4 tokenizer name/type: the accessible cards do not state it, and both tokenizer files returned HTTP 401.
- Exact release dates for DeepSeek V4, Mistral Medium 3.5, Mistral Small 4, both Kimi K2 records, both gpt-oss records, both Gemma 4 records, and MiniMax-M2.7: not stated in the captured official cards/repos.
- OpenRouter also listed newer hosted names including DeepSeek V4 Flash 0731, Qwen3.7, Kimi K3, and MiniMax M3. I did not promote those to open-weight inventory rows because the captured official publisher Hugging Face listings did not expose corresponding official open-weight repositories/cards.
- The five Docker commands were source-checked but not GPU-executed in this worktree. The image tags, model launch flags, provider GPU listings, and benchmark CLI flags are verified; actual throughput will vary by rental host and runtime conditions.
- The L40S recommendation for gpt-oss-20b is a capacity recommendation based on the official 16GB fit statement plus Runpod's official 48 GB listing. The Mistral and Qwen H100 choices combine each card's official GPU count/tensor-parallel command with Runpod's official H100 80 GB listing; those cards do not prescribe Runpod specifically.
