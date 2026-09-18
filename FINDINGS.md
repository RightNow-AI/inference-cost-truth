# Token billing mechanics

Retrieved on `2026-07-31`. The authoritative machine-readable result is `findings.json`: 25 provider-topic rows backed by raw first-party responses under `evidence/`. Each row records its observed HTTP status and an exact evidence literal; rows that use more than one official page also carry `additional_evidence` records.

## OpenAI

- **Prompt caching:** Offered. The current guide separates GPT-5.6-and-later behavior from earlier models: the newer families document a `1.25×` cache-write rate, a minimum `30m` retention, explicit breakpoints with an implicit default, and a `1024`-token minimum. Earlier in-memory entries are generally retained for `5 to 10 minutes` of inactivity, at most `1 hour`; extended retention can reach `24 hours`. Cache-read price is model-specific rather than one universal percentage.
- **Batch / async:** Offered at `50%` off, with a `24-hour` completion window, up to `50,000` requests, a `200 MB` input file, and one model per file. The Batch guide does not document whether prompt-cache discounts stack.
- **Reasoning tokens:** Billed as output. Raw reasoning is hidden; callers can request summaries. Exact usage paths documented across the APIs are `usage.output_tokens_details.reasoning_tokens` and `usage.completion_tokens_details.reasoning_tokens`. Documented effort values are model-dependent and can include `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, and `max`; GPT-5.6 also documents `standard` and `pro` modes. An official example reports `1186` output tokens, including `1024` reasoning tokens.

## Anthropic

- **Prompt caching:** Offered through automatic caching and explicit breakpoints. Reads cost `0.1×` base input; `5-minute` writes cost `1.25×`; `1-hour` writes cost `2×`. The default `5-minute` TTL refreshes on a hit without an extra write charge. The official minimum table currently says `512` tokens for Claude Opus 5, Claude Fable 5, and Claude Mythos 5; `2,048` for Claude Mythos Preview, Claude Opus 4.7, and Claude Haiku 3.5; `4,096` for Claude Opus 4.6, Claude Opus 4.5, and Claude Haiku 4.5; and `1,024` for the other listed models.
- **Batch / async:** Offered at `50%` off. Most batches finish in less than `1 hour`; unfinished work expires after `24 hours`. Limits are `100,000` requests or `256 MB`, results remain downloadable for `29 days`, and all active models are supported. Prompt caching can stack with Message Batches, but hits are best-effort. `max_tokens` must be at least `1`; a `0`-token cache-prewarm request is unsupported.
- **Reasoning tokens:** Full internal thinking is billed as output, while callers receive a summary or no thinking text; raw chain of thought is not returned. The exact field is `usage.output_tokens_details.thinking_tokens`. Effort settings are `low`, `medium`, `high`, `xhigh`, and `max`, subject to model support; `high` is the documented default. The official worked example reports `348` billed output tokens, of which `312` are thinking tokens.

## Google Gemini

- **Prompt caching:** Offered in implicit and explicit forms. Explicit cache objects default to `1 hour`, and callers can choose the TTL; an implicit-cache TTL is not documented. The current minimum table says `4096` tokens for Gemini 3.5 Flash and Gemini 3.1 Pro Preview, and `2048` for Gemini 2.5 Flash and Gemini 2.5 Pro. Cache-read and storage/write costs are model-specific.
- **Batch / async:** Offered at `50%` of interactive cost with a target turnaround of `24 hours`. Inline payloads must be under `20MB`; input-file batches accept up to `2GB`. The guide explicitly uses `gemini-3.6-flash`, `gemini-embedding-2`, and `gemini-3-pro-image-preview` in examples but sends readers to the Models page for the complete support matrix. Context caching is supported and billed at standard context-caching rates.
- **Reasoning tokens:** Thinking is billed in addition to output; only summaries are exposed. The current Interactions guide uses `interaction.usage.total_thought_tokens`. `thinking_level` supports model-dependent subsets of `minimal`, `low`, `medium`, and `high`. The official streaming example reports `530` total tokens: `62` input, `171` output, and `297` thought tokens.

## xAI

- **Prompt caching:** Offered automatically for all `grok` language models. Cached tokens use a model-specific reduced price. A fixed TTL, minimum prefix length, write surcharge, and extendability rule are not documented; the FAQ says an entry can be evicted at any time because of load or restarts.
- **Batch / async:** Offered. The current pricing page gives a `20%` discount only to `grok-4.3`, `grok-4.20-0309-reasoning`, `grok-4.20-0309-non-reasoning`, and `grok-4.20-multi-agent-0309`; unlisted models receive no batch discount. Eligible input, output, cached, and reasoning tokens receive the discount. Image and video generation remain at standard rates. Most work completes within `24 hours`, but that is best-effort.
- **Reasoning tokens:** Reasoning is billed at the completion-token rate and callers receive a summary. Chat and Responses use `usage.completion_tokens_details.reasoning_tokens` and `usage.output_tokens_details.reasoning_tokens`. The current reasoning guide documents `low`, `medium`, and `high`, plus `xhigh` for multi-agent control; the REST schema also exposes `none` where disabling is supported. An official Chat example reports `32` prompt tokens, `9` completion tokens, `94` reasoning tokens, and `135` total tokens.

## DeepSeek

- **Prompt caching:** Offered automatically as a best-effort disk cache. The current pricing page lists cached-input prices for `deepseek-v4-flash` and `deepseek-v4-pro`. Unused cache is usually cleared within a few hours to a few days. A write surcharge, minimum prefix length, and extendability rule are not documented.
- **Batch / async:** `not documented`. No Batch API or asynchronous batch-processing page was found in the official sitemap or docs navigation. OpenAI-format compatibility was not treated as evidence that OpenAI Batch semantics exist.
- **Reasoning tokens:** Reasoning is a completion-token breakdown and is billed as output. Full reasoning is returned in `reasoning_content`; the exact usage field is `usage.completion_tokens_details.reasoning_tokens`. Thinking defaults to `high`; the guide also documents `none`, `low`, `xhigh`, and `max` through model-specific mappings. No official worked numeric token-count example was found.

## Mistral

- **Prompt caching:** Offered automatically. Cached tokens are billed at `10%` of standard input price. Cache blocks contain `64` tokens, so prompts shorter than `64` tokens cannot hit. TTL, write surcharge, and extendability are not documented.
- **Batch / async:** Offered at `50%` off. `timeout_hours` defaults to `24 hours` and must be below `7 days`; this is a timeout, not a promised completion SLA. A workspace can have `1 million` pending requests, and the page documents no maximum batch-job count. Each batch uses one model and a supported endpoint. Cache-discount stacking is not documented.

## Together AI

- **Prompt caching:** Offered automatically on supported serverless chat models with model-specific cached-input prices. Retention is best-effort and short-lived, with no configurable window. A write surcharge and minimum prefix length are not documented.
- **Batch / async:** Offered at up to `50%` off with a best-effort `24-hour` window. The six listed `50%` models are `meta-llama/Llama-3.3-70B-Instruct-Turbo`, `meta-llama/Llama-3-70b-chat-hf`, `Qwen/Qwen2.5-7B-Instruct-Turbo`, `mistralai/Mixtral-8x7B-Instruct-v0.1`, `zai-org/GLM-4.5-Air-FP8`, and `openai/whisper-large-v3`. The six explicitly unavailable serverless models are `deepseek-ai/DeepSeek-R1`, `deepseek-ai/DeepSeek-V3.1`, `deepseek-ai/DeepSeek-V4-Pro`, `MiniMaxAI/MiniMax-M2.7`, `moonshotai/Kimi-K2.5`, and `moonshotai/Kimi-K2.6`. Limits are `50,000` requests, `100 MB`, and `30B` enqueued tokens per model. Dedicated inference receives no batch discount; cache stacking is not documented.

## Fireworks AI

- **Prompt caching:** Enabled automatically by default. The default cached-token discount is `50%`, but it varies by model. Entries usually remain for at least several minutes and can remain for several hours, depending on model, load, and deployment. Minimum prefix length, write surcharge, and extendability are not documented.
- **Batch / async:** Offered at `50%` off. Prompt caching is automatic in Batch and can add another `50%` saving on cached tokens. Input datasets can be `1GB`; outputs can be `8GB`. Only batch-compatible bases and derivatives are supported. The same page conflicts with itself: it offers `12`, `24`, `48`, and `72` hour expiration windows, then later says jobs expire after `24 hours`.

## DeepInfra

- **Prompt caching:** The official model catalog exposes `rate_per_input_token_cached`, so cached-input billing is offered. No first-party standalone mechanics page was found; the read discount, write surcharge, TTL, extendability, minimum prefix, and automatic/explicit behavior are not documented.
- **Batch / async:** Offered at `20%` off with results returned within `24 hours`; `completion_window` currently accepts only `24h`. Supported endpoints are `/v1/chat/completions`, `/v1/completions`, and `/v1/embeddings`. A file must use one model and endpoint. Limits are `50,000` request lines, `200 MB`, `50,000` embedding inputs, and `100` concurrent batches per user. Cached-input stacking is not documented.

## Groq

- **Prompt caching:** Offered automatically for `openai/gpt-oss-20b`, `openai/gpt-oss-120b`, and `openai/gpt-oss-safeguard-20b`. Cached input receives `50%` off with no added fee. Entries expire after `2 hours` without use. The page gives a model-dependent minimum range of `128` to `1024` tokens rather than a per-model minimum table.
- **Batch / async:** Offered at `50%` off with a selectable window from `24 hours` to `7 days`. Listed chat models are `openai/gpt-oss-20b`, `openai/gpt-oss-120b`, `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, and `meta-llama/llama-guard-4-12b`; transcription lists `whisper-large-v3` and `whisper-large-v3-turbo`, while translation lists `whisper-large-v3`. Files are limited to `50,000` lines and `200MB`. Prompt caching remains active in Batch, but its discount does not stack with the batch rate.

