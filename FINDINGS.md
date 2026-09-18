# Live-source audit findings

Retrieved on 2026-07-31 with raw shell HTTP clients. Every machine-readable evidence literal was checked against the saved response body.

- Source rows sampled: 126 across every provider in both arrays
- Source rows with all sampled numeric fields evidence-backed: 123
- Source rows not re-verifiable: 3
- Machine-readable checks: 326 (matches 296, mismatches 21, unverifiable 9)

## Provider summary

| Provider | Source rows | Match checks | Mismatch checks | Unverifiable checks |
|---|---:|---:|---:|---:|
| Anthropic | 9 | 32 | 0 | 0 |
| AWS | 2 | 2 | 0 | 0 |
| Baseten | 2 | 5 | 0 | 0 |
| Cerebras | 2 | 4 | 0 | 0 |
| CoreWeave | 2 | 2 | 0 | 0 |
| DeepInfra | 5 | 13 | 0 | 0 |
| DeepSeek | 2 | 6 | 0 | 0 |
| Fireworks AI | 15 | 43 | 11 | 0 |
| Google Cloud | 2 | 2 | 0 | 0 |
| Google Gemini | 3 | 0 | 0 | 9 |
| Groq | 3 | 7 | 0 | 0 |
| Hyperstack | 30 | 60 | 0 | 0 |
| Lambda | 6 | 12 | 0 | 0 |
| Mistral | 2 | 4 | 0 | 0 |
| Nebius | 2 | 2 | 0 | 0 |
| Nebius AI Studio | 2 | 3 | 0 | 0 |
| Novita AI | 2 | 5 | 0 | 0 |
| OpenAI | 27 | 81 | 10 | 0 |
| RunPod | 2 | 2 | 0 | 0 |
| Together AI | 3 | 7 | 0 | 0 |
| Together AI GPU clusters | 2 | 2 | 0 | 0 |
| xAI | 1 | 2 | 0 | 0 |

## Mismatches grouped by provider

### Fireworks AI

The following rows store `service_tier="standard"`, but their values are taken from the official table's Priority column and their own notes say Priority:

- `providers.rows[327]` -- Kimi K3
- `providers.rows[330]` -- Kimi K3 US
- `providers.rows[332]` -- Kimi K2.7 Code
- `providers.rows[335]` -- Kimi K2.6
- `providers.rows[338]` -- DeepSeek V4 Pro
- `providers.rows[340]` -- DeepSeek V4 Flash
- `providers.rows[342]` -- GLM 5.2
- `providers.rows[345]` -- GLM 5.1
- `providers.rows[349]` -- MiniMax M3
- `providers.rows[351]` -- MiniMax M2.7
- `providers.rows[353]` -- OpenAI GPT OSS 120B

The price values themselves match the live Priority cells. Exact raw table excerpts and literals are in `findings.json`.

### OpenAI

The live price values match the repo, but these rows violate the requested unexplained tier relationship check:

- `providers.rows[108]` -- gpt-5.5 (<272K context length): official Fast table is not exactly double Standard
- `providers.rows[114]` -- gpt-5-mini: official Fast table is not exactly double Standard
- `providers.rows[115]` -- gpt-4.1: official Fast table is not exactly double Standard
- `providers.rows[116]` -- gpt-4.1-mini: official Fast table is not exactly double Standard
- `providers.rows[118]` -- gpt-4o: official Fast table is not exactly double Standard
- `providers.rows[119]` -- gpt-4o-2024-05-13: official Fast table is not exactly double Standard
- `providers.rows[120]` -- gpt-4o-mini: official Fast table is not exactly double Standard
- `providers.rows[121]` -- o3: official Fast table is not exactly double Standard
- `providers.rows[122]` -- o4-mini: official Fast table is not exactly double Standard
- `providers.rows[74]` -- gpt-3.5-turbo-1106: official Batch table is not exactly half Standard

## Confirmed price rows by provider

