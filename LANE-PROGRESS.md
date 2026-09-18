# Lane progress

## 2026-07-31 checkpoint 1

- Read `data/providers.json`; found 257 `B_hosted_open_api` rows: Together AI 31, DeepInfra 40, Novita AI 101, Baseten 11, Nebius AI Studio 26, Groq 7, Cerebras 3, and Fireworks AI 38.
- Saved raw HTTP 200 response bodies for all seven requested pricing pages under `evidence/`: `together_pricing.html`, `deepinfra_pricing.html`, `novita_pricing.html`, `baseten_pricing.html`, `nebius_pricing.html`, `groq_pricing.html`, and `cerebras_pricing.html`.
- Saved HTTP 200 raw responses for `evidence/nebius_models_info.json`, `evidence/nebius_main.js`, and `evidence/deepinfra_service_tier_docs.html`.
- Confirmed DeepInfra pricing HTML literally publishes service tiers `Standard`, `Priority`, and `Flex` at `1x base price`, `1.5x base price`, and `0.8x base price`.
- Confirmed Novita pricing HTML literally says: `Batch inference is available at an introductory 50% discount on input and output tokens for supported models.`
- Nebius public `models_info` currently contains 25 flavors, all labelled `cheap`, with no record containing more than one flavor and no `fast` or `base` model ID.
- Preliminary: Together exposes `Turbo` and `Lite` as separate model names; Baseten exposes one Model APIs token table plus non-token dedicated compute pricing; Groq exposes one on-demand token table plus Batch API at `50% lower cost`; Cerebras currently exposes one token table.

## 2026-07-31 checkpoint 2

- Saved HTTP 200 raw Together model pages for MiniMax M3, Llama 3.3 70B Turbo, Qwen 2.5 7B Turbo, Llama 3 8B Lite, and Qwen3 235B Throughput.
- Baseten current raw pricing data confirms a real cross-name tier-copy defect:
  - `GLM-5.2 Fast` is input `2.1`, output `6.6`; base `GLM-5.2` is input `1.4`, output `4.4`. The repo assigns `2.1 / 6.6` to both rows.
  - `Inkling-Small` is input `0.5`, output `1.2`; `Inkling` is input `1`, output `4.05`. The repo assigns `0.5 / 1.2` to both rows.
- Parsed all 11 Baseten repo models from the raw first-party page. The other nine match their current first-party Model APIs prices.
- Parsed 96 Novita chat-model records from the raw page; every matched repo row agrees with the current normal serverless list price. Two reranker records need separate handling because they are not Chat records.
- Novita publishes separate model-name variants with different prices, including `minimax/minimax-m2.5-highspeed` versus `minimax/minimax-m2.5`, `xiaomimimo/mimo-v2.5-pro` versus `xiaomimimo/mimo-v2.5`, and `zai-org/glm-4.7-flash` versus `zai-org/glm-4.7`. The page also marks some model records with the `batch-api` endpoint and publishes the generic 50% batch discount.
- Groq has one On-Demand price table and a separate Batch API section stating `50% lower cost`.
- Cerebras has Free Trial, Developer, and Enterprise account plans, but only one per-model token-price table (`Model`, `Speed`, `Input`, `Output`).

## 2026-07-31 checkpoint 3

- Wrote `findings.json` with seven provider-summary objects and 40 sampled-model objects.
- Wrote `FINDINGS.md` with provider-by-provider tier shapes, exact label quotes, multiplier examples, sampled rows, mandatory fetch-gap section, and mandatory uncertainty section.
- Confirmed hazards: DeepInfra Standard/Priority/Flex; Novita Batch plus separate Highspeed/Pro/Flash names; Baseten separate base/Fast names; Groq On-Demand versus Batch API.
- Confirmed two mislabelled repo rows, both Baseten: `zai-org/GLM-5.2` contains the Fast pair, and `Inkling` contains the Inkling-Small pair.
- Mechanically checked all 47 `evidence_literal` values against their declared raw evidence files: zero misses.
- Mechanically checked every sampled repo and cheapest-standard numeric field against that row's `evidence_literal`: zero misses.
- Mechanically checked every provider-summary tier-label quote against its declared raw evidence file: zero misses.

