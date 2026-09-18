# LANE pricing-closed progress

## 2026-07-31 initial checkpoint

- Confirmed worktree: `C:/Users/jaber/RightNow-Full/ict-pricing-closed`.
- Read the repository README; no `AGENTS.md` was present in the worktree.
- Preserved pre-existing `evidence/probe-gemini.html` untouched.
- Next: fetch every supplied official URL with redirects and a browser user-agent, saving raw response bodies and recording observed status/effective URL.

## 2026-07-31 fetch checkpoint

- Saved raw final response bodies under `evidence/` for all eight supplied URLs.
- Observed redirects/statuses:
  - OpenAI docs: `200`, landed at `https://developers.openai.com/api/docs/pricing`.
  - OpenAI marketing pricing: `200`, landed at `https://openai.com/business/pricing/` (not an API price table).
  - Anthropic docs: `200`, landed at `https://platform.claude.com/docs/en/about-claude/pricing`.
  - Anthropic marketing pricing: `200`, landed at `https://claude.com/pricing`.
  - Google Gemini: `200`, stayed at the supplied URL.
  - xAI: `200`, landed at `https://docs.x.ai/developers/models`.
  - Mistral: `200`, normalized to trailing slash.
  - DeepSeek: `200`, normalized to trailing slash.
- Static bodies contain price data for OpenAI docs, Anthropic docs, Gemini, xAI, and DeepSeek. Mistral's visible static HTML currently exposes only a pricing example; its full API model grid needs underlying-data investigation. The redirected OpenAI marketing page is business/ChatGPT pricing rather than the API table.

## 2026-07-31 extraction checkpoint

- Found Mistral's dedicated first-party API page linked from the supplied pricing page: `https://mistral.ai/pricing/api/`.
- Fetched it with raw curl: `200`, effective URL unchanged, saved as `evidence/mistral-api-pricing.html`.
- Confirmed the current source pages expose substantially changed lineups, so no remembered model names or prices are being used.
- Extraction plan now covers:
  - OpenAI Standard, Batch, Flex, Fast mode, separate long-context columns, specialized text models, and fine-tuning inference rows.
  - Anthropic base prices, both cache-write durations, Batch, Fast mode, dated Sonnet 5 introductory/standard tiers, and the documented US inference multiplier without inventing multiplied totals.
  - Gemini Standard, Batch, Flex, Priority, and both sides of every printed 200k pricing threshold for the text-generating/specialized text models.
  - xAI's one text-model card on the current catalog page.
  - Mistral text-model/API cards, including rows labeled Open for exhaustiveness, while separating audio/OCR/embedding/tool cards in the summary.
  - DeepSeek's two current model columns with cache-hit, cache-miss, output, context, and thinking-mode evidence.

## 2026-07-31 final checkpoint

- Wrote `findings.json`: 281 rows total.
  - OpenAI: 152
  - Anthropic: 50
  - Google Gemini: 58
  - xAI: 1
  - Mistral: 18
  - DeepSeek: 2
- Wrote `FINDINGS.md` with provider summaries, the full redirect/status record, non-text exclusions, and mandatory uncertainty sections.
- Independent closeout validation passed:
  - all 281 `evidence_literal` values are exact substrings of their referenced saved response bodies;
  - every non-null price field's decimal string occurs inside that row's literal;
  - every non-null context-window string occurs inside that row's literal;
  - all rows have the exact requested schema and retrieval metadata;
  - every null cached-input field has a `not documented` explanation in notes.
- No calculated regional, Batch, or cache prices were inserted when the resulting number was not literally printed by the vendor.