- **Anthropic:** providers.rows[152], providers.rows[169], providers.rows[170], providers.rows[171], providers.rows[172], providers.rows[173], providers.rows[183], providers.rows[193], providers.rows[194]
- **AWS:** providers.gpu_rental_rows[15], providers.gpu_rental_rows[63]
- **Baseten:** providers.rows[423], providers.rows[433]
- **Cerebras:** providers.rows[420], providers.rows[421]
- **CoreWeave:** providers.gpu_rental_rows[83], providers.gpu_rental_rows[98]
- **DeepInfra:** providers.rows[368], providers.rows[375], providers.rows[376], providers.rows[392], providers.rows[406]
- **DeepSeek:** providers.rows[279], providers.rows[280]
- **Fireworks AI:** providers.rows[326], providers.rows[327], providers.rows[328], providers.rows[330], providers.rows[332], providers.rows[335], providers.rows[338], providers.rows[340], providers.rows[342], providers.rows[345], providers.rows[348], providers.rows[349], providers.rows[351], providers.rows[353], providers.rows[361]
- **Google Cloud:** providers.gpu_rental_rows[142], providers.gpu_rental_rows[232]
- **Groq:** providers.rows[413], providers.rows[417], providers.rows[418]
- **Hyperstack:** providers.gpu_rental_rows[239], providers.gpu_rental_rows[240], providers.gpu_rental_rows[241], providers.gpu_rental_rows[242], providers.gpu_rental_rows[243], providers.gpu_rental_rows[244], providers.gpu_rental_rows[245], providers.gpu_rental_rows[246], providers.gpu_rental_rows[247], providers.gpu_rental_rows[248], providers.gpu_rental_rows[249], providers.gpu_rental_rows[250], providers.gpu_rental_rows[251], providers.gpu_rental_rows[252], providers.gpu_rental_rows[253], providers.gpu_rental_rows[254], providers.gpu_rental_rows[255], providers.gpu_rental_rows[256], providers.gpu_rental_rows[257], providers.gpu_rental_rows[258], providers.gpu_rental_rows[259], providers.gpu_rental_rows[260], providers.gpu_rental_rows[261], providers.gpu_rental_rows[262], providers.gpu_rental_rows[263], providers.gpu_rental_rows[264], providers.gpu_rental_rows[265], providers.gpu_rental_rows[266], providers.gpu_rental_rows[267], providers.gpu_rental_rows[268]
- **Lambda:** providers.gpu_rental_rows[284], providers.gpu_rental_rows[285], providers.gpu_rental_rows[286], providers.gpu_rental_rows[292], providers.gpu_rental_rows[293], providers.gpu_rental_rows[294]
- **Mistral:** providers.rows[261], providers.rows[274]
- **Nebius:** providers.gpu_rental_rows[299], providers.gpu_rental_rows[306]
- **Nebius AI Studio:** providers.rows[552], providers.rows[567]
- **Novita AI:** providers.rows[441], providers.rows[450]
- **OpenAI:** providers.rows[0], providers.rows[3], providers.rows[13], providers.rows[16], providers.rows[17], providers.rows[19], providers.rows[20], providers.rows[21], providers.rows[23], providers.rows[25], providers.rows[26], providers.rows[32], providers.rows[36], providers.rows[43], providers.rows[74], providers.rows[83], providers.rows[96], providers.rows[105], providers.rows[108], providers.rows[114], providers.rows[115], providers.rows[116], providers.rows[118], providers.rows[119], providers.rows[120], providers.rows[121], providers.rows[122]
- **RunPod:** providers.gpu_rental_rows[320], providers.gpu_rental_rows[337]
- **Together AI:** providers.rows[281], providers.rows[284], providers.rows[286]
- **Together AI GPU clusters:** providers.gpu_rental_rows[343], providers.gpu_rental_rows[350]
- **xAI:** providers.rows[260]

## PAGES I COULD NOT FETCH

- `https://ai.google.dev/gemini-api/docs/pricing` -- the first response was HTTP 302; following redirects exhausted curl's 50-redirect limit in an OAuth loop. The unmodified 302 body is saved as `evidence/2026-07-31/01_ai.google.dev_gemini-api_docs_pricing.body`.

## THINGS I COULD NOT VERIFY

- `providers.rows[202]` -- Gemini 3.6 Flash: model existence and all sampled prices were not present in the saved redirect response.
- `providers.rows[226]` -- Gemini 3.1 Pro Preview: model existence and all sampled prices were not present in the saved redirect response.
- `providers.rows[245]` -- Gemini 2.5 Flash-Lite: model existence and all sampled prices were not present in the saved redirect response.
- Hyperstack: all thirty sampled rows remain honestly `UNCLEAR` for per-GPU versus per-node. The page says "Pricing Per Hour" but does not bind that rate to a GPU or a node.
- Lambda: all six sampled reserved-cluster rows remain honestly `UNCLEAR`. The tables state GPU count and price per hour, but do not explicitly say whether the listed price is per GPU or for the cluster.
