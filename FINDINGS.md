# K3 / GLM-5.2 comparison findings

Retrieved on 2026-07-31. All reported values come from fresh first-party or official-project HTTP responses saved under `evidence/`. No third-party price aggregator was used.

## Self-hosting cost verdict

- Kimi K3: **No.** I did not find a public throughput result that clears all five required fields. Official vLLM and SGLang launch posts publish useful measurements and configurations, and InferenceX publishes Kimi records, but the captured records do not state a semantic engine version, commit, or immutable image digest alongside the result. The InferenceX image is `vllm/vllm-openai:kimi-k3`, which is model-named but unversioned. I did not promote its throughput number.
- GLM-5.2: **Yes, once a GPU hourly price is supplied.** InferenceX row `436234` is a non-disaggregated eight-GPU AMD Instinct MI325X deployment using `lmsysorg/sglang:v0.5.15.post1-rocm720-mi30x`, FP8, concurrency 1, observed mean input length `332732.44681`, observed mean output length `3082.3617`, and `metrics.output_tput_per_gpu = 4.99233`. The throughput basis is therefore `per_gpu_output`, not whole-system throughput. Evidence: `evidence/inferencex_glm_52.json`.

The GLM sequence lengths are the same record's observed means for an `agentic_traces` workload. Its fixed `isl` and `osl` fields are null; this is called out explicitly in `findings.json` rather than silently treating the run as a fixed-length synthetic benchmark.

## Hosted prices

All amounts below are USD per one million tokens in input / cached input / output order. A dash means the official source did not publish that field for the model/tier. No batch amount was emitted because none of the captured pages supplied an exact model-specific batch price literal.

### Fireworks AI

Source: `evidence/fireworks_serverless_pricing.html` (HTTP 200). The table itself states that each Standard or Priority cell is input / cached input / output.

| Model | Tier | Input | Cached | Output |
|---|---:|---:|---:|---:|
| Kimi K3 | standard | 3.00 | 0.30 | 15.00 |
| Kimi K3 | priority | 3.75 | 0.375 | 18.75 |
| Kimi K3 Fast | fast | 4.50 | 0.45 | 22.50 |
| Kimi K3 US | standard | 3.30 | 0.33 | 16.50 |
| Kimi K3 US | priority | 4.125 | 0.4125 | 20.625 |
| GLM 5.2 | standard | 1.40 | 0.14 | 4.40 |
| GLM 5.2 | priority | 1.75 | 0.18 | 5.50 |
| GLM 5.2 Fast | fast | 2.10 | 0.21 | 6.60 |

### Together AI

Sources: `evidence/together_kimi_k3.html` and `evidence/together_glm_52.html` (HTTP 200).

| Model | Tier | Input | Cached | Output | Served context | Quantization |
|---|---:|---:|---:|---:|---:|---:|
| Kimi K3 | standard | 3.00 | 0.30 | 15.00 | 1M | FP4 |
| GLM 5.2 | standard | 1.40 | 0.26 | 4.40 | 256K | FP4 |

Together's served GLM context is reported as 256K even though the official model maximum is larger; both values are preserved in their respective sections rather than reconciled by assumption.

### Baseten

Source: `evidence/baseten_pricing.html` (HTTP 200).

| Model | Tier | Input | Cached | Output |
|---|---:|---:|---:|---:|
| Kimi K3 | standard | 3.00 | 0.30 | 15.00 |
| GLM-5.2 | standard | 1.40 | 0.14 | 4.40 |
| GLM-5.2 Fast | fast | 2.10 | 0.21 | 6.60 |

### Novita AI

Source: `evidence/novita_pricing.html` (HTTP 200).

| Model | Tier | Input | Cached | Output | Context | Quantization |
|---|---:|---:|---:|---:|---:|---:|
| Kimi K3 | standard | 3.00 | 0.30 | 15.00 | 1048576 | not stated |
| GLM 5.2 | standard | 1.40 | 0.26 | 4.40 | 1048576 | fp8 |

