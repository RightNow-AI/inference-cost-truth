# Lane progress: context-pricing

## 2026-07-31 initial checkpoint

- Confirmed writable worktree: `C:/Users/jaber/RightNow-Full/ict-context-pricing`.
- Ran no git commands and no test runners.
- Existing repo data will be used only to locate official vendor URLs; no existing price, model, threshold, or specification will be reused as a factual finding.
- Next: fetch raw first-party pricing/docs responses into `evidence/`, recording HTTP status for every attempted URL.

## 2026-07-31 raw-fetch checkpoint 1

- Saved raw first-party bodies and response headers for OpenAI, Anthropic, Google Vertex AI, xAI, Mistral, DeepSeek, Cohere, Amazon Bedrock, Azure OpenAI, Together, Fireworks, DeepInfra, Novita, Nebius, Baseten, Groq, and Cerebras.
- Those primary fetches returned final HTTP `200`.
- `https://ai.google.dev/gemini-api/docs/pricing` did not yield a body: `curl.exe -L` hit the 50-redirect limit while the site repeatedly attempted automatic OAuth sign-in. Saved the observed redirect headers as `evidence/google-gemini-pricing.headers.txt`; continuing with alternate official Google fetch forms/endpoints.
- No pricing facts have yet been promoted into output rows. Extraction and literal validation are next.

## 2026-07-31 raw-fetch checkpoint 2

- Recovered the official Gemini Developer API pricing body with a Googlebot user agent from `https://ai.google.dev/gemini-api/docs/pricing.md.txt`; saved the unmodified HTTP `200` body as `evidence/google-gemini-pricing-mdtxt-googlebot.txt` and its headers beside it. The ordinary browser-user-agent variants remained trapped in OAuth redirect loops and their headers were retained.
- Saved clean official markdown for the OpenAI pricing page, seven OpenAI model pages, the Anthropic pricing page, and six xAI model pages. These pages provide the exact pricing rows and the vendor wording for whole-request versus undocumented scope.
- Saved individual official Novita model pages for the two models whose main pricing payload marks tiered billing.
- Working tier inventory: OpenAI, Gemini Developer API, Google Vertex AI, xAI, Novita, and Azure OpenAI. Azure exposes four short/long-context price pairs without a numeric cutoff; those will be reported as incomplete, not inferred.
- Regional/data-residency evidence found so far: OpenAI `10%`, Anthropic partner endpoints `10%` plus direct/Foundry `1.1x`, Mistral Enterprise APIs `75% above list pricing`, and explicit region matrices on Vertex AI and Azure without a single documented universal percentage.
- Extraction is now being converted into JSON rows, with every evidence literal checked against its saved raw body before release.

## 2026-07-31 final checkpoint

- Wrote `findings.json` with 34 evidence-backed tier rows across OpenAI, Gemini Developer API, Google Vertex AI, xAI, Novita AI, and Azure OpenAI.
- Independent literal validation passed with zero failures: every populated below/above price and every documented threshold appears in the corresponding exact substring, and every stored substring appears byte-for-byte in its declared evidence file.
- 30 rows have an exact numeric cutoff. Four Azure rows expose short/long prices without a numeric cutoff and are marked `not documented`.
- 32 rows have the requested per-1M-token input/output prices. Two legacy Vertex Gemini rows retain real 128K thresholds but publish modality/character units, so their per-1M-token fields are null rather than converted.
- Wrote `FINDINGS.md`, grouped by provider, with the mandatory `PAGES I COULD NOT FETCH` and `THINGS I COULD NOT VERIFY` sections, whole-request-versus-marginal findings, and regional/data-residency evidence.
- Recovered Amazon Bedrock's official metered-unit JSON endpoints by inspecting the raw first-party pricing bundle after the static page exposed token placeholders. Neither official JSON payload documented a long-context threshold.
- Remaining unknowns are explicit: four Azure cutoff values; whole-request versus marginal behavior for Gemini Developer API, Novita, Azure, and OpenAI GPT-5.5 Pro; per-1M-token conversion for two legacy Vertex rows; universal regional percentages on Azure/Vertex; and Mistral's model-level applicability.
- Ran no git commands and no test runners. Nothing was committed or pushed.
