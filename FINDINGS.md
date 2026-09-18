# Throughput operating-point findings

Retrieved on 2026-07-31. The publishable set contains **50 COMPLETE concurrency sweeps** and **356 evidence-backed point rows**, spanning **8 models** and the exact InferenceX hardware keys `h100`, `h200`, `b200`, `b300`, `mi300x`, `mi325x`, and `mi355x`.

The critical basis rule is absolute: every InferenceX `throughput_tok_per_s` value is copied from the source field `metrics.output_tput_per_gpu`, recorded as `per_gpu_output`, and never multiplied. For non-disaggregated rows, `gpu_count` is the common `num_prefill_gpu`/`num_decode_gpu` value; those two equal fields are not added together.

Each point also carries the source `metrics.mean_intvty`, which the official frontend labels **Mean Interactivity (tok/s/user)**. That permits throughput-versus-user-speed analysis from the same run without deriving a reciprocal latency number.

## Selection rule

The full API sets produced 692 clean exact-run candidate groups after rejecting disaggregated rows, missing images/versions, incomplete required fields, groups with fewer than three concurrency levels, and groups containing duplicate concurrency values. To avoid listing many near-duplicate builds, the retained set is the widest clean sweep per current API model and exact hardware key, with deterministic tie-breaks: latest benchmark date, then 1k/1k sequence, then lower GPU count, then image tag.

## COMPLETE sweeps