### DeepInfra

Source: `evidence/deepinfra_glm_52_model.html` (HTTP 200). GLM-5.2 was listed; Kimi K3 was not found in the captured official pricing/catalog response.

| Model | Tier | Input | Cached | Output |
|---|---:|---:|---:|---:|
| GLM-5.2 | standard | 0.75 | 0.14 | 2.40 |
| GLM-5.2 | priority | 1.125 | 0.21 | 3.60 |
| GLM-5.2 | flex | 0.60 | 0.112 | 1.92 |

### Nebius AI Studio

Source: `evidence/nebius_models_info.json` (HTTP 200). GLM-5.2 was listed; Kimi K3 was not.

| Model | Tier | Input | Cached | Output | Context | Quantization |
|---|---:|---:|---:|---:|---:|---:|
| GLM-5.2 | standard | 1.40 | — | 4.40 | 1024K | fp4 |

The API's flavor label is `cheap`; `standard` is used in the comparison field to distinguish it from explicit priority/fast/flex rows.

### SiliconFlow

Sources: `evidence/siliconflow_kimi_k3.html` and `evidence/siliconflow_glm_52.html` (HTTP 200).

| Model | Tier | Input | Cached | Output | Context |
|---|---:|---:|---:|---:|---:|
| Kimi-K3 | standard | 3.0 | 0.3 | 15.0 | 1049K |
| GLM-5.2 | standard | 1.302 | 0.26 | 4.092 | 1049K |

### First-party model-owner APIs

Sources: `evidence/moonshot_chat_k3_pricing.md` and `evidence/zai_pricing.md` (HTTP 200).

| Model | Provider | Tier | Input | Cached | Output | Context |
|---|---|---:|---:|---:|---:|---:|
| kimi-k3 | Moonshot AI / Kimi API | standard | 3.00 | 0.30 | 15.00 | 1,048,576 tokens |
| GLM-5.2 | Z.ai API | standard | 1.40 | 0.26 | 4.40 | — |

### Named providers with no target listing found

- Groq: neither exact target name appeared in `evidence/groq_pricing.html` (HTTP 200).
- Cerebras: neither exact target name appeared in `evidence/cerebras_pricing.html` or `evidence/cerebras_public_models.html` (HTTP 200).
- DeepInfra: GLM-5.2 was present; Kimi K3 was absent from the captured pricing/catalog response.
- Nebius AI Studio: GLM-5.2 was present; Kimi K3 was absent from the captured public models API.

## Official model metadata

| Field | Kimi K3 | GLM-5.2 |
|---|---|---|
| model_id | moonshotai/Kimi-K3 | zai-org/GLM-5.2 |
| total_params | 2.8T | not stated in captured official card/docs |
| active_params | 104B | not stated in captured official card/docs |
| context_window | 1048576 | 1048576 |
| license | Kimi K3 License | MIT |
| tokenizer | TikTokenTokenizer | TokenizersBackend |
| release_date | July 27, 2026 | 2026-06-16 |
| Hugging Face | https://huggingface.co/moonshotai/Kimi-K3 | https://huggingface.co/zai-org/GLM-5.2 |

Primary metadata evidence is in `evidence/hf_kimi_k3_readme.md`, `evidence/hf_kimi_k3_tokenizer_config.json`, `evidence/hf_glm_52_config.json`, `evidence/hf_glm_52_readme.md`, and `evidence/hf_glm_52_tokenizer_config.json`. Release evidence is in `evidence/kimi_k3_official_blog.html` and `evidence/glm_52_official_blog_bundle.js`.

## Throughput search

The InferenceX client bundle in `evidence/inferencex_chunk_04.js` enumerated these visible model keys: `DeepSeek-V4-Pro`, `Kimi-K3`, `Kimi-K2.5`, `MiniMax-M3`, `DeepSeek-R1-0528`, `GLM-5`, `GLM-5.2`, `Qwen-3.5-397B-A17B`, `gpt-oss-120b`, `MiniMax-M2.5`, and `Llama-3.3-70B-Instruct-FP8`. The bundle also contains a hidden `Llama-3.1-70B-Instruct-FP8-KV` key.

