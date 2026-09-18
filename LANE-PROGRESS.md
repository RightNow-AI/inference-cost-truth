# Lane Progress

## 2026-07-31 initial checkpoint

- Confirmed workspace root: `C:/Users/jaber/RightNow-Full/ict-pricing-hosted`.
- Read-only convention check found only the lane README and no existing findings/evidence artifacts.
- Beginning raw `curl.exe -L` capture for all supplied official URLs; no git or test commands will be run.

## 2026-07-31 raw-page checkpoint

- Saved HTTP 200 response bodies for Together, Fireworks, DeepInfra, Groq, both Cerebras URLs, Baseten, Novita, and both Nebius URLs under `evidence/`.
- Redirect observed: `https://studio.nebius.com/pricing` resolved to `https://tokenfactory.nebius.com/pricing` (HTTP 200, 6,716 bytes).
- The static HTML already contains pricing tables for Together, DeepInfra, Groq, and Novita.
- Fireworks' main page contains dedicated GPU pricing but points model-specific serverless pricing to official docs; that docs page will be captured next.
- Cerebras, Baseten, and Nebius need deeper static/embedded-data or official-endpoint inspection before any numeric row is trusted.

## 2026-07-31 final extraction checkpoint

- Saved 96 raw response bodies under `evidence/`, covering the supplied pages, official pricing/docs endpoints, Together model detail pages, and Novita JavaScript bundles.
- Generated `findings.json` with 305 evidence-backed rows: 257 serverless per-token rows and 48 dedicated GPU-hour rows across all eight providers.
- Generated `FINDINGS.md` with provider summaries, 95 observed URL/status entries, fetch failures, and explicit unverifiable items.
- Mechanical audit passed: zero missing required fields, zero missing evidence literals, zero evidence-file substring misses, and zero reported numeric/quantization values absent from their row's evidence literal.
- Remaining honest gaps: exact batch dollar values when only a discount rule is published; Cerebras GLM/Gemma context and quantization; Groq/Cerebras GPU-hour rates; normalized Novita dedicated rates whose API exposes only encoded price/precision integers.
