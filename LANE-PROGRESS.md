# LANE billing-mechanics progress

## 2026-07-31 checkpoint 1

- Confirmed worktree contents: only `README.md` was present before lane output.
- Read the browser-control instructions; the in-app browser backend is unavailable, so discovery will use official-domain HTTP/search and all evidence capture will use raw `curl.exe` downloads.
- Scope fixed at 25 provider-topic combinations: 10 prompt-caching, 10 batch/async, and 5 reasoning-token rows.
- No Git commands or test runners will be used.

## 2026-07-31 checkpoint 2

- Saved raw official prompt-caching pages for OpenAI, Anthropic, Google, xAI, DeepSeek, Mistral, Together, Fireworks, DeepInfra, and Groq.
- Google HTML and `.md.txt` initially entered an OAuth redirect loop; verified the vendor endpoint returns `200` when the DevSite wall cookie is supplied, then saved the raw official Markdown mirrors.
- Confirmed current cache-mechanics evidence includes OpenAI GPT-5.6-era cache-write pricing and breakpoints, Anthropic automatic plus explicit caching and model-specific minimums, Google implicit plus explicit cache objects, Mistral cache-block minimums, and Groq TTL/minimum ranges.
- Saved raw official batch pages for OpenAI, Anthropic, Google, xAI, Mistral, Together, Fireworks, DeepInfra, and Groq. DeepSeek's official sitemap/docs index contains no batch page found so far.
- Located DeepInfra's canonical docs host (`docs.deepinfra.com`) after the legacy `/docs` shell exposed its navigation; captured the actual Batch API Markdown with the documented discount, window, endpoints, and limits.

## 2026-07-31 checkpoint 3

- Saved current official reasoning-token pages for OpenAI, Anthropic, Google Gemini, xAI, and DeepSeek, including API usage-field examples and documented visibility/billing behavior.
- Captured official worked token-count examples for all five reasoning providers where available; DeepSeek documents its usage field and full `reasoning_content` response but no worked numeric token-count example was found.
- Generated `findings.json` with 25 rows: 10 prompt-caching, 10 batch/async, and 5 reasoning-token rows.
- Mechanically verified every primary and supporting `evidence_literal` against its named raw file: zero misses.
- Performed a second scan of all numeric claims, including model-name numerals, against the combined evidence literals for each row: zero misses.

## 2026-07-31 final checkpoint

- Wrote `FINDINGS.md`, grouped by provider, with the required fetch-failure and unverifiable-items sections.
- Final schema check found all required fields present across all 25 rows.
- Final evidence checks: 25 primary literals verified, all supporting literals verified, and zero numeric-claim misses.
- Preserved the raw official response bodies in 67 files under `evidence/`.
- No Git commands, test runners, commits, pushes, or deployments were performed.
