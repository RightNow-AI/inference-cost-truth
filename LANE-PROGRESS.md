# LANE audit progress

## 2026-07-31 initial inventory

- Read the required `data/providers.json`, `data/self-host.json`, `data/self-host-inputs.json`, `data/tokenizers.json`, and `README.md`.
- `providers.json` contains 586 API rows across 14 providers and 355 GPU-rental rows across 8 providers.
- Found 36 GPU rows marked `per_gpu_or_per_node = "UNCLEAR"`: 30 Hyperstack rows and 6 Lambda rows. All 36 are mandatory members of the live sample.
- Planned sample: every unclear GPU row, API price extremes/flagship-looking rows from all API providers, and GPU extremes from every remaining GPU provider; target is above 60 total rows.
- No Git commands or test runners have been used. No files under `data/` and no README content have been modified.

## 2026-07-31 live-fetch and first adversarial pass

- Built an 86-row base sample spanning all 14 API providers and all 8 GPU-rental providers. It includes all 36 `UNCLEAR` GPU rows. Added targeted flagship/effective-date and mislabeled-tier rows after the first pass, so the final checked set will exceed 100 source rows.
- Fresh raw bodies are saved in `evidence/2026-07-31/` for 26 distinct official URLs. Twenty-five returned HTTP 200. The Gemini pricing URL entered an OAuth redirect loop; a raw HTTP 302 redirect body is saved as `01_ai.google.dev_gemini-api_docs_pricing.body` after the followed-redirect attempt exhausted its limit.
- Confirmed a real structural mismatch: 11 Fireworks records store `service_tier="standard"` even though their prices are taken from the live table's `Priority` column. The live page explicitly labels the columns `Standard` and `Priority` and prints both vectors.
- Confirmed a README-currentness mismatch: the closed-vendor table prints Claude Sonnet 5's post-2026-09-01 standard price, while the live page says the lower introductory price applies through 2026-08-31. Both future and current rows exist in JSON, but the README chooses the future row without its effective-date qualifier.
- All 24 self-host arithmetic cells recomputed within the published rounding tolerance; none differ by more than the mission threshold.
- No Git commands, commits, pushes, or test runners have been used.

## 2026-07-31 final bank

- Final adversarial sample: 126 source rows across every API and GPU provider; 123 rows have all sampled numeric fields backed by literal text in saved official responses. The 3 unresolved rows are Google Gemini rows blocked by the OAuth redirect loop.
- Wrote 326 machine-readable checks: 296 matches, 21 mismatches/relationship anomalies, and 9 unverifiable Google field checks.
- Mechanically re-opened every declared evidence file and confirmed that all 326 `evidence_literal` strings and all 326 raw `quote` strings occur exactly in their declared files.
- Final findings include 11 Fireworks service-tier label mismatches, 10 unexplained OpenAI Batch/Fast relationship anomalies, the README Claude Sonnet 5 future-price presentation issue, and the README Llama self-host one-cent double-rounding issue.
- All 24 self-host formula recomputations remain within 0.01; the report enumerates 24 utilization/configuration comparisons where the comparable hosted API is cheaper.
- Saved `AUDIT.md`, `audit.json`, `FINDINGS.md`, and `findings.json`. No data or README file was edited; no Git command, test runner, commit, or push was used.