## PAGES I COULD NOT FETCH

| URL | Observed status / symptom | Recovery used |
| --- | --- | --- |
| `https://ai.google.dev/gemini-api/docs/caching` | Repeated HTTP `302` OAuth redirects until curl exhausted its redirect limit. | Saved the official `generate-content/caching.md.txt` response with the DevSite wall cookie; HTTP `200`. |
| `https://ai.google.dev/gemini-api/docs/batch-api` | Repeated HTTP `302` OAuth redirects until curl exhausted its redirect limit. | Saved the official `batch-api.md.txt` response with the DevSite wall cookie; HTTP `200`. |
| `https://ai.google.dev/gemini-api/docs/thinking` | Repeated HTTP `302` OAuth redirects until curl exhausted its redirect limit. | Saved the official `thinking.md.txt` response with the DevSite wall cookie; HTTP `200`. |
| `https://deepinfra.com/llms.txt` | HTTP `404` / holding-page body. | Used canonical `https://docs.deepinfra.com/llms.txt`; HTTP `200`. |
| `https://deepinfra.com/batch/introduction` | HTTP `404` / holding-page body. | Used canonical `https://docs.deepinfra.com/batch/introduction.md`; HTTP `200`. |
| `https://deepinfra.com/batch/introduction.md` | HTTP `404` / holding-page body. | Used canonical `https://docs.deepinfra.com/batch/introduction.md`; HTTP `200`. |
| `https://deepinfra.com/batch/batch-objects` | HTTP `404` / holding-page body. | Used canonical `https://docs.deepinfra.com/batch/batch-objects.md`; HTTP `200`. |
| `https://deepinfra.com/batch/batch-endpoints` | HTTP `404` / holding-page body. | Used canonical `https://docs.deepinfra.com/batch/batch-endpoints.md`; HTTP `200`. |
| `https://deepinfra.com/docs/batch/introduction` | HTTP `200`, but the static response was the docs-root shell (`data-current-path="/"`), not the requested article. | Used canonical `docs.deepinfra.com` Markdown; HTTP `200`. |
| `https://deepinfra.com/docs/batch/batch-objects` | HTTP `200`, but the static response was the docs-root shell, not the requested article. | Used canonical `docs.deepinfra.com` Markdown; HTTP `200`. |
| `https://deepinfra.com/docs/batch/batch-endpoints` | HTTP `200`, but the static response was the docs-root shell, not the requested article. | Used canonical `docs.deepinfra.com` Markdown; HTTP `200`. |
| `https://api-docs.deepseek.com/guides/kv_cache.md` | HTTP `200`, but the `.md` route served the docs shell/home rather than the cache article. | Used the canonical HTML article at `/guides/kv_cache`; HTTP `200`. |