| Sweep | Model | Hardware | GPUs | Engine / version | Precision | ISL/OSL | Points | Concurrency levels | Min output tok/s/GPU | Max output tok/s/GPU |
|---|---|---:|---:|---|---|---:|---:|---|---:|---:|
| IX-001 | DeepSeek-R1-0528 | `b200` | 8 | SGLang / `v0.5.12-cu130` | fp8 | 1024/1024 | 10 | 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 | 29.213357921647503 | 1073.4857008366578 |
| IX-002 | DeepSeek-R1-0528 | `b300` | 8 | SGLang / `v0.5.15.post1-cu130` | fp8 | 8192/1024 | 10 | 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 | 32.13549848558322 | 319.5683393414602 |
| IX-003 | DeepSeek-R1-0528 | `h200` | 64 | TensorRT-LLM / `1.1.0rc2.post2` | fp8 | 1024/8192 | 6 | 4, 8, 16, 32, 64, 128 | 68.6965550322458 | 650.7008749992362 |
| IX-004 | DeepSeek-R1-0528 | `mi300x` | 8 | SGLang / `v0.5.12-rocm700-mi30x` | fp8 | 1024/1024 | 5 | 4, 8, 16, 32, 64 | 31.64334900447029 | 188.44172990747268 |
| IX-005 | DeepSeek-R1-0528 | `mi325x` | 8 | SGLang / `v0.5.12-rocm700-mi30x` | fp8 | 1024/1024 | 5 | 4, 8, 16, 32, 64 | 32.96699004467202 | 219.7745937878908 |
| IX-006 | DeepSeek-R1-0528 | `mi355x` | 8 | ATOM / `rocm7.2.4_ubuntu24.04_py3.12_pytorch_release_2.10.0_atom0.1.3` | fp8 | 1024/1024 | 8 | 4, 8, 16, 32, 64, 128, 256, 512 | 25.279782217365234 | 911.2194133229364 |
| IX-007 | DeepSeek-V4-Pro | `b200` | 8 | vLLM / `v0.25.0` | fp4 | 1024/1024 | 7 | 1, 2, 4, 8, 16, 32, 64 | 11.915463205705189 | 319.1141410213594 |
| IX-008 | DeepSeek-V4-Pro | `b300` | 4 | vLLM / `v0.25.0` | fp4 | 1024/1024 | 9 | 1, 2, 4, 8, 16, 32, 64, 128, 256 | 43.93253164848933 | 1391.518568071143 |
| IX-009 | DeepSeek-V4-Pro | `h200` | 8 | vLLM / `v0.25.1` | fp8 | 1024/1024 | 8 | 1, 2, 4, 8, 16, 64, 128, 256 | 20.176719222862317 | 126.52322007732391 |
| IX-010 | DeepSeek-V4-Pro | `mi300x` | 8 | vLLM / `nightly-09663abde0f50944a8d5ea30120666024b503faa` | fp8 | 1024/1024 | 8 | 4, 8, 16, 32, 64, 128, 256, 512 | 9.973388609444033 | 262.8900761341054 |
| IX-011 | DeepSeek-V4-Pro | `mi325x` | 8 | vLLM / `nightly-09663abde0f50944a8d5ea30120666024b503faa` | fp8 | 1024/1024 | 8 | 4, 8, 16, 32, 64, 128, 256, 512 | 10.067312805913051 | 308.016215283587 |
| IX-012 | DeepSeek-V4-Pro | `mi355x` | 8 | ATOM / `rocm7.2.4_ubuntu24.04_py3.12_pytorch_release_2.10.0_atom0.1.3` | fp4 | 1024/1024 | 11 | 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024 | 13.892610387606927 | 698.447709513656 |
| IX-013 | GLM-5 | `b200` | 4 | SGLang / `nightly-dev-cu13-20260605-7dc73766` | fp4 | 1024/1024 | 7 | 4, 8, 16, 32, 64, 128, 256 | 136.4036465999145 | 1065.477087216986 |
| IX-014 | GLM-5 | `b300` | 4 | SGLang / `v0.5.12-cu130` | fp4 | 1024/1024 | 7 | 4, 8, 16, 32, 64, 128, 256 | 80.54161837384495 | 1444.30165723849 |
| IX-015 | GLM-5 | `h200` | 8 | SGLang / `v0.5.12-cu130` | fp8 | 1024/1024 | 5 | 4, 8, 16, 32, 64 | 28.75859739269279 | 166.19612541450937 |
| IX-016 | GLM-5 | `mi325x` | 8 | SGLang / `v0.5.12-rocm720-mi30x` | fp8 | 1024/1024 | 5 | 4, 8, 16, 32, 64 | 15.986206896682404 | 125.85902069129665 |
| IX-017 | GLM-5 | `mi355x` | 2 | SGLang / `v0.5.13.post1-rocm720-mi35x-20260622` | fp4 | 1024/1024 | 7 | 4, 8, 16, 32, 64, 128, 256 | 102.42262928697913 | 1145.7330668349719 |
| IX-018 | gpt-oss-120b | `b200` | 2 | TensorRT-LLM / `1.3.0rc14` | fp4 | 1024/1024 | 7 | 4, 8, 16, 32, 64, 128, 256 | 676.8048071432216 | 8546.991986607418 |
| IX-019 | gpt-oss-120b | `h100` | 2 | vLLM / `v0.21.0` | fp4 | 1024/1024 | 5 | 4, 8, 16, 32, 64 | 373.07192763088625 | 2079.299971872639 |
| IX-020 | gpt-oss-120b | `h200` | 2 | vLLM / `v0.22.0` | fp4 | 1024/1024 | 5 | 4, 8, 16, 32, 64 | 394.0589411414046 | 2129.4002790526642 |
| IX-021 | gpt-oss-120b | `mi300x` | 2 | vLLM / `v0.17.0` | fp4 | 1024/1024 | 5 | 4, 8, 16, 32, 64 | 327.27172903733776 | 1869.260521536098 |
| IX-022 | gpt-oss-120b | `mi325x` | 1 | vLLM / `v0.22.0` | fp4 | 1024/1024 | 5 | 4, 8, 16, 32, 64 | 278.13066287634103 | 1823.8243019551285 |
| IX-023 | gpt-oss-120b | `mi355x` | 1 | vLLM / `v0.22.0` | fp4 | 1024/1024 | 6 | 4, 8, 16, 32, 64, 128 | 913.2410953487833 | 8774.334410159883 |
| IX-024 | Kimi-K2.5 | `b200` | 4 | vLLM / `v0.22.0` | fp4 | 1024/1024 | 8 | 1, 2, 4, 8, 16, 32, 64, 128 | 38.8795095397644 | 1038.435604997667 |
| IX-025 | Kimi-K2.5 | `b300` | 4 | vLLM / `v0.22.0` | fp4 | 1024/1024 | 8 | 1, 2, 4, 8, 16, 32, 64, 128 | 39.670959392963425 | 1062.0281610653517 |
| IX-026 | Kimi-K2.5 | `h200` | 8 | vLLM / `v0.22.0` | int4 | 1024/1024 | 5 | 4, 8, 16, 32, 64 | 50.7232635684782 | 260.5762665290102 |
| IX-027 | Kimi-K2.5 | `mi300x` | 8 | vLLM / `v0.21.0` | int4 | 1024/1024 | 5 | 4, 8, 16, 32, 64 | 23.621893078581863 | 103.17323461551375 |
| IX-028 | Kimi-K2.5 | `mi325x` | 8 | vLLM / `v0.21.0` | int4 | 1024/1024 | 5 | 4, 8, 16, 32, 64 | 24.805768038677737 | 118.87654506725349 |
| IX-029 | Kimi-K2.5 | `mi355x` | 4 | vLLM / `nightly-387189c42997b27e2c04b5d97ef8190ffa2bf909` | fp4 | 8192/1024 | 6 | 4, 8, 16, 32, 64, 128 | 109.0457807927896 | 566.5904155261447 |
| IX-030 | MiniMax-M2.5 | `b200` | 2 | vLLM / `v0.22.0` | fp8 | 8192/1024 | 8 | 4, 8, 16, 32, 64, 128, 256, 512 | 212.7385081795555 | 1154.219854886341 |
| IX-031 | MiniMax-M2.5 | `b300` | 2 | vLLM / `v0.19.0-cu130` | fp8 | 1024/1024 | 8 | 4, 8, 16, 32, 64, 128, 256, 512 | 205.2480459396775 | 4608.533916673441 |
| IX-032 | MiniMax-M2.5 | `h100` | 64 | vLLM / `v0.22.0` | fp8 | 1024/1024 | 6 | 4, 8, 16, 32, 64, 128 | 56.44086351330988 | 632.9436609734709 |
| IX-033 | MiniMax-M2.5 | `h200` | 4 | vLLM / `v0.22.0` | fp8 | 1024/1024 | 9 | 1, 2, 4, 8, 16, 32, 64, 128, 256 | 33.11178780344081 | 1547.6895383255346 |
| IX-034 | MiniMax-M2.5 | `mi300x` | 2 | vLLM / `v0.21.0` | fp8 | 1024/1024 | 5 | 4, 8, 16, 32, 64 | 153.54246052774883 | 821.291055621522 |
| IX-035 | MiniMax-M2.5 | `mi325x` | 64 | vLLM / `v0.22.0` | fp8 | 1024/1024 | 8 | 4, 8, 16, 32, 64, 128, 256, 512 | 50.29028483880898 | 1619.007183989124 |
| IX-036 | MiniMax-M2.5 | `mi355x` | 4 | vLLM / `v0.22.0` | fp8 | 1024/1024 | 9 | 2, 4, 8, 16, 32, 64, 128, 256, 512 | 117.82115165078908 | 3943.737684553362 |
| IX-037 | MiniMax-M3 | `b200` | 64 | vLLM / `vllm-minimax-m3-perf-x86_64-13.0.1-8b00f41` | fp4 | 1024/1024 | 10 | 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 | 22.09229845284698 | 1616.3171196062049 |
| IX-038 | MiniMax-M3 | `b300` | 64 | vLLM / `nightly-4080263bb2c5d10deac17aaeb88e0823bc35bca9` | fp8 | 8192/1024 | 10 | 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 | 24.597326652113225 | 645.4400496648859 |
| IX-039 | MiniMax-M3 | `h100` | 64 | vLLM / `minimax-m3` | fp8 | 1024/1024 | 9 | 1, 2, 4, 8, 16, 32, 64, 128, 256 | 13.940149612805756 | 413.4405229717141 |
| IX-040 | MiniMax-M3 | `h200` | 16 | vLLM / `minimax-m3` | fp8 | 1024/1024 | 9 | 1, 2, 4, 8, 16, 32, 64, 128, 256 | 29.231521204905473 | 740.1301822466194 |
| IX-041 | MiniMax-M3 | `mi300x` | 8 | vLLM / `nightly-4559c43a9526597c00cbcc4f59979496500268d1` | fp8 | 1024/1024 | 9 | 1, 2, 4, 8, 16, 32, 64, 128, 256 | 12.116656712130595 | 453.6417379062121 |
| IX-042 | MiniMax-M3 | `mi325x` | 8 | vLLM / `minimax-m3` | fp8 | 1024/1024 | 8 | 1, 2, 4, 8, 16, 32, 64, 128 | 11.806132720788737 | 346.64513784519306 |
| IX-043 | MiniMax-M3 | `mi355x` | 4 | vLLM / `nightly-69715823df89b11ee684b84066390cbb9092d5c1` | fp4 | 1024/1024 | 10 | 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 | 41.932206676569024 | 2574.42001712596 |
| IX-044 | Qwen-3.5-397B-A17B | `b200` | 4 | SGLang / `v0.5.14-cu130` | fp8 | 1024/1024 | 7 | 4, 8, 16, 32, 64, 128, 256 | 133.9325413026864 | 1876.9516489993753 |
| IX-045 | Qwen-3.5-397B-A17B | `b300` | 4 | SGLang / `v0.5.12-cu130` | fp8 | 1024/1024 | 7 | 4, 8, 16, 32, 64, 128, 256 | 139.87467319598002 | 1839.0839131584682 |
| IX-046 | Qwen-3.5-397B-A17B | `h100` | 64 | SGLang / `v0.5.14-cu130` | fp8 | 1024/1024 | 5 | 16, 32, 64, 128, 256 | 129.5571118741794 | 667.8201370349136 |
| IX-047 | Qwen-3.5-397B-A17B | `h200` | 64 | SGLang / `v0.5.14-cu130` | fp8 | 1024/1024 | 6 | 4, 8, 16, 32, 64, 128 | 85.54011019586088 | 433.4154470772047 |
| IX-048 | Qwen-3.5-397B-A17B | `mi300x` | 8 | SGLang / `v0.5.12-rocm720-mi30x` | bf16 | 1024/1024 | 5 | 4, 8, 16, 32, 64 | 45.39627989978077 | 278.4100795373653 |
| IX-049 | Qwen-3.5-397B-A17B | `mi325x` | 8 | SGLang / `v0.5.12-rocm720-mi30x` | bf16 | 1024/1024 | 5 | 4, 8, 16, 32, 64 | 46.72284934676396 | 312.85196331899544 |
| IX-050 | Qwen-3.5-397B-A17B | `mi355x` | 4 | SGLang / `v0.5.16-rocm720-mi35x-20260726` | fp8 | 8192/1024 | 7 | 4, 8, 16, 32, 64, 128, 256 | 142.2976805144594 | 734.0645386140262 |

