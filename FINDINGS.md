# Cited throughput findings — lane throughput2

Retrieved on: 2026-07-31

## Outcome

I found **23 COMPLETE throughput datapoints** and recorded **7 INCOMPLETE rows** without filling missing fields from another source.

The COMPLETE set contains:

- 14 SemiAnalysis InferenceX points: full concurrency sweeps on 2xH100, 2xH200, and 8xH100.
- 9 first-party NVIDIA TensorRT-LLM points: three single-H200 `llama_13b` operating points and six 1x/8xH200 Llama-70B operating points.

`findings.json` contains 30 rows total. Every row's `evidence_literal` was mechanically checked as an exact substring of its `evidence_file`; validation found zero missing literals.

## Throughput-basis rule applied

InferenceX's official metric-key source says: “Throughput values are tokens/sec — `_per_gpu` is per-GPU, `_tps` is total tokens/sec across the deployment.” The selected API field is exactly `output_tput_per_gpu`, so all selected InferenceX rows use `throughput_basis="per_gpu_output"`. I did not multiply these values by GPU count.

Evidence: `evidence/inferencex-app__packages__constants__src__metric-keys.ts` (HTTP 200), sourced from `https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX-app/master/packages/constants/src/metric-keys.ts`.

The NVIDIA H200 launch table labels its field `Throughput (out tok/s/GPU)`. The Falcon/Llama page labels the same field and separately states that throughput is output tokens per second per GPU. Those rows also use `per_gpu_output`.

## COMPLETE — SemiAnalysis InferenceX

All rows below are non-disaggregated. In each row, `num_prefill_gpu` and `num_decode_gpu` are equal and refer to the same deployment GPUs, so the count is not summed.

### gptoss120b — 2xH100 — vLLM v0.21.0 — FP4 — 8192/1024

| Concurrency | Output tok/s/GPU |
|---:|---:|
| 4 | 328.9741180876137 |
| 8 | 499.1324317853124 |
| 16 | 692.6718285399187 |
| 32 | 912.4854921693673 |
| 64 | 1140.9360301350728 |

Source: `https://inferencex.semianalysis.com/api/v1/benchmarks?model=gpt-oss-120b` (HTTP 200). Evidence: `evidence/inferencex-benchmarks-gpt-oss-120b.json`.

### gptoss120b — 2xH200 — vLLM v0.22.0 — FP4 — 8192/1024

| Concurrency | Output tok/s/GPU |
|---:|---:|
| 4 | 346.880164530463 |
| 8 | 215.6675872716752 |
| 16 | 726.5822025272298 |
| 32 | 618.9053526075801 |
| 64 | 1210.7420554229893 |

Source: `https://inferencex.semianalysis.com/api/v1/benchmarks?model=gpt-oss-120b` (HTTP 200). Evidence: `evidence/inferencex-benchmarks-gpt-oss-120b.json`.

The non-monotonic points at concurrency 8 and 32 are source-reported. I did not smooth, replace, or discard them.

### qwen3.5 — 8xH100 — SGLang v0.5.14-cu130 — FP8 — 8192/1024

| Concurrency | Output tok/s/GPU |
|---:|---:|
| 1 | 19.972072260238555 |
| 2 | 34.928773526682676 |
| 4 | 57.17140608744602 |
| 8 | 58.97888549866508 |

Source: `https://inferencex.semianalysis.com/api/v1/benchmarks?model=Qwen-3.5-397B-A17B` (HTTP 200). Evidence: `evidence/inferencex-benchmarks-qwen-3-5-397b-a17b.json`.

## COMPLETE — NVIDIA TensorRT-LLM

These are first-party vendor-reported rows, so `vendor_reported=true`.

### llama_13b — 1xH200 — TensorRT LLM v0.5.0 — FP8

| Batch size | Input/output | Output tok/s/GPU |
|---:|---:|---:|
| 1024 | 128/128 | 11819 |
| 128 | 128/2048 | 4750 |
| 64 | 2048/128 | 1349 |

The source explicitly describes the result as running on a single H200 GPU.

Source: `https://raw.githubusercontent.com/NVIDIA/TensorRT-LLM/main/docs/source/blogs/H200launch.md` (HTTP 200). Evidence: `evidence/nvidia-trtllm__docs__source__blogs__H200launch.md`.

### Llama-70B — H200 — TensorRT LLM v0.7a — FP8 — input length 128