Both requested keys returned HTTP 200 from the benchmark API. I also checked the official vLLM blog/index and repository tree, official SGLang/LMSYS blog/index and repository tree, AMD ROCm blog/search pages, NVIDIA technical-blog search pages, and the two model owners' release material. The most relevant saved articles are:

- `evidence/vllm_kimi_k3_day0.html`
- `evidence/vllm_kimi_k3_preview.html`
- `evidence/sglang_kimi_k3_day0.html`
- `evidence/vllm_glm_52_b300.html`
- `evidence/sglang_glm_52_optimization.html`

The official SGLang GLM article independently gives a versioned SGLang environment and a complete agentic workload description. The numeric row selected for `findings.json` is the InferenceX result because it exposes the exact field `metrics.output_tput_per_gpu`, preventing a per-GPU versus whole-deployment ambiguity.

## PAGES I COULD NOT FETCH

| URL | Observed symptom |
|---|---|
| `https://docs.vllm.ai/en/latest/search.html?q=Kimi-K3` | HTTP 404; the vLLM blog itself was fetched successfully. |
| `https://docs.vllm.ai/en/latest/search.html?q=GLM-5.2` | HTTP 404; the vLLM blog itself was fetched successfully. |
| `https://inferencex.semianalysis.com/openapi.json` | HTTP 404. |
| `https://inferencex.semianalysis.com/api/v1/models` | HTTP 404. |
| `https://inferencex.semianalysis.com/api/v1/benchmarks/models` | HTTP 404. |
| `https://inferencex.semianalysis.com/api/v1/model-names` | HTTP 404. Model keys were instead recovered from the fetched client bundle. |
| `https://api.github.com/repos/SemiAnalysisAI/InferenceX/actions/jobs/90734300666/logs` | HTTP 403; logs require authorization. |
| `https://api.github.com/repos/SemiAnalysisAI/InferenceX/actions/jobs/88114980636/logs` | HTTP 403; logs require authorization. |
| `https://api.github.com/repos/SemiAnalysisAI/InferenceX-app/git/trees/main?recursive=1` | HTTP 404. |
| `https://api.github.com/repos/ROCm/rocm-blogs/git/trees/develop?recursive=1` | HTTP 404 for the guessed tree endpoint; the official ROCm blog pages returned HTTP 200. |
| `https://inferencex.semianalysis.com/_next/static/chunks/1d7djfo3w-p8d.js` | curl receive reset; observed status `000`. Other client chunks, including the model-key bundle, returned HTTP 200. |

## THINGS I COULD NOT VERIFY

- A fully specified Kimi K3 serving throughput datapoint under the requested strict definition. The missing item is an engine release, commit, or immutable image digest stated with the measurement; no number was downgraded into the throughput array.
- GLM-5.2 total and active parameter counts from the official Hugging Face card or Z.ai docs captured in this lane. The fields are null even though non-owner provider pages publish figures.
- Exact model-specific batch input/output prices. Generic batch-discount language was not converted into amounts because the derived numbers would not appear literally in an evidence file.
- Cached-input pricing for Nebius GLM-5.2; the public API supplied input and output prices but no cached-input field.
- Context or quantization for hosted rows where the exact pricing response did not pair those fields with the model. Those fields remain null rather than being borrowed from another provider.

## Saved output

- `findings.json`: 23 hosted-price rows, 2 model-metadata rows, and 2 throughput rows. All 27 primary `evidence_literal` values were mechanically checked against their declared files. One throughput row is an explicit Kimi evidence-gap row; one is a verified GLM datapoint.
- `FINDINGS.md`: this human-readable summary.
- `evidence/`: raw response bodies and HTTP-status ledgers used for every reported value.
