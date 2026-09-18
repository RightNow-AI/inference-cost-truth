# Closed-weight vendor API pricing findings

Retrieved on `2026-07-31`. `findings.json` contains **281 evidence-backed rows** across six vendors. Every row has one exact raw-body substring in `evidence_literal`; values that were not literally printed were left `null` rather than calculated.

## Fetch and redirect record

| Requested URL | HTTP status | Effective URL | Saved body |
|---|---:|---|---|
| `https://platform.openai.com/docs/pricing` | 200 | `https://developers.openai.com/api/docs/pricing` | `evidence/openai-platform-pricing.html` |
| `https://openai.com/api/pricing/` | 200 | `https://openai.com/business/pricing/` | `evidence/openai-api-pricing.html` |
| `https://docs.claude.com/en/docs/about-claude/pricing` | 200 | `https://platform.claude.com/docs/en/about-claude/pricing` | `evidence/anthropic-docs-pricing.html` |
| `https://www.anthropic.com/pricing` | 200 | `https://claude.com/pricing` | `evidence/anthropic-pricing.html` |
| `https://ai.google.dev/gemini-api/docs/pricing` | 200 | unchanged | `evidence/google-gemini-pricing.html` |
| `https://docs.x.ai/docs/models` | 200 | `https://docs.x.ai/developers/models` | `evidence/xai-models.html` |
| `https://mistral.ai/pricing` | 200 | `https://mistral.ai/pricing/` | `evidence/mistral-pricing.html` |
| `https://mistral.ai/pricing/api/` (official API-pricing page linked from the supplied page) | 200 | unchanged | `evidence/mistral-api-pricing.html` |
| `https://api-docs.deepseek.com/quick_start/pricing` | 200 | `https://api-docs.deepseek.com/quick_start/pricing/` | `evidence/deepseek-pricing.html` |

## OpenAI

**152 rows; 58 distinct printed model labels.** Coverage includes Standard, Batch, Flex, Fast mode, separate Long context columns, specialized text models, and fine-tuning inference tables.

- General text labels include `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, the printed short-context variants of `gpt-5.5`, `gpt-5.5-pro`, `gpt-5.4`, and `gpt-5.4-pro`, plus `gpt-5.4-mini`, `gpt-5.4-nano`, `gpt-5.2`, `gpt-5.2-pro`, `gpt-5.1`, `gpt-5`, `gpt-5-mini`, `gpt-5-nano`, `gpt-5-pro`, the GPT-4.1/GPT-4o families, o-series models, and the printed legacy GPT-4/GPT-3.5/Davinci/Babbage rows.
- Specialized rows include `chat-latest`, `gpt-5.3-chat-latest`, `gpt-5.2-chat-latest`, `gpt-5.3-codex`, `gpt-5.4-cyber`, `gpt-5.5-cyber`, `gpt-5-search-api`, and `omni-moderation-latest`.
- Fine-tuning inference rows include the printed snapshot, data-sharing, and Legacy labels from both Standard and Batch tables.
- The documented regional-processing uplift and its eligibility date are recorded in notes, but no regional totals were calculated.
- Thirty unique audio/realtime, image, video, transcription, and embedding model entries were counted but excluded from token-text rows.

## Anthropic

**50 rows; 15 distinct printed model labels.** Models: Claude Fable 5, Claude Mythos 5, Claude Opus 5/4.8/4.7/4.6/4.5/4.1/4, Claude Sonnet 5/4.6/4.5/4, and Claude Haiku 4.5/3.5.

- Each Standard price row is represented twice so both separately printed cache-write durations are preserved in `cache_write_per_1m`.
- Batch prices are separate rows. Fast mode rows are included for Claude Opus 5 and Claude Opus 4.8.
- Claude Sonnet 5 has separate rows for introductory pricing through August 31, 2026 and standard pricing starting September 1, 2026.
- The full 1M-token context statement is attached only to the models covered by the page's “Claude 4.6 and later” statement.
- The US inference multiplier is recorded, but multiplied per-model totals were not invented.

## Google Gemini

**58 rows; 17 text-generating or specialized text model headings.** Included: Gemini 3.6 Flash, Gemini 3.5 Flash, Gemini 3.5 Flash-Lite, Gemini 3.1 Flash-Lite, Gemini Omni Flash Preview, Gemini 3.1 Pro Preview, Gemini 3 Flash Preview, Gemini 2.5 Pro, Gemini 2.5 Flash, Gemini 2.5 Flash-Lite, Gemini 2.5 Flash-Lite Preview, Gemini 2.0 Flash, Gemini 2.0 Flash-Lite, Gemini Robotics ER 2 Preview, Gemini Robotics ER 2 Streaming Preview, Gemini Robotics ER 1.6 Preview, and Gemini 2.5 Computer Use Preview.

- Standard, Batch, Flex, and Priority are separate rows where the page lists them.
- Every printed `<= 200k` and `> 200k` price tier is a separate row.
- When a cell lists text and other modalities, only the text token price is placed in the requested token fields.
- Eighteen non-text/open-unpriced headings were not turned into text-model rows: live/audio, image, TTS, Imagen, Veo, Lyria, embedding, and Gemma sections.

## xAI

**1 row; 1 text model.** The current models catalog prints one text-model card: `Grok 4.5`, including input, output, context, and configurable reasoning. Voice API and Imagine API were counted as non-text cards.

## Mistral

**18 rows; 18 text or classifier model cards.** Included: Mistral Medium 3.5, Mistral Small 4, Mistral Large 3, Devstral 2, Devstral Small 2, Codestral, Leanstral, Magistral Medium, Magistral Small, Ministral 3 in 3B/8B/14B sizes, Classifier API model 3B/8B, Mistral Moderation, Mistral NeMo, Mixtral 8x7B, and Mixtral 8x22B.

- The supplied `/pricing` page is a plans page; its official `/pricing/api/` link contains the full API card grid.
- Rows that the page labels or describes as open were retained and explicitly marked, because the mission also requires exhaustive page coverage.
- The page advertises global Batch and cached-input discounts but does not print literal discounted per-model amounts. Those fields remain `null`.
- Fifteen other unique cards were excluded: seven audio/OCR/embedding models, seven tool cards, and one Enterprise APIs service card.

## DeepSeek

**2 rows; 2 models.** `deepseek-v4-flash` and `deepseek-v4-pro` include literal cache-hit, cache-miss, output, 1M context, and thinking-mode evidence from the same raw table.

## PAGES I COULD NOT FETCH

None. Every supplied URL returned HTTP 200 after redirects. The OpenAI marketing URL fetched successfully but landed on a business/ChatGPT pricing page rather than an API token-pricing table.

## THINGS I COULD NOT VERIFY

- Exact per-model regional totals for OpenAI and Anthropic: their pages print an uplift/multiplier, not the resulting token prices. No arithmetic-derived prices were reported.
- Literal per-model Batch and cached-input amounts for Mistral: only global discount rules are printed, so the requested numeric fields are `null`.
- Maximum context windows for OpenAI, Google Gemini, and Mistral models where the pricing page did not state them. Pricing thresholds were not misrepresented as maximum windows.
- Reasoning status where a page only priced output/thinking tokens but did not explicitly classify the model. `is_reasoning_model` remains `null` in those cases.
- Whether Mistral rows labeled Open should ultimately be filtered by the orchestrator's closed-weight scope. They are included and flagged so no pricing-page model silently disappears.
- Any API-model data from `https://openai.com/api/pricing/`; on retrieval it redirected to `https://openai.com/business/pricing/` and exposed business-plan pricing instead.

