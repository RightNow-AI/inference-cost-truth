# Long-context pricing thresholds

Retrieved on 2026-07-31. This report uses only raw first-party responses saved under `evidence/`. Prices and thresholds preserve the vendor's literal formatting; no multiplier is calculated unless the vendor explicitly prints it.

`findings.json` contains 34 evidence-backed tier rows. Of those, 30 publish an exact numeric cutoff, 32 publish the requested per-1M-token input/output prices, and 28 contain both an exact cutoff and the requested price units. The exceptions are four Azure short/long rows without a numeric cutoff and two legacy Vertex rows priced in non-token units.

## Vendors with long-context tiers

| Provider | Rows | What is documented | Whole-request rule |
|---|---:|---|---|
| OpenAI | 7 | `272K`; Standard service-tier short/long prices | Full request/session for 6 rows; GPT-5.5 Pro not documented |
| Google Gemini Developer API | 3 | `200k` prompt bands in the paid Standard tier | Not documented |
| Google Vertex AI | 9 | `200K` for current Gemini/Claude/Grok rows; `128K` for two legacy Gemini rows | All tokens are repriced |
| xAI | 6 | `200k` prompt threshold | All tokens in the request are repriced |
| Novita AI | 3 | Input-length bands at `524,288`, `32,768`, and `131,072` | Not documented |
| Azure OpenAI | 6 | Exact `272k` cutoff for GPT-5.4 and GPT-5.4 Pro; four other models only label short/long context | Not documented |

### Evidence-backed model rows

