# Lane progress

## 2026-07-31 initial inventory

- Read `data/providers.json` and `data/self-host-inputs.json` without modifying either file.
- Found 586 provider/model rows, 355 GPU-rental rows, 36 GPU-rental rows with `per_gpu_or_per_node = "UNCLEAR"`, and 352 provider/model rows with `context_window = null`.
- The 36 unclear billing-unit rows are 30 Hyperstack rows and 6 Lambda 1-Click Cluster rows.
- Created `evidence/`; only unmodified first-party HTTP response bodies will be stored there.
- No Git commands or test runners used.

## 2026-07-31 pricing and unit-evidence checkpoint

- Saved raw 200-response bodies for TensorWave MI355X/MI325X/MI300X product pages, Crusoe pricing and AMD product pages, Vultr cloud-GPU pricing, DigitalOcean GPU Droplets pricing, Oracle Cloud price list plus its official JSON price feed, Hot Aisle pricing, RunPod pricing, Azure ND MI300X docs plus the Azure Retail Prices API, Hyperstack pricing/docs, Lambda pricing/docs, and Vast.ai pricing/page bundles.
- Saved one TensorWave URL that returned HTTP 404 (`evidence/tensorwave-wafer-mi355x-blog.html`) and will report it as an unfetchable page rather than use it.
- Gap 1 has direct AMD hourly evidence from TensorWave, Crusoe, Vultr, DigitalOcean, Oracle, Hot Aisle, and Azure. Some named providers expose AMD products but no public price; those will remain explicitly unverified.
- Found Vast.ai's unauthenticated first-party page endpoint: `https://storage.googleapis.com/vast-public-gpu-pricing/gpu-pricing-public.json`. Saved its raw current response and the page JavaScript that proves the endpoint and renders `min` as the displayed `from $.../hr` value.
- Hyperstack's official pricebook content says GPU entries are billed `Per GPU, per hour`; Lambda's official billing docs say 1-Click Clusters are priced per GPU per hour. This resolves all 36 existing `UNCLEAR` rows as `per_gpu` without cross-provider inference.
- No files under `data/` and no `README.md` edits.

## 2026-07-31 context checkpoint

- Saved raw official model documentation for OpenAI GPT-5.6 Sol/Terra/Luna and GPT-OSS 120B/20B, Anthropic's model overview, Google's Gemini 3 guide and Gemini 3.1 Pro page, and Mistral Large 3 / Medium 3.5 model cards.
- Evidence literals found: OpenAI `1,050,000 context window` and `131,072 context window`; Anthropic `200k tokens`; Gemini 3 `1M / 64k`; Mistral `256k`.
- Context findings will preserve those literal vendor units rather than derive alternate numeric spellings.
- Remaining work: capture Runpod pricing bundles, assemble findings.json/FINDINGS.md, and mechanically verify every evidence literal.

## 2026-07-31 final checkpoint

- Saved `findings.json` with 75 findings: 15 AMD pricing rows, 8 Vast.ai current-rate rows, 36 explicit unit resolutions, and 16 context-window mappings.
- The 16 context mappings cover 54 currently null provider/model rows by exact provider + model-name match.
- Saved `FINDINGS.md` with provider-grouped summaries, the mandatory unfetchable/unverified sections, and an HTTP status log covering all 54 saved evidence bodies.
- Mechanical validation passed: JSON parses; all 75 primary evidence literals and all auxiliary unit, node, endpoint, display, and tier literals are exact substrings of their declared evidence files.
- All 36 source `UNCLEAR` rows have a corresponding evidence-backed resolution. No files under `data/` and no `README.md` edits were made.
- No Git commands, test runners, commits, or pushes were used.
