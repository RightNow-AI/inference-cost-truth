# LANE k3-glm progress

## 2026-07-31 start

- Confirmed worktree root and inspected repository schemas without running git or tests.
- Existing generated data mentions both target models, but it will be used only to locate official sources; all reported facts will come from fresh raw HTTP captures under `evidence/`.
- Next: fetch provider catalogs/pricing, official model cards/docs, and benchmark APIs.

## 2026-07-31 pricing and benchmark capture

- Saved fresh raw HTTP bodies plus observed status logs for Fireworks, Together, Baseten, Novita, Nebius, DeepInfra, Groq, Cerebras, SiliconFlow, Moonshot/Kimi first party, Z.AI first party, both official Hugging Face repos, and the SemiAnalysis InferenceX API.
- Confirmed static/raw price literals exist for Fireworks (including Standard/Priority and named Fast/US variants), Together, Novita, Baseten, Nebius, SiliconFlow, Kimi first party, and Z.AI first party.
- DeepInfra's raw catalog lists GLM-5.2; model-specific endpoints were captured for a closer price/tier check. No Kimi-K3 string appeared on the DeepInfra pricing response.
- Groq and Cerebras captured pricing/model pages contain neither target model name. SiliconFlow contains both targets.
- InferenceX returned 16 Kimi-K3 records and 40 GLM-5.2 records. They are agentic-trace runs with concurrency and observed mean token lengths rather than fixed ISL/OSL fields; engine-image version sufficiency is still being checked before accepting a row.

## 2026-07-31 strict throughput and provider closeout

- Saved the official vLLM launch/preview articles and official SGLang/LMSYS launch/optimization articles for both models, plus official AMD ROCm and NVIDIA blog search responses.
- GLM-5.2 has a fully specified official SGLang result: the same page states the GPU deployment, SGLang version, NVFP4 precision, batch/concurrency basis, agentic input/output lengths, and output throughput.
- Kimi K3 has strong official vLLM/SGLang results and recipes, but none of the captured Kimi sources states a semantic engine version, commit, or immutable image digest alongside the result. The public InferenceX rows likewise use the unversioned `vllm/vllm-openai:kimi-k3` tag. This will be reported as a strict evidence gap rather than promoted to a self-hosting datapoint.
- Fresh provider closeout: Nebius currently lists GLM-5.2 but not Kimi K3; DeepInfra lists GLM-5.2 with Standard, Priority, and Flex prices; SiliconFlow lists both models; Groq and Cerebras list neither target on the captured official pages.

## 2026-07-31 outputs complete

- Wrote `findings.json` with 23 hosted-price rows, 2 official metadata rows, and 2 throughput rows (one verified GLM-5.2 datapoint and one explicit Kimi K3 evidence-gap row).
- Wrote `FINDINGS.md` with provider-grouped prices, official metadata, the self-hosting verdict for each model, InferenceX key enumeration, fetch failures, and unverified items.
- Mechanically checked all 27 primary `evidence_literal` strings against their declared evidence files and separately checked every populated numeric comparison field against its row literal.
