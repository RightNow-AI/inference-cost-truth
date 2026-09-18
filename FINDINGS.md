# Hosted inference tier audit

Retrieved on `2026-07-31`. Every cited body was downloaded with `curl.exe -L` from a first-party URL and saved under `evidence/`.

## Executive result

- Confirmed multi-price hazards: **DeepInfra** (Standard/Priority/Flex multipliers), **Novita AI** (Batch plus separate Highspeed/Pro/Flash model names), **Baseten** (base/Fast separate model names), and **Groq** (On-Demand versus Batch API).
- No current same-model per-token tier hazard found: **Together AI**, **Nebius AI Studio**, and **Cerebras**. Together still has suffix-normalization risk because Turbo/Lite/Throughput are separate model names.
- Confirmed repo mislabels: **Baseten `zai-org/GLM-5.2`** carries the Fast price, and **Baseten `Inkling`** carries the Inkling-Small price.
- Evidence-backed sampled model rows: **40**; provider summary rows: **7**; mislabelled sampled rows: **2**.

## Together AI

- More than one per-token price tier for the same model: **no**.
- Provider words: `Turbo`, `Lite`, `Throughput`.
- Scraper shape: separate MODEL NAMES; no same-model tier columns or same-model tier table in the current serverless pricing surface.
- Literal label quotes:
  - `Turbo`
  - `Lite`
  - `Throughput`
- Multiplier examples:
  - Not computable: the current page does not simultaneously list an identical unsuffixed base SKU for the sampled Turbo, Lite, or Throughput names.
- Evidence: `evidence/together_pricing.html`; HTTP `200`; source `https://www.together.ai/pricing`.
- Caveat: The requested Reference label was not present on the current raw pricing page. Variant words are embedded in model names, so a scraper fails by normalizing away the suffix, not by choosing a wrong column.

| Repo model | Repo input | Repo output | Number belongs to | Cheapest standard input | Cheapest standard output | Verdict | Evidence |
|---|---:|---:|---|---:|---:|---|---|
| `MiniMaxAI/MiniMax-M3` | 0.30 | 1.20 | standard model-name SKU | 0.30 | 1.20 | **correctly_labelled** | `evidence/together_model_minimax_m3.html` |
| `meta-llama/Llama-3.3-70B-Instruct-Turbo` | 1.04 | 1.04 | Turbo separate model-name SKU | unverified | unverified | **correctly_labelled** | `evidence/together_model_llama_3_3_70b.html` |
| `Qwen/Qwen2.5-7B-Instruct-Turbo` | 0.30 | 0.30 | Turbo separate model-name SKU | unverified | unverified | **correctly_labelled** | `evidence/together_model_qwen2_5_7b_turbo.html` |
| `meta-llama/Meta-Llama-3-8B-Instruct-Lite` | 0.14 | 0.14 | Lite separate model-name SKU | unverified | unverified | **correctly_labelled** | `evidence/together_model_llama_3_8b_lite.html` |
| `Qwen/Qwen3-235B-A22B-Instruct-2507-tput` | 0.20 | 0.60 | Throughput separate model-name SKU | unverified | unverified | **correctly_labelled** | `evidence/together_model_qwen3_235b_throughput.html` |

## DeepInfra

- More than one per-token price tier for the same model: **yes**.
- Provider words: `Standard`, `Priority`, `Flex`.
- Scraper shape: separate TABLES: model list prices are in the main pricing tables; tier multipliers are in a separate Service Tiers table.
- Literal label quotes:
  - `Standard`
  - `Priority`
  - `Flex`
  - `1x base price`
  - `1.5x base price`
  - `0.8x base price`
- Multiplier examples:
  - The first sampled model: Standard 1x base price, Priority 1.5x base price, Flex 0.8x base price.
  - The second sampled model: Standard 1x base price, Priority 1.5x base price, Flex 0.8x base price.
  - The third sampled model: Standard 1x base price, Priority 1.5x base price, Flex 0.8x base price.
- Evidence: `evidence/deepinfra_pricing.html`; HTTP `200`; source `https://deepinfra.com/pricing`.
- Caveat: The page says availability varies by model. The sampled repo numbers match the base price table and therefore belong to Standard, not Priority or Flex.

