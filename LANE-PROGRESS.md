# LANE hidden-costs progress

## 2026-07-31 - initialization

- Read `data/providers.json`; its current provider set is OpenAI, Anthropic, Google Gemini, xAI, Mistral, DeepSeek, Together AI, Fireworks AI, DeepInfra, Groq, Cerebras, Baseten, Novita AI, and Nebius AI Studio.
- Mission scope also explicitly includes Cohere and GPU-rental providers RunPod, Lambda, CoreWeave, Vultr, Nebius, Hyperstack, and TensorWave, for 22 provider rows total.
- Evidence schema decision: one row per provider, with aligned arrays for `evidence_file`, `evidence_literal`, `source_url`, and `http_status`, because a provider's ten fields normally require multiple official pages.
- No provider facts have been accepted yet. All unsupported fields will remain the literal string `not documented`.

## 2026-07-31 - first evidence bank

- Saved raw official response bodies for all 22 providers under `evidence/`, including both successful pages and failed/404 attempts.
- Closed-vendor evidence banked for OpenAI, Anthropic, Google Gemini, xAI, Mistral, DeepSeek, and Cohere.
- Hosted-open evidence banked for Together AI, Fireworks AI, DeepInfra, Groq, Cerebras, Baseten, Novita AI, and Nebius AI Studio.
- GPU-rental evidence banked for RunPod, Lambda, CoreWeave, Vultr, Nebius, Hyperstack, and TensorWave.
- Hyperstack documentation pages returned JavaScript shells with no substantive billing text in static HTML. Saved the official route chunks that contain the rendered pricebook and billing prose instead.
- Began literal-only extraction. Confirmed usable evidence for rate-limit/tier, billing, retention/training, SLA, storage/egress, billing-increment, and cold-start claims where the provider publishes them. Unsupported fields remain candidates for the literal value `not documented`.

## 2026-07-31 - final evidence bank and assembly

- Wrote `findings.json` with one row for every mission provider and aligned evidence, URL, and HTTP-status arrays.
- Corrected captured names and limits to the current official response bodies, including a Cerebras model label that differed from an earlier draft.
- Mechanical validation passed: the JSON parses, every required provider is present, all evidence arrays align, every referenced evidence file exists, and every recorded literal is an exact substring of its saved response body.
- Wrote `FINDINGS.md` with provider-grouped findings, transparency conclusions, failed-page symptoms, and explicit unverified gaps.
- No git commands, test runners, commits, pushes, or deploy actions were run.