## THINGS I COULD NOT VERIFY

- **DeepSeek Batch:** offering, discount, SLA, limits, model support, and cache stacking are all `not documented` in the official pages and sitemap inspected.
- **DeepInfra prompt-cache mechanics:** only the official cached-input catalog field was verifiable. No official mechanics page established TTL, minimum prefix, write surcharge, or activation mode.
- **Fixed cache properties:** xAI provides no guaranteed TTL or minimum; DeepSeek provides only a broad unused-cache lifetime; Mistral gives no TTL; Together gives no configurable or guaranteed duration; Fireworks gives a broad load-dependent range; Groq gives only a minimum-token range, not a per-model table.
- **Cache-write charges:** no write surcharge was documented for xAI, DeepSeek, Mistral, Together, Fireworks, or DeepInfra.
- **Batch/cache stacking:** OpenAI, Mistral, Together, and DeepInfra do not document whether the discounts stack. Anthropic, Google, Fireworks, and Groq do document the interaction; xAI's pricing page says eligible cached tokens receive the batch discount.
- **Batch model matrices:** OpenAI and Google refer to separate model support pages rather than enumerating a complete list in the Batch guide. Fireworks and Mistral describe compatibility rules without a complete current model-ID list on the page captured.
- **Fireworks Batch SLA:** the official page contains unresolved `12`/`24`/`48`/`72`-hour versus `24`-hour expiration language.
- **xAI reasoning controls:** the reasoning guide describes grok-4.5 with `high` as the default and no disable option, while the REST schema still describes grok-4.3 with `none`/`low`/`medium`/`high` and `low` as default. Both official statements are retained; no inference was used to reconcile them.
- **Worked reasoning counts:** DeepSeek did not provide an official worked numeric usage example. OpenAI's example gives billed output and reasoning counts but not an explicit visible-output token count. Anthropic gives billed output and internal-thinking counts but not the visible summary's token count.
- **Google response shape:** the current official thinking and token-count pages are centered on the Interactions API, so `interaction.usage.total_thought_tokens` is recorded. A separate current `generateContent` thought-token usage field was not stated on those captured pages.