## SemiAnalysis InferenceX

The no-parameter benchmark request returned HTTP 400 `{"error":"Unknown model"}`, and `/api/v1/models` returned HTTP 404. The current official frontend bundle was therefore used to enumerate the model values, and each exact database model string was requested directly. All successful result bodies are saved as decompressed, unmodified JSON under `evidence/`.

| Current API model value | Full result rows | Retained COMPLETE sweeps | HTTP |
|---|---:|---:|---:|
| DeepSeek-R1-0528 | 1744 | 6 | 200 |
| gpt-oss-120b | 502 | 6 | 200 |
| Llama-3.3-70B-Instruct-FP8 | 681 | 0 | 200 |
| Qwen-3.5-397B-A17B | 741 | 7 | 200 |
| Kimi-K2.5 | 406 | 6 | 200 |
| Kimi-K3 | 16 | 0 | 200 |
| MiniMax-M2.5 | 814 | 7 | 200 |
| MiniMax-M3 | 1468 | 7 | 200 |
| GLM-5 | 519 | 5 | 200 |
| GLM-5.2 | 40 | 0 | 200 |
| DeepSeek-V4-Pro | 1034 | 6 | 200 |

`Llama-3.3-70B-Instruct-FP8`, `Kimi-K3`, and `GLM-5.2` returned data but did not yield a retained COMPLETE fixed-sequence sweep under the stated rule. A legacy configuration name, `Llama-3.1-70B-Instruct-FP8-KV`, returned HTTP 400 and is not treated as currently served.