| Provider | Model | Cutoff | Below input/output | Above input/output | Scope | Evidence |
|---|---|---:|---|---|---|---|
| OpenAI | gpt-5.6-sol | 272K | $5.00 / $30.00 | $10.00 / $45.00 | whole request | `evidence/openai-pricing-md.txt` |
| OpenAI | gpt-5.6-terra | 272K | $2.00 / $12.00 | $4.00 / $18.00 | whole request | `evidence/openai-pricing-md.txt` |
| OpenAI | gpt-5.6-luna | 272K | $0.20 / $1.20 | $0.40 / $1.80 | whole request | `evidence/openai-pricing-md.txt` |
| OpenAI | gpt-5.5 | 272K | $5.00 / $30.00 | $10.00 / $45.00 | whole session | `evidence/openai-pricing-md.txt` |
| OpenAI | gpt-5.4 | 272K | $2.50 / $15.00 | $5.00 / $22.50 | whole session | `evidence/openai-pricing-md.txt` |
| OpenAI | gpt-5.4-pro | 272K | $30.00 / $180.00 | $60.00 / $270.00 | whole session | `evidence/openai-pricing-md.txt` |
| OpenAI | gpt-5.5-pro | 272K | $30.00 / $180.00 | $60.00 / $270.00 | not documented | `evidence/openai-pricing-md.txt` |
| Google Gemini Developer API | Gemini 3.1 Pro Preview | 200k | $2.00 / $12.00 | $4.00 / $18.00 | not documented | `evidence/google-gemini-pricing-mdtxt-googlebot.txt` |
| Google Gemini Developer API | Gemini 2.5 Pro | 200k | $1.25 / $10.00 | $2.50 / $15.00 | not documented | `evidence/google-gemini-pricing-mdtxt-googlebot.txt` |
| Google Gemini Developer API | Gemini 2.5 Computer Use Preview | 200k | $1.25 / $10.00 | $2.50 / $15.00 | not documented | `evidence/google-gemini-pricing-mdtxt-googlebot.txt` |
| Google Vertex AI | Gemini 3.1 Pro Preview | 200K | $2 / $12 | $4 / $18 | whole request | `evidence/google-vertex-pricing.html` |
| Google Vertex AI | Gemini 2.5 Pro | 200K | $1.25 / $10 | $2.50 / $15 | whole request | `evidence/google-vertex-pricing.html` |
| Google Vertex AI | Gemini 2.5 Pro Computer Use-Preview | 200K | $1.25 / $10.00 | $2.5 / $15.00 | whole request | `evidence/google-vertex-pricing.html` |
| Google Vertex AI | Claude Sonnet 4.5 | 200K | $3.00 / $15.00 | $6.00 / $22.50 | whole request | `evidence/google-vertex-pricing.html` |
| Google Vertex AI | Grok 4.20 Reasoning | 200K | $1.25 / $2.50 | $2.50 / $5.00 | whole request | `evidence/google-vertex-pricing.html` |
| Google Vertex AI | Grok 4.20 Non-Reasoning | 200K | $1.25 / $2.50 | $2.50 / $5.00 | whole request | `evidence/google-vertex-pricing.html` |
| Google Vertex AI | Grok 4.3 | 200K | $1.25 / $2.50 | $2.50 / $5.00 | whole request | `evidence/google-vertex-pricing.html` |
| Google Vertex AI | Gemini 1.5 Flash | 128K | not published per 1M tokens | not published per 1M tokens | whole request | `evidence/google-vertex-pricing.html` |
| Google Vertex AI | Gemini 1.5 Pro | 128K | not published per 1M tokens | not published per 1M tokens | whole request | `evidence/google-vertex-pricing.html` |
| xAI | Grok 4.20 | 200k | $1.25 / $2.50 | $2.50 / $5.00 | whole request | `evidence/xai-grok-4-20-md.txt` |
| xAI | Grok 4.20 (Non-Reasoning) | 200k | $1.25 / $2.50 | $2.50 / $5.00 | whole request | `evidence/xai-grok-4-20-non-reasoning-md.txt` |
| xAI | Grok 4.20 Multi-Agent Beta | 200k | $1.25 / $2.50 | $2.50 / $5.00 | whole request | `evidence/xai-grok-4-20-multi-agent-md.txt` |
| xAI | Grok 4.3 | 200k | $1.25 / $2.50 | $2.50 / $5.00 | whole request | `evidence/xai-grok-4-3-md.txt` |
| xAI | Grok 4.5 | 200k | $2.00 / $6.00 | $4.00 / $12.00 | whole request | `evidence/xai-grok-4-5-md.txt` |
| xAI | Grok Build 0.1 | 200k | $1.00 / $2.00 | $2.00 / $4.00 | whole request | `evidence/xai-grok-build-0-1-md.txt` |
| Novita AI | MiniMax M3 | 524,288 | $0.3 / $1.2 | $0.6 / $2.4 | not documented | `evidence/novita-minimax-m3.html` |
| Novita AI | Qwen3 Max | 32,768 | $0.845 / $3.38 | $1.4 / $5.64 | not documented | `evidence/novita-qwen3-max.html` |
| Novita AI | Qwen3 Max | 131,072 | $1.4 / $5.64 | $2.11 / $8.45 | not documented | `evidence/novita-qwen3-max.html` |
| Azure OpenAI | GPT-5.6-sol | not documented | 5.0 / 30.0 | 10.0 / 45.0 | not documented | `evidence/azure-openai-pricing.html` |
| Azure OpenAI | GPT-5.6-terra | not documented | 2.5 / 15.0 | 5.0 / 22.5 | not documented | `evidence/azure-openai-pricing.html` |
| Azure OpenAI | GPT-5.6-luna | not documented | 1.0 / 6.0 | 2.0 / 9.0 | not documented | `evidence/azure-openai-pricing.html` |
| Azure OpenAI | GPT-5.5 | not documented | 5.0 / 30.0 | 10.0 / 45.0 | not documented | `evidence/azure-openai-pricing.html` |
| Azure OpenAI | GPT-5.4 | 272k | 2.5 / 15.0 | 5.0 / 22.5 | not documented | `evidence/azure-openai-pricing.html` |
| Azure OpenAI | GPT-5.4 Pro | 272k | 30.0 / 180.0 | 60.0 / 270.0 | not documented | `evidence/azure-openai-pricing.html` |

The exact character-for-character evidence substring for every row is stored in its `evidence_literal`; split-source rows also carry `above_evidence_literal`, `threshold_evidence_literal`, and `rule_evidence_literal`.

## Vendors without a documented long-context price tier on the captured page