| Repo model | Repo input | Repo output | Number belongs to | Cheapest standard input | Cheapest standard output | Verdict | Evidence |
|---|---:|---:|---|---:|---:|---|---|
| `meta-llama/Llama-3.3-70B-Instruct-Turbo` | 0.10 | 0.32 | Standard (1x base price) | 0.10 | 0.32 | **correctly_labelled** | `evidence/deepinfra_pricing.html` |
| `Qwen/Qwen3-32B` | 0.08 | 0.28 | Standard (1x base price) | 0.08 | 0.28 | **correctly_labelled** | `evidence/deepinfra_pricing.html` |
| `google/gemma-3-27b-it` | 0.08 | 0.16 | Standard (1x base price) | 0.08 | 0.16 | **correctly_labelled** | `evidence/deepinfra_pricing.html` |
| `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo` | 0.02 | 0.04 | Standard (1x base price) | 0.02 | 0.04 | **correctly_labelled** | `evidence/deepinfra_pricing.html` |

## Novita AI

- More than one per-token price tier for the same model: **yes**.
- Provider words: `normal serverless list price`, `Batch inference`, `Highspeed`, `Pro`, `Flash`.
- Scraper shape: mixed: Batch is a separate explanatory discount applied to supported models; Highspeed, Pro, and Flash are separate MODEL NAMES.
- Literal label quotes:
  - `Batch inference`
  - `highspeed`
  - `Pro`
  - `Flash`
- Multiplier examples:
  - The sampled OpenAI batch-api model: Batch is 50% off the printed list price.
  - The sampled Qwen vision-language batch-api model: Batch is 50% off the printed list price.
  - The sampled DeepSeek reasoning batch-api model: Batch is 50% off the printed list price.
  - The sampled Highspeed/base pair is two-to-one for both input and output; exact source prices are in the paired sampled rows.
  - The sampled Pro/base pair has the same input/output ratio; exact source prices are in the paired sampled rows.
  - The sampled Flash/base pair is not a uniform input/output multiplier; exact source prices are in the paired sampled rows.
- Evidence: `evidence/novita_pricing.html`; HTTP `200`; source `https://novita.ai/pricing`.
- Caveat: The raw page identifies batch-capable records by the batch-api endpoint. It does not print the discounted dollar totals, so this report preserves the literal 50% rule and does not invent derived batch prices.

| Repo model | Repo input | Repo output | Number belongs to | Cheapest standard input | Cheapest standard output | Verdict | Evidence |
|---|---:|---:|---|---:|---:|---|---|
| `minimax/minimax-m2.5` | 0.3 | 1.2 | base model-name SKU | 0.3 | 1.2 | **correctly_labelled** | `evidence/novita_pricing.html` |
| `minimax/minimax-m2.5-highspeed` | 0.6 | 2.4 | Highspeed separate model-name SKU | 0.3 | 1.2 | **correctly_labelled** | `evidence/novita_pricing.html` |
| `xiaomimimo/mimo-v2.5` | 0.168 | 0.336 | base model-name SKU | 0.168 | 0.336 | **correctly_labelled** | `evidence/novita_pricing.html` |
| `xiaomimimo/mimo-v2.5-pro` | 0.522 | 1.044 | Pro separate model-name SKU | 0.168 | 0.336 | **correctly_labelled** | `evidence/novita_pricing.html` |
| `zai-org/glm-4.7` | 0.6 | 2.2 | base model-name SKU | 0.6 | 2.2 | **correctly_labelled** | `evidence/novita_pricing.html` |
| `zai-org/glm-4.7-flash` | 0.07 | 0.4 | Flash separate model-name SKU | 0.6 | 2.2 | **correctly_labelled** | `evidence/novita_pricing.html` |
| `openai/gpt-oss-120b` | 0.05 | 0.25 | normal serverless list price; batch-api supported | 0.05 | 0.25 | **correctly_labelled** | `evidence/novita_pricing.html` |
| `qwen/qwen3-vl-235b-a22b-instruct` | 0.3 | 1.5 | normal serverless list price; batch-api supported | 0.3 | 1.5 | **correctly_labelled** | `evidence/novita_pricing.html` |
| `deepseek/deepseek-r1-0528` | 0.7 | 2.5 | normal serverless list price; batch-api supported | 0.7 | 2.5 | **correctly_labelled** | `evidence/novita_pricing.html` |

## Baseten

- More than one per-token price tier for the same model: **yes**.
- Provider words: `GLM-5.2`, `GLM-5.2 Fast`.
- Scraper shape: separate MODEL NAMES in one Model APIs list; no tier columns.
- Literal label quotes:
  - `GLM-5.2 Fast`
  - `GLM-5.2`
