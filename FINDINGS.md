# LLM inference throughput findings

Retrieved on 2026-07-31. This lane found **9 evidence-backed datapoints: 6 COMPLETE and 3 INCOMPLETE**. It also captured **3 exact benchmark command blocks**.

No throughput was derived, rounded, multiplied, or filled from another source. Every `evidence_literal` in `findings.json` is present verbatim in its saved `evidence_file`.

## Interpretation warning

The four COMPLETE InferenceX rows report `output_tput_per_gpu`: aggregate output-token throughput normalized per GPU. They are recorded with `throughput_basis="total_output"`, but the number is **per GPU**, not the whole-system total. The two COMPLETE AMD rows report aggregate output throughput for the full 8-GPU system. These scopes must not be mixed without an explicit conversion.

## SemiAnalysis InferenceX

InferenceX is the most structurally complete source found. Its parameterized API returns hardware, GPU counts, engine image/version, precision, concurrency, ISL/OSL, and separated input/output throughput in one JSON row.

| Status | Model | Hardware | Engine | Precision | Concurrency | ISL/OSL | Output tok/s | Scope |
|---|---|---:|---|---|---:|---:|---:|---|
| COMPLETE | DeepSeek-R1-0528 | 4x B200 | SGLang v0.5.12.post1 | FP4 | 32 | 8192/1024 | 371.921627327941 | per GPU, aggregate output |
| COMPLETE | DeepSeek-R1-0528 | 4x MI355X | SGLang v0.5.12-rocm700-mi35x | FP4 | 64 | 8192/1024 | 405.8931737264108 | per GPU, aggregate output |
| COMPLETE | MiniMax-M3 | 4x B300 | vLLM nightly `4080263...` | FP4 | 512 | 8192/1024 | 1570.0039806655666 | per GPU, aggregate output |
| COMPLETE | MiniMax-M3 | 4x MI355X | vLLM ROCm nightly `6971582...` | FP4 | 512 | 8192/1024 | 954.3380192035655 | per GPU, aggregate output |
| INCOMPLETE | Llama-3.3-70B-Instruct-FP8 bucket | 2x H200 | `trt`, version absent | FP8 | 128 | 8192/1024 | 560.7088249392447 | per GPU, aggregate output |
| INCOMPLETE | Llama-3.3-70B-Instruct-FP8 bucket | 1x MI355X | vLLM, version absent | FP4 | 64 | 8192/1024 | 970.6165773336551 | per GPU, aggregate output |

The two Llama rows are retained to represent dense-transformer coverage, but both have `image=null`; their missing field is exactly `inference engine version`. Meta's official Llama 3.3 model card was also saved and describes the 70B optimized transformer architecture. The attempted Hugging Face copies were access-gated, so the public Meta GitHub model card is the usable first-party architecture source.

## AMD ROCm

AMD's Kimi-K2.5 MXFP4 post produced the strongest vendor-published COMPLETE rows. The same source gives the exact 8x MI355X hardware, ATOM container digest, MXFP4 model format, FP8 KV cache, concurrency, fixed sequence lengths, and aggregate output throughput.

| Status | Model | Hardware | Engine build | Concurrency | ISL/OSL | Aggregate output tok/s |
|---|---|---:|---|---:|---:|---:|
| COMPLETE | amd/Kimi-K2.5-MXFP4 | 8x MI355X | ATOM/AITER container digest `eba8c908...` | 2 | 10240/512 | 165.30 |
| COMPLETE | amd/Kimi-K2.5-MXFP4 | 8x MI355X | same exact digest | 40 | 10240/512 | 1,055.95 |

AMD explicitly describes these as end-to-end serving measurements, including scheduler, attention, MoE, sampling, KV-cache, and framework overhead. Two exact `atom.benchmarks.benchmark_serving` invocations are preserved in `benchmark_commands`.

## NVIDIA TensorRT-LLM

One high-value row is retained as INCOMPLETE:

| Status | Model | Hardware | Engine | Precision | Concurrency | ISL/OSL | Total output tok/s | Missing |
|---|---|---|---|---|---:|---:|---:|---|
| INCOMPLETE | nvidia/DeepSeek-R1-FP4 | B200, count not stated | TensorRT-LLM commit `b626186...` | NVFP4 weights, FP16 KV cache | 3072 | 1024/2048 | 36384.0838 | GPU count |