| Provider | Result | Primary raw evidence | HTTP |
|---|---|---|---:|
| Anthropic | Current direct pricing says the full one-million-token window is at standard pricing. | `evidence/anthropic-pricing-md.txt` | 200 |
| Mistral | No token-count pricing threshold found. | `evidence/mistral-api-pricing.html` | 200 |
| DeepSeek | No token-count pricing threshold found. | `evidence/deepseek-pricing.html` | 200 |
| Cohere | No token-count pricing threshold found. | `evidence/cohere-pricing.html` | 200 |
| Amazon Bedrock | NOT_IN_STATIC_HTML for numeric prices; no long-context threshold term found in the page or the two official metered-unit JSON payloads. | `evidence/amazon-bedrock-metered.json` | 200 |
| Together AI | No token-count pricing threshold found. | `evidence/together-pricing.html` | 200 |
| Fireworks AI | No token-count pricing threshold found. | `evidence/fireworks-docs-pricing.html` | 200 |
| DeepInfra | No token-count pricing threshold found. | `evidence/deepinfra-pricing.html` | 200 |
| Nebius AI Studio | No token-count pricing threshold found. | `evidence/nebius-models-info.json` | 200 |
| Baseten | No token-count pricing threshold found. | `evidence/baseten-pricing.html` | 200 |
| Groq | No token-count pricing threshold found. | `evidence/groq-pricing.html` | 200 |
| Cerebras | No token-count pricing threshold found. | `evidence/cerebras-pricing.html` | 200 |

Absence means "not documented on the captured first-party pricing/model surface," not a claim that a private contract can never contain such a term.

## Whole-request versus marginal-token rule

- OpenAI: full request/session for GPT-5.6 Sol/Terra/Luna, GPT-5.5, GPT-5.4, and GPT-5.4 Pro. GPT-5.5 Pro: not documented.
- Gemini Developer API: not documented.
- Vertex AI: all tokens are charged at long-context rates for every included Vertex row.
- xAI: all tokens in the request are charged at the higher rate.
- Novita AI: not documented.
- Azure OpenAI: not documented.

Exact vendor sentences and their source files are stored per row in `billing_scope_quote` / `rule_evidence_literal`.

## Regional and data-residency pricing

### OpenAI

Applies a published uplift to eligible data-residency models released on or after the stated date.

- Evidence file: `evidence/openai-pricing-md.txt`
- Evidence literal:

```text
Regional processing (data residency) endpoints are charged a 10% uplift for models released on or after March 5, 2026, that are eligible for data residency. See our [Your data](https://developers.openai.com/api/docs/guides/your-data) guide for supported regions and processing details. [OpenAI models in Amazon Bedrock](https://developers.openai.com/api/docs/guides/amazon-bedrock) are billed through AWS and may differ from direct OpenAI pricing. Priority processing was renamed Fast mode on July 30, 2026. You can use either `service_tier: "priority"` or `service_tier: "fast"` in your API requests. [Learn more about Fast mode](https://developers.openai.com/api/docs/guides/fast-mode).
```

### Anthropic / partner platforms

- Partner regional and multi-region endpoints for Claude 4.5 models and beyond carry the documented premium.
  - Evidence file: `evidence/anthropic-pricing-md.txt`
  - Evidence literal:

```text
**Regional and multi-region endpoint pricing for Claude 4.5 models and beyond**

  Starting with Claude Sonnet 4.5, Haiku 4.5, and Opus 4.5:

  * **Bedrock** offers two endpoint types: global endpoints (dynamic routing for maximum availability) and regional endpoints (guaranteed data routing through specific geographic regions).
  * **Google Cloud** offers three endpoint types: global endpoints, multi-region endpoints (dynamic routing within a geographic area), and regional endpoints.

  Regional and multi-region endpoints include a 10% premium over global endpoints. The Claude API (first-party) is global by default; for first-party data residency options and pricing, see [Data residency pricing](#data-residency-pricing).
```
- Direct Claude API / Claude Platform on AWS US-only inference, plus Microsoft Foundry US Data Zone Standard, uses the documented multiplier for Claude 4.6 and later.
  - Evidence file: `evidence/anthropic-pricing-md.txt`
  - Evidence literal:

```text
For Claude 4.6 and later models, specifying US-only inference through the `inference_geo` parameter incurs a 1.1x multiplier on all token pricing categories, including input tokens, output tokens, cache writes, and cache reads. Global routing (the default) uses standard pricing.
```