- Multiplier examples:
  - GLM-5.2 Fast versus GLM-5.2: input ratio 2.1:1.4 and output ratio 6.6:4.4, both three-to-two. This is the only exact base/Fast pair currently published on the page.
- Evidence: `evidence/baseten_pricing.html`; HTTP `200`; source `https://www.baseten.co/pricing/`.
- Caveat: This provider contains two confirmed repo mislabels: the base GLM-5.2 row carries Fast prices, and the Inkling row carries Inkling-Small prices.

| Repo model | Repo input | Repo output | Number belongs to | Cheapest standard input | Cheapest standard output | Verdict | Evidence |
|---|---:|---:|---|---:|---:|---|---|
| `moonshotai/Kimi-K3` | 3 | 15 | Model APIs list price | 3 | 15 | **correctly_labelled** | `evidence/baseten_pricing.html` |
| `zai-org/GLM-5.2-Fast` | 2.1 | 6.6 | GLM-5.2 Fast separate model name | 1.4 | 4.4 | **correctly_labelled** | `evidence/baseten_pricing.html` |
| `Inkling-Small` | 0.5 | 1.2 | Inkling-Small separate model name | 0.5 | 1.2 | **correctly_labelled** | `evidence/baseten_pricing.html` |
| `Inkling` | 0.5 | 1.2 | Inkling-Small separate model name | 1 | 4.05 | **mislabelled** | `evidence/baseten_pricing.html` |
| `zai-org/GLM-5.2` | 2.1 | 6.6 | GLM-5.2 Fast separate model name | 1.4 | 4.4 | **mislabelled** | `evidence/baseten_pricing.html` |
| `GLM 4.7` | 0.6 | 2.2 | Model APIs list price | 0.6 | 2.2 | **correctly_labelled** | `evidence/baseten_pricing.html` |
| `moonshotai/Kimi-K2.7-Code` | 0.95 | 4 | Model APIs list price | 0.95 | 4 | **correctly_labelled** | `evidence/baseten_pricing.html` |
| `moonshotai/Kimi-K2.6` | 0.95 | 4 | Model APIs list price | 0.95 | 4 | **correctly_labelled** | `evidence/baseten_pricing.html` |
| `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B` | 0.6 | 2.4 | Model APIs list price | 0.6 | 2.4 | **correctly_labelled** | `evidence/baseten_pricing.html` |
| `DeepSeek V4` | 1.74 | 3.48 | Model APIs list price | 1.74 | 3.48 | **correctly_labelled** | `evidence/baseten_pricing.html` |
| `openai/gpt-oss-120b` | 0.1 | 0.5 | Model APIs list price | 0.1 | 0.5 | **correctly_labelled** | `evidence/baseten_pricing.html` |

## Nebius AI Studio

- More than one per-token price tier for the same model: **no**.
- Provider words: `cheap`.
- Scraper shape: JSON flavor objects; the current public models_info response has one flavor per listed model and no fast/base pair.
- Literal label quotes:
  - `"label":"cheap"`
- Multiplier examples:
  - Not computable: no current record exposes more than one flavor, and no fast or base flavor label is present.
- Evidence: `evidence/nebius_models_info.json`; HTTP `200`; source `https://tokenfactory.nebius.com/api/public/models_info`.
- Caveat: The requested fast-versus-base distinction was not present in the current raw public API response. This is a current-page finding, not a claim about historical Nebius lineups.

| Repo model | Repo input | Repo output | Number belongs to | Cheapest standard input | Cheapest standard output | Verdict | Evidence |
|---|---:|---:|---|---:|---:|---|---|
| `google/gemma-3-27b-it` | 0.1 | 0.3 | cheap flavor; only published flavor in current record | 0.1 | 0.3 | **correctly_labelled** | `evidence/nebius_models_info.json` |
| `meta-llama/Llama-3.3-70B-Instruct` | 0.13 | 0.4 | cheap flavor; only published flavor in current record | 0.13 | 0.4 | **correctly_labelled** | `evidence/nebius_models_info.json` |
| `MiniMaxAI/MiniMax-M3` | 0.3 | 1.2 | cheap flavor; only published flavor in current record | 0.3 | 1.2 | **correctly_labelled** | `evidence/nebius_models_info.json` |
| `openai/gpt-oss-120b` | 0.15 | 0.6 | cheap flavor; only published flavor in current record | 0.15 | 0.6 | **correctly_labelled** | `evidence/nebius_models_info.json` |

## Groq

