# Hosted Open-Weight Pricing Findings

Retrieved: 2026-07-31

Total evidence-backed rows: 305

Every row in `findings.json` carries an exact `evidence_literal` that was mechanically checked as a substring of its saved raw `evidence_file`.

## Together AI

- Evidence-backed rows: 45
- Serverless per-token rows: 31
- Dedicated/GPU-hour rows: 14

Captured all priced text/vision, embedding, and moderation rows shown in the current serverless tables, plus Dedicated Inference and GPU Cluster rates. Model detail pages supplied endpoint IDs, context, and page-stated quantization. Exact client-calculated batch discounts were left null unless the page encoded no discount and the batch rate therefore equals the literal base rate.

## Fireworks AI

- Evidence-backed rows: 42
- Serverless per-token rows: 38
- Dedicated/GPU-hour rows: 4

Captured Standard and available Priority rows, Fast/US variants, size/architecture brackets, embedding brackets, and on-demand deployment GPU rates. Model-specific batch dollar fields remain null because the page states a discount rule rather than literal expanded dollar values.

## DeepInfra

- Evidence-backed rows: 45
- Serverless per-token rows: 40
- Dedicated/GPU-hour rows: 5

Captured unique open-family text/vision rows, embedding rows, and dedicated GPU-hour rows. Duplicate responsive/legacy rows were de-duplicated; Gemini and Claude closed-vendor tables and non-token image/audio pricing were excluded.

## Groq

- Evidence-backed rows: 7
- Serverless per-token rows: 7
- Dedicated/GPU-hour rows: 0

Captured every headline LLM row plus the Kimi row present in the Prompt Caching table. Exact cached-input rates were used where printed. The Batch API is acknowledged, but exact per-model batch dollar fields remain null because they are not printed.

## Cerebras

- Evidence-backed rows: 3
- Serverless per-token rows: 3
- Dedicated/GPU-hour rows: 0

Captured the three current Developer Tier model rows. The public models endpoint returned 403 without credentials; the static public-model documentation example supplied full ID, context, and quantization for GPT OSS only.

## Baseten

- Evidence-backed rows: 18
- Serverless per-token rows: 11
- Dedicated/GPU-hour rows: 7

Captured all current Model API rows and every GPU instance in the Dedicated Deployments price record. The static pricing page does not state context or quantization for Model APIs.

## Novita AI

- Evidence-backed rows: 105
- Serverless per-token rows: 101
- Dedicated/GPU-hour rows: 4

Captured all active records in the page's embedded `initialFullLLMModels` array, including fast/turbo variants and embeddings, plus the official dedicated-spec records. Dedicated normalized hourly decimals were withheld because the API exposes encoded price/precision integers rather than literal decimal dollar strings.

## Nebius AI Studio

- Evidence-backed rows: 40
- Serverless per-token rows: 26
- Dedicated/GPU-hour rows: 14

Captured every active public model/flavor in the official `models_info` JSON, including quantization and context, plus adjacent Nebius AI Cloud preemptible/on-demand GPU-hour infrastructure rates.

## PAGES I COULD NOT FETCH

- `https://api.cerebras.ai/v1/models` — HTTP 403 JSON response; body saved as `evidence/cerebras-api-models.json`.
- `https://api-server.novita.ai/gpus/v2/products` — HTTP 401 JSON response; body saved as `evidence/novita-gpu-products.json`.

## THINGS I COULD NOT VERIFY

- Exact per-model batch dollar rates where a provider only publishes a page-wide discount/calculation rule. Those batch fields are null unless the literal printed rate is unchanged.
- Cerebras context and quantization for ZAI GLM 4.7 and Gemma 4 31B; the current pricing page does not print them, and the public live model endpoint was inaccessible without authorization.
- Dedicated/reserved GPU-hour pricing for Cerebras and Groq; neither captured pricing page publishes literal GPU-hour rates.
- Normalized Novita dedicated GPU-hour decimals. The official endpoint exposes encoded numerator/precision fields, so only the raw encoding is recorded and `gpu_hourly_rate` is null.
- Row-level open-weight classification flags are not exposed uniformly by every provider. The capture follows provider-listed open-model/family surfaces and excludes DeepInfra's explicit Gemini/Claude closed-vendor tables, but ambiguous partner-labelled records remain identified by their exact provider IDs and notes rather than guessed from training memory.