### Mistral

The page bundles regional data-processing controls into Enterprise APIs; it does not map the surcharge to individual models or isolate the regional-control component.

- Evidence file: `evidence/mistral-api-pricing.html`
- Evidence literal:

```text
Introducing our Enterprise APIs, including regional data processing controls, system-level SLAs, increased rate limits, and premium support. This service is available for 75% above list pricing on select APIs.
```

### Google Vertex AI

The captured Standard table lists distinct Global and Non-global rates for Gemini 3.5 Flash, Gemini 3.5 Flash-Lite, and Gemini 3.1 Flash-Lite. The page does not state a universal percentage; the raw row literals are preserved below.

- Evidence file for all four literals: `evidence/google-vertex-pricing.html`
- Gemini 3.5 Flash evidence literal:

```html
<tr>
            <td rowspan="3">Gemini 3.5 Flash</td>
          </tr>
          <tr>
            <td>Input (text, image, video, audio)</td>
            <td>$1.50 (Global)<br><br>$1.65 (Non-global)*</td>
            <td>$1.50 (Global)<br><br>$1.65 (Non-global)*</td>
            <td>$0.15 (Global)<br><br>$0.165 (Non-global)*</td>
            <td>$0.15 (Global)<br><br>$0.165 (Non-global)*</td>
          </tr>
          <tr>
            <td>Text output (response and reasoning)</td>
            <td>$9.00 (Global)<br><br>$9.90 (Non-global)*</td>
            <td>$9.00 (Global)<br><br>$9.90 (Non-global)*</td>
            <td>N/A</td>
            <td>N/A</td>
          </tr>
```
- Gemini 3.5 Flash-Lite evidence literal:

```html
<tr>
            <td rowspan="3">Gemini 3.5 Flash-Lite</td>
          </tr>
          <tr>
            <td>Input (text, image, video, audio)</td>
            <td>$0.3 (Global)<br><br>$0.33 (Non-global)*</td>
            <td>$0.3 (Global)<br><br>$0.33 (Non-global)*</td>
            <td>$0.03 (Global)<br><br>$0.033 (Non-global)*</td>
            <td>$0.03 (Global)<br><br>$0.033 (Non-global)*</td>
          </tr>
          <tr>
            <td>Text output (response and reasoning)</td>
            <td>$2.5 (Global)<br><br>$2.75 (Non-global)*</td>
            <td>$2.5 (Global)<br><br>$2.75 (Non-global)*</td>
            <td>N/A</td>
            <td>N/A</td>
          </tr>
```
- Gemini 3.1 Flash-Lite evidence literal:

```html
<tr>
            <td rowspan="4">Gemini 3.1 Flash-Lite</td>
          </tr>
          <tr>
            <td>Input (text, image, video)</td>
            <td>$0.25 (Global)<br><br>$0.275 (Non-global)*</td>
            <td>$0.25 (Global)<br><br>$0.275 (Non-global)*</td>
            <td>$0.025 (Global)<br><br>$0.0275 (Non-global)*</td>
            <td>$0.025 (Global)<br><br>$0.0275 (Non-global)*</td>
          </tr>
          <tr>
            <td>Input (audio)</td>
            <td>$0.5 (Global)<br><br>$0.55 (Non-global)*</td>
            <td>$0.5 (Global)<br><br>$0.55 (Non-global)*</td>
            <td>$0.05 (Global)<br><br>$0.055 (Non-global)*</td>
            <td>$0.05 (Global)<br><br>$0.055 (Non-global)*</td>
          </tr>
          <tr>
            <td>Text output (response and reasoning)</td>
            <td>$1.5 (Global)<br><br>$1.65 (Non-global)*</td>
            <td>$1.5 (Global)<br><br>$1.65 (Non-global)*</td>
            <td>N/A</td>
            <td>N/A</td>
          </tr>
```
- Effective-date evidence literal:

```html
<p><small>* For non-global endpoints, pricing will go into effect for the Generally available Gemini 3 and later families of models on July 1, 2026. Before July 1, 2026, Global endpoint pricing applies to Non-global endpoints.<br>* If a query input context is longer than 200K tokens, all tokens (input and output) are charged at long context rates.<br>
```

### Azure OpenAI