| GPU count | Batch size | Output length | Output tok/s/GPU |
|---:|---:|---:|---:|
| 1 | 960 | 128 | 3803 |
| 8 | 960 | 128 | 3803 |
| 1 | 192 | 2048 | 2941 |
| 8 | 560 | 2048 | 3163 |
| 1 | 96 | 4096 | 1946 |
| 8 | 640 | 4096 | 2263 |

The source gives the six batch sizes “in order” immediately after the six table rows and explicitly defines the 1x and 8x H200 configurations.

Source: `https://raw.githubusercontent.com/NVIDIA/TensorRT-LLM/main/docs/source/blogs/Falcon180B-H200.md` (HTTP 200). Evidence: `evidence/nvidia-trtllm__docs__source__blogs__Falcon180B-H200.md`.

## INCOMPLETE rows

| Model | Hardware | Engine | Precision | Operating point | Input/output | Throughput | Missing fields |
|---|---|---|---|---|---:|---:|---|
| llama_70b | H200, count unknown | TensorRT LLM v0.5.0 | FP8 | batch 512, TP 1 | 128/128 | 3014 tok/s/GPU | `gpu_count` |
| llama_70b | H200, count unknown | TensorRT LLM v0.5.0 | FP8 | batch 512, TP 2 | 128/2048 | 1654 tok/s/GPU | `gpu_count` |
| llama_70b | H200, count unknown | TensorRT LLM v0.5.0 | FP8 | batch 64, TP 1 | 2048/128 | 341 tok/s/GPU | `gpu_count` |
| llama_70b | H200, count unknown | TensorRT LLM v0.5.0 | FP8 | batch 32, TP 1 | 2048/128 | 303 tok/s/GPU | `gpu_count` |
| GPT-J 6B | H100, count unknown | TensorRT LLM v0.5.0 | FP8 | batch 64, TP 1 | 128/128 | 10907 total output tok/s | `gpu_count` |
| GPT-J 6B | A100, count unknown | TensorRT LLM v0.5.0 | FP16 | batch 64, TP 1 | 128/128 | 3679 total output tok/s | `gpu_count` |
| deepseek-ai/DeepSeek-R1 | H200, count unknown | TensorRT LLM, version unknown | FP8 | concurrency 1024; batch 1024 | 1024/2048 | 1436.1584 tok/s/GPU | `gpu_count`, `engine_version` |

I did not convert TP degree into total GPU count. TP is a parallelism dimension, and the completeness rule requires the source to state the GPU count.

## InferenceX model enumeration

The accepted display-model keys were taken from the official application source and all 11 API endpoints were downloaded. `Fixed rows with image` means a fixed-sequence row had ISL, OSL, concurrency, throughput, and a non-null image field; it is a discovery count, not an assertion that every image tag contains a usable semantic version.

| API model key | Returned rows | Fixed rows with image | Target-GPU fixed rows with image |
|---|---:|---:|---:|
| DeepSeek-R1-0528 | 1744 | 1634 | 829 |
| DeepSeek-V4-Pro | 1034 | 797 | 384 |
| GLM-5 | 519 | 519 | 167 |
| GLM-5.2 | 40 | 0 | 0 |
| gpt-oss-120b | 502 | 442 | 255 |
| Kimi-K2.5 | 406 | 386 | 127 |
| Kimi-K3 | 16 | 0 | 0 |
| Llama-3.3-70B-Instruct-FP8 | 681 | 0 | 0 |
| MiniMax-M2.5 | 814 | 812 | 391 |
| MiniMax-M3 | 1468 | 1464 | 820 |
| Qwen-3.5-397B-A17B | 741 | 732 | 309 |

The target-GPU count includes H100, H200, B200, and B300 rows. I selected only three coherent sweeps rather than bulk-exporting hundreds of near-duplicate points.

## Benchmark commands

`findings.json` carries five exact command entries in `benchmark_commands` arrays:

- InferenceX gptoss120b H100 benchmark client command.
- InferenceX gptoss120b H200 benchmark client command.
- InferenceX qwen3.5 H100 SGLang server command.
- InferenceX qwen3.5 H100 benchmark client command.
- NVIDIA DeepSeek-R1 H200 dataset/config/benchmark command block.

Each command was mechanically checked as an exact substring of its saved source file.

## Sources checked with no COMPLETE datapoint used

