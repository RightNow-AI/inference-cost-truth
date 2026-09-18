# pricing-fill lane progress

## 2026-07-31 checkpoint 1

- Read `data/providers.json` before collection.
- Existing closed-vendor counts confirmed: OpenAI 152, Google Gemini 58, Anthropic 50, Mistral 18, DeepSeek 2, xAI 1.
- No existing rows found for Cohere, AI21, Amazon Bedrock, Azure OpenAI, Google Vertex AI, Reka, or Perplexity.
- Starting raw official-source capture under `evidence/`; no git or test commands will be run.

## 2026-07-31 checkpoint 2

- Saved raw HTTP 200 bodies for xAI pricing/models, DeepSeek pricing, Cohere pricing/docs, AI21 pricing/docs, Amazon Bedrock, Azure OpenAI, Google Vertex AI, Reka pricing/models, and Perplexity pricing/model pages.
- xAI static HTML contains a first-party embedded model/pricing payload and a rendered per-1M-token table. It currently exposes six text models in the US region, with separate short/long-context prices and model-specific batch-discount metadata.
- DeepSeek static HTML currently lists exactly `deepseek-v4-flash` and `deepseek-v4-pro`, both with a 1M context length. The page says a future peak/off-peak policy is not yet effective; it prints a future 2x peak multiplier rather than a current off-peak discount.
- Cohere's current pricing payload contains paid text-generation cards for Command R and Command R7B, plus official FAQ prices for legacy/current named Command and Aya variants. Detailed model pages are still being checked before rows are emitted.
- AI21's pricing page directly prints Jamba Mini and Jamba Large per-1M input/output prices.

## 2026-07-31 checkpoint 3

- Captured the official AWS pricing JSON endpoints used by the Bedrock page, including the compressed raw responses and decoded bodies. The endpoint returned HTTP 200, but many Bedrock HTML cells are arithmetic placeholders whose per-1M result does not literally occur in any single raw response; those rows will not be invented.
- Confirmed direct, static per-1M rows on the Bedrock page for several additional model owners; only rows whose complete reported prices are literal in the saved HTML will be emitted.
- Confirmed official static pricing tables for Reka and Perplexity, and a large region-addressable Azure OpenAI pricing payload. Azure rows will consistently use East US where a regional value is required.
- Began mechanical row construction and literal-substring validation. Every emitted evidence literal will be checked against its saved evidence file before finalizing.

## 2026-07-31 checkpoint 4 - final

- Wrote `findings.json` and `FINDINGS.md`.
- Final evidence-backed row count: 321 across xAI, DeepSeek, Cohere, AI21, Amazon Bedrock, Azure OpenAI, Google Vertex AI, Reka, and Perplexity.
- Tier split is preserved in separate rows where literal prices exist: standard, batch, flex, fast (Azure Priority Processing), and provisioned.
- Mechanical integrity checks passed: exact 17-field schema, allowed service tiers only, retrieval date fixed to `2026-07-31`, HTTP status recorded as observed, every evidence literal found in its evidence file, and every non-null token-price value found literally inside its row's evidence literal.
- Honest gaps are documented in `FINDINGS.md`, especially AWS arithmetic placeholders, xAI derived batch/priority prices, DeepSeek's future-only peak policy and non-literal UTC conversion, character-priced Vertex legacy rows, and unpublished Cohere production token prices.