Azure embeds per-region matrices. For GPT-5.5 Long Context Data Zone, the same deployment row has differing regional input and output values. No universal percentage or qualifying-condition sentence was documented on the captured page, so none is inferred.

- Evidence file: `evidence/azure-openai-pricing.html`
- Deployment-row label evidence literal:

```text
GPT-5.5 Long Context Data Zone
```
- Input evidence literal:

```text
"australia-east":12.0,"central-india":12.0,"us-central":11.0
```
- Output evidence literal:

```text
"australia-east":54.0,"central-india":54.0,"us-central":49.5
```

### Other checked providers

No numeric regional/data-residency price differential was documented on the captured first-party pricing surfaces for direct Gemini API, xAI, DeepSeek, Cohere, Together, Fireworks, DeepInfra, Novita, Nebius, Baseten, Groq, or Cerebras. Amazon Bedrock is covered by Anthropic's documented partner-endpoint rule for applicable Claude models; the captured AWS page/JSON did not independently expose a universal percentage sentence.

## PAGES I COULD NOT FETCH

| URL | Observed status/symptom | Saved evidence |
|---|---|---|
| `https://ai.google.dev/gemini-api/docs/pricing` | Repeated HTTP 302 redirects until curl reached its 50-redirect limit; no body. | `evidence/google-gemini-pricing.headers.txt` |
| `https://ai.google.dev/gemini-api/docs/pricing?hl=en` | Repeated HTTP 302 redirects until the redirect limit; no body. | `evidence/google-gemini-pricing-hl.headers.txt` |
| `https://ai.google.dev/gemini-api/docs/pricing?hl=en&authuser=0` | Repeated HTTP 302 redirects until the redirect limit; no body. | `evidence/google-gemini-pricing-authuser.headers.txt` |
| `https://ai.google.dev/gemini-api/docs/pricing.md` | Repeated HTTP 302 redirects until the redirect limit; no body. | `evidence/google-gemini-pricing-md.headers.txt` |
| `https://ai.google.dev/gemini-api/docs/pricing.md.txt` | Normal browser user agent repeated HTTP 302 redirects; the Googlebot-user-agent fetch of this same URL returned HTTP 200 and is the row source. | `evidence/google-gemini-pricing-mdtxt.headers.txt` |
| `https://ai.google.dev/pricing` | Repeated HTTP 302 redirects until the redirect limit; no body. | `evidence/google-ai-pricing.headers.txt` |
| `https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/bedrock/bedrock/USD/current/bedrock.json` | HTTP 404 for the first inferred path. The bundle-derived path without the duplicated segment returned HTTP 200. | `evidence/amazon-bedrock-metered-badpath.headers.txt` |
| `https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/bedrockfoundationmodels/bedrockfoundationmodels/USD/current/bedrockfoundationmodels.json` | HTTP 404 for the first inferred path. The bundle-derived path without the duplicated segment returned HTTP 200. | `evidence/amazon-bedrock-foundationmodels-metered-badpath.headers.txt` |

## THINGS I COULD NOT VERIFY

- Azure OpenAI: the numeric cutoff for GPT-5.6 Sol, GPT-5.6 Terra, GPT-5.6 Luna, and GPT-5.5. The page only labels short/long context rows.
- Azure OpenAI: whether the higher long-context rate applies to the whole request or only marginal tokens for every listed Azure row.
- Gemini Developer API: whether crossing the prompt boundary reprices the whole request or only marginal tokens.
- Novita AI: whether crossing an input-length band reprices the whole request or only marginal tokens.
- OpenAI GPT-5.5 Pro: whole-request versus marginal scope and explicit multiplier wording. The rate table is present, but the model page omits the rule found on the neighboring models.
- Google Vertex AI legacy Gemini 1.5 Flash and Gemini 1.5 Pro: per-1M-token prediction prices. The page publishes image, second, and character units instead, so the requested token-unit fields are null.
- Azure OpenAI and Google Vertex AI: a universal regional percentage. Both pages expose differing regional prices, but the captured text does not state one universal percentage, so no percentage was calculated.
- Mistral: which individual models/select APIs receive the Enterprise API bundle containing regional data-processing controls.

No unverified number was substituted for any of these gaps.