- `https://inferencex.semianalysis.com/` and `https://inferencex.semianalysis.com/inference`: static HTML did not contain a directly usable complete benchmark row; the underlying API was used instead.
- `https://inferencex.semianalysis.com/api/v1/benchmarks`: HTTP 400 `Unknown model` without a model parameter.
- `https://inferencex.semianalysis.com/api/v1/models`: HTTP 404; model keys were enumerated from official source instead.
- `https://inferencex.semianalysis.com/openapi.json`: HTTP 404.
- InferenceX `Kimi-K3` and `GLM-5.2` endpoints: no fixed-sequence rows with explicit input/output lengths.
- InferenceX `Llama-3.3-70B-Instruct-FP8` endpoint: returned throughput rows, but no row had a non-null image field from which an engine version could be recovered.
- `https://nvidia.github.io/TensorRT-LLM/0.21.0/performance/perf-overview.html`: extensive throughput tables, but no batch size or concurrency per result.
- `https://nvidia.github.io/TensorRT-LLM/performance/perf-overview.html`: same completeness gap; no batch size or concurrency per result.
- `https://developer.nvidia.com/deep-learning-performance-training-inference/ai-inference`: embedded chart JSON has model, hardware key, TP, concurrency, sequence, framework, precision, and throughput, but no engine version and no explicit total GPU count.
- `blog01_Pushing_Latency_Boundaries_Optimizing_DeepSeek-R1_Performance_on_NVIDIA_B200_GPUs.md`: no pinned overall TensorRT-LLM version for the headline operating point.
- `blog03_Optimizing_DeepSeek_R1_Throughput_on_NVIDIA_Blackwell_GPUs.md`: the headline throughput discussion does not pin a complete operating point with engine version and exact batch/concurrency.
- `blog20_Tuning_CUDA_Graph_Batch_Sizes_for_Higher_Output_Throughput.md`: reports relative improvements and plots, not a literal absolute throughput table sufficient for these rows.
- Official GitHub metadata, trees, README files, model registries, schema files, tests, and fixtures were used only for enumeration, field semantics, and source discovery; they were not treated as current throughput datapoints.

## PAGES I COULD NOT FETCH

- `https://inferencex.semianalysis.com/openapi.json` — HTTP 404; saved response body in `evidence/inferencex-openapi.json`.
- `https://inferencex.semianalysis.com/api/v1/models` — HTTP 404; saved response body in `evidence/inferencex-models.json`.
- `https://api.github.com/repos/SemiAnalysisAI/InferenceX-app/git/trees/main?recursive=1` — HTTP 404 because the repository default branch is `master`; the `master` tree was subsequently fetched successfully with HTTP 200.

No request failed at the transport layer. The items above returned explicit HTTP error responses.

## THINGS I COULD NOT VERIFY

- Total GPU count for NVIDIA rows that state TP but not an explicit 1x/8x deployment count.
- TensorRT-LLM version/commit for the NVIDIA DeepSeek-R1 H200 result reporting 1436.1584 output tok/s/GPU.
- Engine versions for the NVIDIA developer-page chart feed; the feed names engine families only.
- Engine versions for the InferenceX Llama endpoint because `image` is null.
- Fixed input/output sequence lengths for InferenceX Kimi-K3 and GLM-5.2 agentic rows.
- Absolute throughput values represented only inside NVIDIA plot images when no literal textual value accompanied the image.
- Whether custom image labels without a semantic version encode a particular package release. I did not infer versions from labels such as `minimax-m3`.

## HTTP status ledger

Every URL requested with the raw shell HTTP client is listed below.