The source command uses `--tp 8`, but this lane does not equate tensor-parallel size with GPU count unless the source explicitly says so. The full dataset-generation, config, and `trtllm-bench` command block is captured verbatim.

## Benchmark commands

`findings.json` contains:

1. AMD ATOM benchmark, concurrency 2, random 10240/512 workload.
2. AMD ATOM benchmark, concurrency 40, random 10240/512 workload.
3. NVIDIA TensorRT-LLM dataset preparation, config heredoc, and throughput benchmark for 1024/2048.

All three decoded command strings were checked as exact substrings of the saved raw Markdown sources.

## Dense and mixture-of-experts coverage

- Mixture-of-experts coverage has COMPLETE rows on both NVIDIA and AMD accelerators through DeepSeek-R1, MiniMax-M3, and Kimi-K2.5 sources.
- Dense-transformer coverage is represented by the two Llama 3.3 70B rows, but both remain INCOMPLETE because the InferenceX rows omit the engine image/version.

## SOURCES CHECKED THAT HAD NOTHING USABLE

- vLLM Blackwell InferenceMAX post: optimization narrative and plots, but no literal point in the page text with all five completeness fields.
- vLLM MI300X best-practices post: hardware, version, precision, and QPS context exist, but ShareGPT input/output lengths are variable and no single literal result point meets the rule.
- vLLM large-scale serving post: literal `2.2k tokens/s per H200` claim, but missing a bound GPU count, precision, concurrency/batch, and input/output lengths.
- vLLM benchmarking/CLI docs: runnable syntax and example outputs, but result examples do not bind a GPU model and count to the same point.
- LMSYS/SGLang GB300 and InferenceMAX posts: useful ratios and headline throughput, but not all five fields for a single literal point.
- NVIDIA TensorRT-LLM generic performance guide: example Llama throughput includes version, precision, and lengths but omits hardware.
- MLPerf Inference Datacenter static page: results are embedded through Tableau. The saved static HTML and Tableau shell did not expose a self-contained row with engine version, precision, batch/concurrency, and sequence lengths together.
- AMD MiniMax-M3 ATOMesh post: publishes ranges over a Pareto curve, not a single text datapoint tied to one concurrency and exact engine version.
- AMD Infera post: publishes relative goodput improvements and responsiveness targets, not absolute throughput rows with all five required fields.
- InferenceX experimental per-run JSON files: literal throughput exists, but the individual files omit hardware model/count and engine version.

## PAGES I COULD NOT FETCH

- `https://developer.nvidia.com/blog/tag/tensorrt-llm/` — HTTP 404; the response body was saved.
- `https://api.github.com/repos/SemiAnalysisAI/InferenceX/releases/latest` — HTTP 404; the repository has no GitHub release marked `latest` at that endpoint.
- `https://api.github.com/repos/SemiAnalysisAI/InferenceX-app/git/trees/main?recursive=1` — HTTP 404 because the default branch is `master`; the `master` tree fetched successfully with HTTP 200.
- `https://api.github.com/repos/ROCm/rocm-blogs/git/trees/develop?recursive=1` — HTTP 404 because the relevant branch is `release`; the `release` tree fetched successfully with HTTP 200.
- Meta Llama 3.3 Hugging Face raw README and config URLs — HTTP 401 access-gated. The official public Meta GitHub model card fetched with HTTP 200.
- Bare InferenceX benchmarks endpoint without `model` — HTTP 400 `Unknown model`; all parameterized model requests used for findings returned HTTP 200.

Every observed URL/status/evidence-file mapping is recorded in `evidence/FETCH-LOG.tsv`.

## THINGS I COULD NOT VERIFY

- The GPU count for NVIDIA's 36,384.0838 tok/s B200 TensorRT-LLM result. It is intentionally INCOMPLETE.
- Engine versions for the two dense Llama InferenceX rows because their source rows contain `image=null`.
- Whole-system output throughput for the InferenceX rows. The source publishes `output_tput_per_gpu`; this lane did not manufacture a system total by multiplying it.
- A fully specified MLPerf LLM row from the public static page/Tableau shell with all five required fields in one source artifact.
- Semantic release numbers for vLLM nightly images and the ATOM container. The exact immutable tag/commit/digest is recorded instead of inventing a semantic version.

