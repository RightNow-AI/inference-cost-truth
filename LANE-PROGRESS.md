# Lane progress

## 2026-07-31 initial checkpoint

- Confirmed the worktree contains only the seed README and ignore file; no prior findings to preserve.
- Created `evidence/` for unmodified raw HTTP response bodies.
- Constraints in force: primary/first-party sources only; no Git commands; no test runners; every reported number must be a literal substring of its saved response body.

## 2026-07-31 research checkpoint

- Saved raw responses from the vLLM blog/docs, LMSYS/SGLang blog, NVIDIA TensorRT-LLM docs/repository, MLCommons datacenter page and Tableau shell, SemiAnalysis InferenceX site/API/repositories, and AMD ROCm blogs/repository.
- Found complete structured InferenceX API rows: each selected row carries hardware key, non-disaggregated GPU count, framework image/version, precision, concurrency, ISL/OSL, and `output_tput_per_gpu` in one JSON object.
- Found two vendor-published COMPLETE AMD rows in the Kimi-K2.5 MXFP4 post: 8x MI355X, exact ATOM container digest, MXFP4 plus FP8 KV cache, concurrency 2 or 40, 10,240/512 tokens, and literal aggregate output throughput.
- NVIDIA DeepSeek reproduction results contain exact TensorRT-LLM commit, precision, concurrency, ISL/OSL, and throughput, but the result section does not explicitly state GPU count; those numbers cannot be COMPLETE under the lane rule.
- Dense-model InferenceX Llama rows expose all required fields except engine version (`image` is null); retain only a small NVIDIA/AMD pair as explicitly INCOMPLETE rather than filling the version elsewhere.
- InferenceX throughput values selected for reporting are `output_tput_per_gpu`: aggregate output-token throughput normalized per GPU. They will be labeled `total_output` with an explicit per-GPU scope note; no derived system-total multiplication will be reported.

## 2026-07-31 final checkpoint

- Wrote `findings.json` with 9 rows: 6 COMPLETE and 3 INCOMPLETE, plus 3 exact benchmark command blocks.
- Wrote `FINDINGS.md` with provider-grouped summaries and the mandatory unusable-source, fetch-failure, and unverifiable-item sections.
- Wrote `evidence/FETCH-LOG.tsv` with 78 observed URL/status/evidence mappings.
- Mechanically confirmed every one of the 9 `evidence_literal` strings exists in its referenced raw evidence file.
- Mechanically confirmed all 3 decoded benchmark command strings exist character-for-character in their referenced raw Markdown source.
- Confirmed JSON parses, every referenced evidence file exists, and the fetch log has no missing local evidence paths.