```text
200 https://inferencex.semianalysis.com/
200 https://inferencex.semianalysis.com/inference
400 https://inferencex.semianalysis.com/api/v1/benchmarks
404 https://inferencex.semianalysis.com/openapi.json
404 https://inferencex.semianalysis.com/api/v1/models
200 https://api.github.com/repos/SemiAnalysisAI/InferenceX
200 https://api.github.com/repos/SemiAnalysisAI/InferenceX/git/trees/main?recursive=1
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX/main/README.md
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX/main/MODELS.md
200 https://api.github.com/repos/SemiAnalysisAI/InferenceX-app
404 https://api.github.com/repos/SemiAnalysisAI/InferenceX-app/git/trees/main?recursive=1
200 https://api.github.com/repos/SemiAnalysisAI/InferenceX-app/git/trees/master?recursive=1
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX-app/main/README.md
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX-app/master/packages/app/src/app/api/v1/benchmarks/route.ts
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX-app/master/packages/app/src/lib/benchmark-transform.ts
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX-app/master/packages/app/src/components/inference/types.ts
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX-app/master/packages/app/src/lib/constants.ts
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX-app/master/packages/app/src/lib/data-mappings.ts
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX-app/master/packages/app/src/hooks/api/use-benchmarks.ts
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX-app/master/packages/app/cypress/fixtures/api/benchmarks.json
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX-app/master/packages/app/src/lib/benchmark-data.server.ts
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX-app/master/packages/constants/src/models.ts
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX-app/master/packages/constants/src/metric-keys.ts
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX-app/master/packages/db/src/queries/benchmarks.ts
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX-app/master/packages/db/migrations/001_initial_schema.sql
200 https://inferencex.semianalysis.com/api/v1/benchmarks?model=DeepSeek-R1-0528
200 https://inferencex.semianalysis.com/api/v1/benchmarks?model=gpt-oss-120b
200 https://inferencex.semianalysis.com/api/v1/benchmarks?model=Llama-3.3-70B-Instruct-FP8
200 https://inferencex.semianalysis.com/api/v1/benchmarks?model=Qwen-3.5-397B-A17B
200 https://inferencex.semianalysis.com/api/v1/benchmarks?model=Kimi-K2.5
200 https://inferencex.semianalysis.com/api/v1/benchmarks?model=Kimi-K3
200 https://inferencex.semianalysis.com/api/v1/benchmarks?model=MiniMax-M2.5
200 https://inferencex.semianalysis.com/api/v1/benchmarks?model=MiniMax-M3
200 https://inferencex.semianalysis.com/api/v1/benchmarks?model=GLM-5
200 https://inferencex.semianalysis.com/api/v1/benchmarks?model=GLM-5.2
200 https://inferencex.semianalysis.com/api/v1/benchmarks?model=DeepSeek-V4-Pro
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX/main/benchmarks/single_node/fixed_seq_len/deprecated/gptoss_fp4_h100.sh
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX/main/benchmarks/single_node/fixed_seq_len/deprecated/gptoss_fp4_h200.sh
200 https://raw.githubusercontent.com/SemiAnalysisAI/InferenceX/main/benchmarks/single_node/fixed_seq_len/qwen3.5_fp8_h100.sh
200 https://api.github.com/repos/NVIDIA/TensorRT-LLM
200 https://api.github.com/repos/NVIDIA/TensorRT-LLM/git/trees/main?recursive=1
200 https://raw.githubusercontent.com/NVIDIA/TensorRT-LLM/main/docs/source/blogs/H100vsA100.md
200 https://raw.githubusercontent.com/NVIDIA/TensorRT-LLM/main/docs/source/blogs/H200launch.md
200 https://raw.githubusercontent.com/NVIDIA/TensorRT-LLM/main/docs/source/blogs/Falcon180B-H200.md
200 https://raw.githubusercontent.com/NVIDIA/TensorRT-LLM/main/docs/source/blogs/Best_perf_practice_on_DeepSeek-R1_in_TensorRT-LLM.md
200 https://raw.githubusercontent.com/NVIDIA/TensorRT-LLM/main/docs/source/blogs/tech_blog/blog01_Pushing_Latency_Boundaries_Optimizing_DeepSeek-R1_Performance_on_NVIDIA_B200_GPUs.md
200 https://raw.githubusercontent.com/NVIDIA/TensorRT-LLM/main/docs/source/blogs/tech_blog/blog03_Optimizing_DeepSeek_R1_Throughput_on_NVIDIA_Blackwell_GPUs.md
200 https://raw.githubusercontent.com/NVIDIA/TensorRT-LLM/main/docs/source/blogs/tech_blog/blog20_Tuning_CUDA_Graph_Batch_Sizes_for_Higher_Output_Throughput.md
200 https://nvidia.github.io/TensorRT-LLM/0.21.0/performance/perf-overview.html
200 https://nvidia.github.io/TensorRT-LLM/performance/perf-overview.html
200 https://developer.nvidia.com/deep-learning-performance-training-inference/ai-inference
```

## Saved artifacts

- `findings.json` — 30 evidence-backed rows: 23 COMPLETE and 7 INCOMPLETE.
- `FINDINGS.md` — this report.
- `evidence/` — raw HTTP response bodies used by the rows and source checks.
- `LANE-PROGRESS.md` — append-only lane checkpoints.

No file under `data/` was edited. No Git command, commit, push, or test runner was used.