## HTTP FETCH STATUS LOG

- HTTP 200 — https://www.together.ai/pricing
- HTTP 200 — https://fireworks.ai/pricing
- HTTP 200 — https://deepinfra.com/pricing
- HTTP 200 — https://groq.com/pricing
- HTTP 200 — https://www.cerebras.ai/pricing
- HTTP 200 — https://www.cerebras.ai/inference
- HTTP 200 — https://www.baseten.co/pricing/
- HTTP 200 — https://novita.ai/pricing
- HTTP 200 — https://studio.nebius.com/pricing → https://tokenfactory.nebius.com/pricing
- HTTP 200 — https://nebius.com/prices
- HTTP 200 — https://docs.fireworks.ai/serverless/pricing
- HTTP 200 — https://inference-docs.cerebras.ai/support → https://www.cerebras.ai/pricing
- HTTP 200 — https://inference-docs.cerebras.ai/api-reference/models/public-models
- HTTP 403 — https://api.cerebras.ai/v1/models
- HTTP 200 — https://docs.baseten.co/inference/model-apis/overview
- HTTP 200 — https://tokenfactory.nebius.com/api/public/models_info
- HTTP 200 — https://tokenfactory.nebius.com/model-catalog.md
- HTTP 200 — https://tokenfactory.nebius.com/llms.txt
- HTTP 200 — https://api-server.novita.ai/api/v1/llm/dedicated/spec
- HTTP 401 — https://api-server.novita.ai/gpus/v2/products
- HTTP 200 — https://api-server.novita.ai/api/v1/market/query_options
- HTTP 200 — https://static.nebius.com/app/ai-studio-ui/main.9e3c36e63364db98.js
- HTTP 200 — https://www.together.ai/models/cogito-v2-1-671b
- HTTP 200 — https://www.together.ai/models/deepseek-v4-pro
- HTTP 200 — https://www.together.ai/models/gemma-3n-e4b-it
- HTTP 200 — https://www.together.ai/models/gemma-4-31b
- HTTP 200 — https://www.together.ai/models/gemma-4-31b-it-pearl
- HTTP 200 — https://www.together.ai/models/glm-51
- HTTP 200 — https://www.together.ai/models/glm-52
- HTTP 200 — https://www.together.ai/models/gpt-oss-120b
- HTTP 200 — https://www.together.ai/models/gpt-oss-20b
- HTTP 200 — https://www.together.ai/models/inkling
- HTTP 200 — https://www.together.ai/models/inkling-small
- HTTP 200 — https://www.together.ai/models/kimi-k26
- HTTP 200 — https://www.together.ai/models/kimi-k27-code
- HTTP 200 — https://www.together.ai/models/kimi-k3
- HTTP 200 — https://www.together.ai/models/liquid-lfm2-5-8b-a1b
- HTTP 200 — https://www.together.ai/models/llama-3-3-70b
- HTTP 200 — https://www.together.ai/models/llama-3-8b-instruct-lite
- HTTP 200 — https://www.together.ai/models/llama-guard-4-12b
- HTTP 200 — https://www.together.ai/models/minimax-m2-7
- HTTP 200 — https://www.together.ai/models/minimax-m3
- HTTP 200 — https://www.together.ai/models/multilingual-e5-large-instruct
- HTTP 200 — https://www.together.ai/models/nvidia-nemotron-3-ultra
- HTTP 200 — https://www.together.ai/models/prism-ml-ternary-bonsai-27b
- HTTP 200 — https://www.together.ai/models/qwen2-5-7b-instruct-turbo
- HTTP 200 — https://www.together.ai/models/qwen3-235b-a22b-instruct-2507-fp8
- HTTP 200 — https://www.together.ai/models/qwen3-5-397b-a17b
- HTTP 200 — https://www.together.ai/models/qwen3-5-9b
- HTTP 200 — https://www.together.ai/models/qwen36-plus
- HTTP 200 — https://www.together.ai/models/qwen37-max
- HTTP 200 — https://www.together.ai/models/qwen37-plus
- HTTP 200 — https://www.together.ai/models/rnj-1-instruct
- HTTP 200 — https://novita.ai/_next/static/chunks/16755-21bb0ff4c9ca954b.js
- HTTP 200 — https://novita.ai/_next/static/chunks/18567-5ebf98f896fad84f.js
- HTTP 200 — https://novita.ai/_next/static/chunks/1934-12a12db37f8cb2b1.js
- HTTP 200 — https://novita.ai/_next/static/chunks/22628-c0ec42e222d702ed.js
- HTTP 200 — https://novita.ai/_next/static/chunks/25904-aa7cf1530a8b7afb.js
- HTTP 200 — https://novita.ai/_next/static/chunks/27115-29d58ec4dfdb31e4.js
- HTTP 200 — https://novita.ai/_next/static/chunks/3022-0b303f93b1b4778a.js
- HTTP 200 — https://novita.ai/_next/static/chunks/4294-677870bf10d495e1.js
- HTTP 200 — https://novita.ai/_next/static/chunks/4473-fd9ec09db1151367.js
- HTTP 200 — https://novita.ai/_next/static/chunks/47675-d4c756b16ccb0c91.js
- HTTP 200 — https://novita.ai/_next/static/chunks/48681-10df5f6bd34b2c28.js
- HTTP 200 — https://novita.ai/_next/static/chunks/4905-5d6a90ab6d92fe7c.js
- HTTP 200 — https://novita.ai/_next/static/chunks/51108-87de06ec15aaecbd.js
- HTTP 200 — https://novita.ai/_next/static/chunks/52229-1025efee48d202bd.js
- HTTP 200 — https://novita.ai/_next/static/chunks/52928-b436778ba22c73b5.js
- HTTP 200 — https://novita.ai/_next/static/chunks/57812-23e5587e1a8b5a6b.js
- HTTP 200 — https://novita.ai/_next/static/chunks/63726-318962a2b2205845.js
- HTTP 200 — https://novita.ai/_next/static/chunks/64474-72b2fd6088d1838a.js
- HTTP 200 — https://novita.ai/_next/static/chunks/69423-aeb2bb4e76fb8ba5.js
- HTTP 200 — https://novita.ai/_next/static/chunks/70026-19c559f2b69e7a77.js
- HTTP 200 — https://novita.ai/_next/static/chunks/70632-938880f930c4cc2c.js
- HTTP 200 — https://novita.ai/_next/static/chunks/73009-05bcce9ce4c781ba.js
- HTTP 200 — https://novita.ai/_next/static/chunks/77213-dbb0ed249bf8ebef.js
- HTTP 200 — https://novita.ai/_next/static/chunks/77256-e9501f975b554381.js
- HTTP 200 — https://novita.ai/_next/static/chunks/78705-aa1bc211d6c1c529.js
- HTTP 200 — https://novita.ai/_next/static/chunks/7901-d7225cb5f5684457.js
- HTTP 200 — https://novita.ai/_next/static/chunks/805-63cd2b5fab80ae1d.js
- HTTP 200 — https://novita.ai/_next/static/chunks/82347-9a2cc439323a61b5.js
- HTTP 200 — https://novita.ai/_next/static/chunks/85227-be7c89d92e9eaa43.js
- HTTP 200 — https://novita.ai/_next/static/chunks/88822-9927b034413a2836.js
- HTTP 200 — https://novita.ai/_next/static/chunks/93916-fa2dbdf4870c95f6.js
- HTTP 200 — https://novita.ai/_next/static/chunks/96296-392ed925ee7c2873.js
- HTTP 200 — https://novita.ai/_next/static/chunks/99605-eeb1217519f95aff.js
- HTTP 200 — https://novita.ai/_next/static/chunks/app/error-16c54529d6086d8d.js
- HTTP 200 — https://novita.ai/_next/static/chunks/app/global-error-585f18349b8521e3.js
- HTTP 200 — https://novita.ai/_next/static/chunks/app/layout-c6ccd2de42d085f5.js
- HTTP 200 — https://novita.ai/_next/static/chunks/app/not-found-9cc72cdbab5eee6b.js
- HTTP 200 — https://novita.ai/_next/static/chunks/app/pricing/page-d85e4e47bb44b3e6.js
- HTTP 200 — https://novita.ai/_next/static/chunks/fd9d1056-73f39082d07de1b6.js
- HTTP 200 — https://novita.ai/_next/static/chunks/main-app-9a5347c2046a2378.js
- HTTP 200 — https://novita.ai/_next/static/chunks/polyfills-42372ed130431b0a.js
- HTTP 200 — https://novita.ai/_next/static/chunks/webpack-016b79a9d64fcd0b.js
