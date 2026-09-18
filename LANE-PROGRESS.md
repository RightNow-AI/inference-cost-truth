# Lane throughput2 progress

## 2026-07-31 checkpoint 1

- Read `data/self-host-inputs.json`; existing costed configurations include DeepSeek-R1-0528/B200, MiniMax-M3/B300, and an incomplete Llama-3.3-70B/H200 row.
- Confirmed the source-basis hazard: `output_tput_per_gpu` must be recorded as `per_gpu_output`, not deployment total.
- Saved raw HTTP bodies for the InferenceX home page (200), dashboard (200), bare benchmark API request (400), missing `/api/v1/models` (404), missing `/openapi.json` (404), official GitHub repository metadata/tree/README (all 200).
- The official repository tree exposes benchmark scripts and configurations. Next: enumerate actual model API keys and download complete benchmark sweeps.

## 2026-07-31 checkpoint 2

- Downloaded all 11 accepted InferenceX benchmark model endpoints as decompressed text bodies (all HTTP 200) so literals are grep-able.
- Selected three strict, non-disaggregated fixed-sequence sweeps with explicit image tags: 2xH100 gptoss120b/vLLM v0.21.0 (5 concurrency points), 2xH200 gptoss120b/vLLM v0.22.0 (5), and 8xH100 qwen3.5/SGLang v0.5.14-cu130 (4).
- Saved the official InferenceX application source defining `_per_gpu` as per-GPU tokens/sec and `_tps` as deployment-total tokens/sec.
- Saved official NVIDIA TensorRT-LLM H200 launch, Falcon/Llama H200, H100-vs-A100, DeepSeek-R1, and performance-overview pages (HTTP 200).
- Identified 9 complete first-party NVIDIA H200 points: three single-H200 llama_13b rows in TensorRT-LLM v0.5.0 and six 1x/8x H200 Llama-70B rows in TensorRT-LLM v0.7a.
- TP-only NVIDIA rows remain incomplete when the source does not explicitly state total GPU count. Current perf-overview tables also omit batch/concurrency, and the NVIDIA chart feed omits engine version.
- Saved exact benchmark scripts/commands for the selected InferenceX sweeps and NVIDIA DeepSeek-R1 reproduction commands.

## 2026-07-31 checkpoint 3

- Wrote `findings.json` with 30 rows: 23 COMPLETE and 7 INCOMPLETE.
- Wrote `FINDINGS.md` with provider-grouped tables, the mandatory fetch/verification-gap sections, model enumeration, command inventory, and a status ledger for every requested URL.
- Mechanically verified every `evidence_literal` against its saved `evidence_file`: 30/30 found.
- Mechanically verified all five collected benchmark commands against their saved source files: 5/5 found.
- Preserved per-GPU throughput semantics; no InferenceX throughput was multiplied by GPU count.

