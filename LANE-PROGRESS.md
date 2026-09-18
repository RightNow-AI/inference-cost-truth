# LANE throughput3 progress

## 2026-07-31 initial checkpoint

- Confirmed the requested worktree and found no root `AGENTS.md`.
- Ran no Git commands and no test runners.
- Created `evidence/` and saved raw bodies for:
  - `https://inferencex.semianalysis.com/api/v1/benchmarks` -> HTTP 400, `evidence/inferencex_benchmarks_no_param.json`, body says `{"error":"Unknown model"}`.
  - `https://inferencex.semianalysis.com/` -> HTTP 200, `evidence/inferencex_home.html`.
  - `https://inferencex.semianalysis.com/api/v1/models` -> HTTP 404, `evidence/inferencex_models_probe.json`.
- The repo has prior single-point InferenceX references useful only as model-key discovery hints. No prior row will be reported without a newly downloaded raw source.
- Next: inspect the official frontend bundles/repository to enumerate current model keys, then download full benchmark result sets.

## 2026-07-31 InferenceX discovery checkpoint

- Saved HTTP 200 raw HTML for `/inference`, `/compare`, and `/datasets` plus all 32 referenced first-party JavaScript chunks (each returned HTTP 200).
- The official frontend bundle exposes these current route-to-database model mappings: `dsr1 -> DeepSeek-R1-0528`, `gptoss120b -> gpt-oss-120b`, `llama70b -> Llama-3.3-70B-Instruct-FP8`, `qwen3.5 -> Qwen-3.5-397B-A17B`, `kimik2.5/2.6/2.7-code -> Kimi-K2.5`, `kimik3 -> Kimi-K3`, `minimaxm2.5/2.7 -> MiniMax-M2.5`, `minimaxm3 -> MiniMax-M3`, `glm5/5.1 -> GLM-5`, `glm5.2 -> GLM-5.2`, `dsv4 -> DeepSeek-V4-Pro`.
- Probing the benchmark endpoint with each route key returned HTTP 400 `Unknown model`; those raw error bodies are saved. Next request will use the exact database model strings exposed by the same official bundle.

## 2026-07-31 full-result and sweep checkpoint

- Re-fetched the benchmark endpoint with `--compressed` and the exact database model strings so the saved bodies are literal, grep-able JSON rather than gzip bytes.
- HTTP 200 full result sets saved for 11 current API model values: DeepSeek-R1-0528, gpt-oss-120b, Llama-3.3-70B-Instruct-FP8, Qwen-3.5-397B-A17B, Kimi-K2.5, Kimi-K3, MiniMax-M2.5, MiniMax-M3, GLM-5, GLM-5.2, and DeepSeek-V4-Pro.
- The official configuration bundle also mentioned `Llama-3.1-70B-Instruct-FP8-KV`, but it is not a current selectable prefix and the API returned HTTP 400 `Unknown model`; raw error body saved.
- Across the 11 successful result sets, exact-run grouping found 692 clean non-disaggregated sweeps with at least three unique concurrency points, no duplicate concurrency inside the group, and identical reported PP/DCP/PCP/KV-cache-pool configuration fields.
- Deterministic publication selection is the widest clean sweep per current model and exact hardware key, then latest date, then 1k/1k sequence as tie-breaker. This yields 50 COMPLETE sweeps and 356 evidence-backed point rows across eight models and seven hardware keys: h100, h200, b200, b300, mi300x, mi325x, mi355x.
- Every selected point has a non-null image tag, precision, engine, equal non-disaggregated GPU counts, input/output lengths, concurrency, `metrics.output_tput_per_gpu`, and `metrics.mean_intvty`.
- External official sources saved and checked: AMD ROCm blogs (three pages), LMSYS/SGLang blogs (two pages), vLLM blog index, NVIDIA TensorRT-LLM performance overview and benchmarking docs, and MLCommons results pages. Their curve plots were raster-only or their text exposed fewer than three points for a fixed configuration, so none can pass the literal-number evidence law as an additional sweep.

## 2026-07-31 final checkpoint

- Wrote `findings.json` as an object containing the model-key inventory, 50 sweep summaries, 356 point rows, and 75 URL/status checks.
- Wrote `FINDINGS.md` with all 50 retained COMPLETE sweeps, provider-by-provider outcomes, fetch failures, and unverifiable items.
- Mechanical audit passed: all 356 `evidence_literal` values occur byte-for-byte in their named evidence files; every row is COMPLETE; every throughput basis is `per_gpu_output`; every literal contains the exact `output_tput_per_gpu` and `mean_intvty` values; all 75 source-check files exist; and the Markdown contains 50 sweep rows.
- No Git commands, commits, pushes, deployments, or test runners were used.
