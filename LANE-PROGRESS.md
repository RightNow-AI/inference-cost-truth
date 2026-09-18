## 2026-07-31 initial capture

- Created `evidence/`.
- Saved raw `curl.exe -L --compressed` response bodies for all nine supplied official starting URLs.
- Every starting URL returned HTTP 200: RunPod, Lambda, CoreWeave, Vast.ai, Hyperstack, Nebius, Together AI, AWS Capacity Blocks, and Google Cloud GPU pricing.
- Next: inspect static bodies for literal prices and per-GPU/per-node wording; trace first-party endpoints where static HTML lacks data.

## 2026-07-31 endpoint and table extraction bank

- RunPod, Lambda, CoreWeave, Hyperstack, Nebius, Together AI, and AWS Capacity Blocks expose usable literal pricing in their saved HTML.
- Vast.ai's static page did not contain the live rates. Saved its official page JavaScript and the first-party endpoint it calls: `evidence/vast-gpu-pricing-public.json`.
- Saved AWS's official EC2 pricing widget assets and current metered-unit map as `evidence/aws-ec2-metered-unit-map.json`; the map contains current P5 on-demand regional rates but no P6/P5e/P5en on-demand entries.
- Google's supplied URL redirected to the general Compute pricing surface. Saved the official accelerator-optimized pricing page plus the all-pricing and Spot VM pages.
- Critical unit handling: CoreWeave full-instance columns are node rates while its inference column explicitly says single GPU; Lambda on-demand explicitly says `PRICE/GPU/HR`; Nebius says `GPU-hour`; Together says all cluster prices are per GPU per hour. Ambiguous surfaces will be emitted as `UNCLEAR` rather than inferred.
- Next: generate `findings.json`, validate every exact `evidence_literal` against its saved file, and write the grouped human summary with all unresolved gaps.

## 2026-07-31 final build and literal validation bank

- Wrote `findings.json` and `FINDINGS.md`.
- Emitted 355 evidence-backed numeric rows: AWS 69, CoreWeave 41, Google Cloud 129, Hyperstack 30, Lambda 28, Nebius 14, RunPod 32, Together AI GPU clusters 12.
- Vast.ai emitted zero rows: its saved official live endpoint does not declare per-GPU versus per-machine units or a price tier, so mapping its values would require guessing.
- Mechanical validation passed for all 355 rows: JSON parsed, required unit/tier enums were valid, every per-node row had `gpus_per_node`, every evidence file existed, and every exact `evidence_literal` was found byte-for-text in its saved response. Validation errors: 0.
- Recorded all observed fetches as HTTP 200 in `FINDINGS.md`, including the official follow-up JSON and JavaScript endpoints.