## Other official sources checked: nothing usable under the evidence law

- AMD ROCm: `scaling-ai-inference`, `LLM_Inference`, and `DeepSeekR1_Perf` all returned HTTP 200. They describe concurrency sweeps, but their plotted series are raster images or otherwise do not expose three literal throughput values for one fixed configuration in the saved HTML.
- LMSYS/SGLang: the GLM-5.2 optimization page and the KTransformers page both returned HTTP 200. The relevant multi-point curves/tables are raster-only; text provides descriptions, ratios, or a later single operating point, not a literal complete curve.
- vLLM blog: the official index returned HTTP 200, but no complete literal three-point fixed-configuration concurrency sweep was located in the current index.
- NVIDIA TensorRT-LLM: the performance overview and benchmarking docs returned HTTP 200. They publish tables, maximum-load results, and one-point examples, but not three or more concurrency points for one fixed model/hardware/engine configuration.
- MLPerf Inference: the v5.1 results page returned HTTP 200, but submissions are operating points rather than same-system concurrency sweeps. The probed v6.0 documentation URL returned HTTP 404.

## PAGES I COULD NOT FETCH

- `https://inferencex.semianalysis.com/api/v1/models` â€” HTTP 404; no model-list endpoint at that path.
- `https://docs.mlcommons.org/inference_results_v6.0/` â€” HTTP 404.
- `https://inferencex.semianalysis.com/api/v1/benchmarks` without an accepted `model` value â€” HTTP 400 `Unknown model`; the endpoint itself was reachable.

## THINGS I COULD NOT VERIFY

- No COMPLETE current sweep with an exact `gb200` hardware key was found. I did not relabel `b200` rows as GB200 systems.
- The external official blog plots could not be converted into rows without violating the literal-substring evidence law; their PNG pixels are not machine-grep-able numeric source text.
- Image tags are used as `engine_version`. For custom or nightly images, the tag identifies the exact build but may not be a semantic release number.
- Rental prices and cost-per-token ratios were not collected or derived in this lane. The output supplies the fixed-hardware throughput curves for the orchestrator to combine with its price data.
- I did not infer aggregate system throughput from InferenceX. Every reported throughput remains per-GPU output throughput exactly as sourced.

## Evidence and HTTP inventory

`findings.json` contains the full `source_checks` inventory with every URL requested in this lane, its observed HTTP status, saved response path, and usability outcome. Each findings row contains the complete raw source object as `evidence_literal`; therefore the model configuration, GPU counts, sequence lengths, concurrency, `mean_intvty`, and `output_tput_per_gpu` number all occur literally in the named evidence file.