- More than one per-token price tier for the same model: **yes**.
- Provider words: `On-Demand`, `Batch API`.
- Scraper shape: separate SECTIONS: one On-Demand price table plus a Batch API prose section; no side-by-side price columns.
- Literal label quotes:
  - `Groq On-Demand Pricing for Tokens-as-a-Service`
  - `Batch API`
  - `50% lower cost`
- Multiplier examples:
  - The sampled small GPT OSS model: Batch is 50% lower than On-Demand.
  - The sampled large GPT OSS model: Batch is 50% lower than On-Demand.
  - The sampled Llama Versatile model: Batch is 50% lower than On-Demand.
- Evidence: `evidence/groq_pricing.html`; HTTP `200`; source `https://groq.com/pricing`.
- Caveat: The repo rows store On-Demand prices. Batch is cheaper but asynchronous and is not the standard on-demand tier requested for the comparison field.

| Repo model | Repo input | Repo output | Number belongs to | Cheapest standard input | Cheapest standard output | Verdict | Evidence |
|---|---:|---:|---|---:|---:|---|---|
| `openai/gpt-oss-20b` | 0.075 | 0.30 | On-Demand | 0.075 | 0.30 | **correctly_labelled** | `evidence/groq_pricing.html` |
| `openai/gpt-oss-120b` | 0.15 | 0.60 | On-Demand | 0.15 | 0.60 | **correctly_labelled** | `evidence/groq_pricing.html` |
| `llama-3.3-70b-versatile` | 0.59 | 0.79 | On-Demand | 0.59 | 0.79 | **correctly_labelled** | `evidence/groq_pricing.html` |
| `qwen/qwen3.6-27b` | 0.60 | 3.00 | On-Demand | 0.60 | 3.00 | **correctly_labelled** | `evidence/groq_pricing.html` |

## Cerebras

- More than one per-token price tier for the same model: **no**.
- Provider words: `none published for per-token prices`.
- Scraper shape: one per-model token-price TABLE; the named account plans change credits, rate limits, and enterprise terms rather than publishing alternate token prices.
- Literal label quotes:
  - `\"cells\":[\"Model\",\"Speed\",\"Input\",\"Output\"]`
- Multiplier examples:
  - Not computable: the current page prints one Input and one Output price per model.
- Evidence: `evidence/cerebras_pricing.html`; HTTP `200`; source `https://www.cerebras.ai/pricing`.
- Caveat: No second per-token price table or per-model speed tier was present in the current raw page.

| Repo model | Repo input | Repo output | Number belongs to | Cheapest standard input | Cheapest standard output | Verdict | Evidence |
|---|---:|---:|---|---:|---:|---|---|
| `ZAI GLM 4.7` | 2.25 | 2.75 | single published per-token table | 2.25 | 2.75 | **correctly_labelled** | `evidence/cerebras_pricing.html` |
| `openai/gpt-oss-120b` | 0.35 | 0.75 | single published per-token table | 0.35 | 0.75 | **correctly_labelled** | `evidence/cerebras_pricing.html` |
| `Google Deepmind Gemma 4 31B` | 0.99 | 1.49 | single published per-token table | 0.99 | 1.49 | **correctly_labelled** | `evidence/cerebras_pricing.html` |

## PAGES I COULD NOT FETCH

None. Every requested primary pricing URL returned HTTP `200` to the raw client. The additional Together model pages, DeepInfra docs page, Nebius public model API, and Nebius JavaScript bundle used during the investigation also returned HTTP `200`.

## THINGS I COULD NOT VERIFY

- Together AI: `Reference` was not present in the current raw pricing body, and the sampled Turbo/Lite/Throughput entries had no identical unsuffixed counterpart from which to compute a current multiplier.
- DeepInfra: the pricing page says tier availability varies by model. The base-price mapping is verified, but this lane did not independently prove that Priority and Flex are enabled for every sampled model.
- Novita AI: the raw page gives a literal `50%` Batch rule and marks batch-capable model records, but it does not print the derived discounted dollar totals. Those totals are intentionally omitted.
- Baseten: the page exposes an exact GLM-5.2/Fast pair, but it does not publish a generic provider-wide Fast multiplier. The Inkling/Inkling-Small collision is a separate-name copy error, not a documented speed-tier contract.
- Nebius AI Studio: no current `fast` or `base` flavor was present. Historical fast/base pricing, if any, is outside what the current official public response can prove.
- Groq: the pricing page states Batch is `50% lower cost` without printing a second per-model batch table.
- Cerebras: account-plan labels are visible, but no alternate per-token prices by account plan are published.
