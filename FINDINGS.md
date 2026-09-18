# Gap closure report

Retrieved on: 2026-07-31

This lane produced 75 evidence-backed findings in `findings.json` without editing `data/` or `README.md`. The 16 context mappings apply to 54 null-context source rows that share the same provider and model name.

## GAP 1 — AMD Instinct hourly pricing

### TensorWave

| GPU | Published rate | Unit | Tier | Evidence |
| --- | ---: | --- | --- | --- |
| AMD Instinct MI355X | $2.95 | per GPU hour | starting at | `evidence/tensorwave-mi355x-product.html`: `$2.95`, `/GPU HR`, `Starting at` |
| AMD Instinct MI325X | $2.25 | per GPU hour | starting at | `evidence/tensorwave-mi325x-product.html`: `$2.25`, `/GPU HR`, `Starting at` |
| AMD Instinct MI300X | $1.71 | per GPU hour | starting at | `evidence/tensorwave-mi300x-product.html`: `$1.71`, `/GPU HR`, `Starting at` |

These are genuine published per-GPU-hour starting rates, but TensorWave does not call them on-demand.

### Crusoe

| GPU | Published rate | Unit | Tier | Evidence |
| --- | ---: | --- | --- | --- |
| AMD Instinct MI300X | $3.45 | per GPU hour | on-demand | `evidence/crusoe-pricing.html`: `$3.45/GPU-hr`, `On-demand` |

Crusoe lists MI355X, but its price is “Contact sales”; no numeric MI355X finding was created.

### Vultr

| GPU | Published rate | Unit | Tier | Evidence |
| --- | ---: | --- | --- | --- |
| AMD Instinct MI355X | $2.590 | per GPU hour | on-demand | `evidence/vultr-cloud-gpu-pricing.html`: `<strong>$2.590</strong>/GPU/hr` |
| AMD Instinct MI325X | $2.000 | per GPU hour | on-demand | `evidence/vultr-cloud-gpu-pricing.html`: `<strong>$2.000</strong>/GPU/hr` |
| AMD Instinct MI300X | $1.850 | per GPU hour | on-demand | `evidence/vultr-cloud-gpu-pricing.html`: `<strong>$1.850</strong>/GPU/hr` |

The same official table says `Pricing shown is on-demand`.

### DigitalOcean

| GPU | Published rate | Unit | Tier | Evidence |
| --- | ---: | --- | --- | --- |
| AMD Instinct MI350X | $4.76 | per GPU hour | 12-month reserved | `evidence/digitalocean-gpu-droplets-pricing.html`: `$4.76`, `12 Month Reserved Price` |
| AMD Instinct MI325X | $2.88 | per GPU hour | 12-month reserved | `evidence/digitalocean-gpu-droplets-pricing.html`: `$2.88`, `12 Month Reserved Price` |
| AMD Instinct MI300X | $1.91 | per GPU hour | 12-month reserved | `evidence/digitalocean-gpu-droplets-pricing.html`: `$1.91`, `12 Month Reserved Price` |
| AMD Instinct MI300X | $1.99 | per GPU hour | labeled on-demand, struck through | `evidence/digitalocean-gpu-droplets-pricing.html`: `$1.99`, `On-Demand Price` |

The $1.99 value is retained with an explicit uncertainty flag: the page labels it on-demand but renders it inside a strike-through element and says new on-demand pricing is coming on August 1, 2026.

### Oracle Cloud

| GPU | Published rate | Unit | Tier | Evidence |
| --- | ---: | --- | --- | --- |
| AMD Instinct MI300X | $6 | per GPU hour | pay as you go | `evidence/oracle-cloud-price-list.json`: `"USD": 6`; HTML part `B109485` |
| AMD Instinct MI355X | $8.6 | per GPU hour | pay as you go | `evidence/oracle-cloud-price-list.json`: `"USD": 8.6`; HTML part `B111758` |

The official HTML table header is `GPU price per hour`; the rows map the GPU shapes to the part numbers used by Oracle's official JSON price feed.

### Hot Aisle

| GPU | Published rate | Unit | Tier | Evidence |
| --- | ---: | --- | --- | --- |
| AMD Instinct MI300X | $2.99 | per GPU hour | on-demand VM/new customer | `evidence/hotaisle-pricing.html`: `$2.99/GPU/hr`, `billed by the minute` |

The page mentions MI355X service but prints no MI355X price.

### Microsoft Azure

| GPU/shape | Published rate | Unit | Tier/region | Evidence |
| --- | ---: | --- | --- | --- |
| ND96isrMI300Xv5 / AMD Instinct MI300X | $48.0 | per 8-GPU VM hour | consumption, US East 2 | `evidence/azure-retail-mi300x.json`: `"retailPrice":48.0,"unitPrice":48.0`; `evidence/azure-nd-mi300x-v5.html`: `<td>8 GPUs</td>` |

No derived per-GPU division is reported because the evidence law requires the reported number itself to appear literally.

## GAP 2 — Vast.ai rates and endpoint

The pricing page's own JavaScript calls this unauthenticated first-party endpoint:

`https://storage.googleapis.com/vast-public-gpu-pricing/gpu-pricing-public.json`

`evidence/vast-live-gpu-grid.js` contains that literal endpoint and maps `current.min` into the displayed rate. `evidence/vast-chunk-4232.js` renders the value with `/hr`.

| GPU | Current minimum shown as hourly | Exact JSON evidence |
| --- | ---: | --- |
| NVIDIA B200 | $4.6265 | `"b200":{"current":{"p10":4.6265,"median":6.6891,"min":4.6265,"available":57}` |
| NVIDIA H200 | $3.9351 | `"h200":{"current":{"p10":3.9351,"median":4.1455,"min":3.9351,"available":17}` |
| NVIDIA H100 SXM | $1.6009 | `"h100 sxm":{"current":{"p10":1.6019,"median":2.7602,"min":1.6009,"available":55}` |
| NVIDIA H100 PCIe | $1.7334 | `"h100 pcie":{"current":{"p10":1.7334,"median":2.0002,"min":1.7334,"available":40}` |
| NVIDIA H100 NVL | $1.9347 | `"h100 nvl":{"current":{"p10":1.9347,"median":2.5881,"min":1.9347,"available":11}` |
| NVIDIA A100 SXM4 | $0.1347 | `"a100 sxm4":{"current":{"p10":0.4046,"median":0.8287,"min":0.1347,"available":146}` |
| NVIDIA A100 PCIe | $0.3335 | `"a100 pcie":{"current":{"p10":0.3337,"median":0.8669,"min":0.3335,"available":83}` |
| NVIDIA L40S | $0.4002 | `"l40s":{"current":{"p10":0.4007,"median":0.6212,"min":0.4002,"available":114}` |

The endpoint and page bundles do not explicitly settle whether the normalized rate is per physical GPU or per multi-GPU offer. Those eight findings therefore retain `per_gpu_or_per_node = "UNCLEAR"`.

## GAP 3 — Previously unclear rental units

### Hyperstack

All 30 Hyperstack rows are resolved to `per_gpu`. The price literals remain in `evidence/hyperstack-gpu-pricing.html`; the official pricebook bundle says `Per GPU, per hour` in `evidence/hyperstack-pricebook-content.js`.

| GPU | Tiers and saved rate literals |
| --- | --- |
| NVIDIA A100 | on-demand $1.35; reserved $0.95; spot $1.08 |
| NVIDIA A100 NVLink | on-demand $1.40; reserved $0.98 |
| NVIDIA A100 SXM | on-demand $1.60; reserved $1.36 |
| NVIDIA A4000 | on-demand $0.15; reserved $0.11 |
| NVIDIA A6000 | on-demand $0.50; reserved $0.35; spot $0.40 |
| NVIDIA B200 | on-demand $6.00; reserved $5.10 |
| NVIDIA B300 | on-demand $7.40 |
| NVIDIA H100 | on-demand $2.50; reserved $1.75 |
| NVIDIA H100 NVLink | on-demand $2.60; reserved $1.82 |
| NVIDIA H100 PCIe | spot $2.00 |
| NVIDIA H100 SXM | on-demand $3.20; reserved $2.72 |
| NVIDIA H200 SXM | on-demand $3.99; reserved $2.79 |
| NVIDIA L40 | on-demand $1.00; reserved $0.70; spot $0.80 |
| NVIDIA RTX Pro 6000 SE | on-demand $1.85; reserved $1.30; spot $1.48 |

### Lambda

All six Lambda 1-Click Cluster rows are resolved to `per_gpu`. The official billing page says `priced per GPU per hour` in `evidence/lambda-billing.html`.

| GPU | GPU-count tier | Saved rate literal |
| --- | ---: | ---: |
| NVIDIA H100 | 256 | $5.54 |
| NVIDIA H100 | 64 | $5.85 |
| NVIDIA H100 | 16 | $6.16 |
| NVIDIA HGX B200 | 256+ | $8.87 |
| NVIDIA HGX B200 | 64 | $9.36 |
| NVIDIA HGX B200 | 16 | $9.86 |

## GAP 4 — Context windows

Each mapping applies to every null-context row with the same provider and model name.

| Provider | Model | Context window | Evidence |
| --- | --- | --- | --- |
| OpenAI | gpt-5.6-sol | 1,050,000 | `evidence/openai-gpt-5.6-sol.md`: `1,050,000 context window` |
| OpenAI | gpt-5.6-terra | 1,050,000 | `evidence/openai-gpt-5.6-terra.md`: `1,050,000 context window` |
| OpenAI | gpt-5.6-luna | 1,050,000 | `evidence/openai-gpt-5.6-luna.md`: `1,050,000 context window` |
| Fireworks AI | OpenAI GPT OSS 120B | 131,072 | `evidence/openai-gpt-oss-120b.md`: `131,072 context window` |
| Fireworks AI | OpenAI GPT OSS 20B | 131,072 | `evidence/openai-gpt-oss-20b.md`: `131,072 context window` |
| Groq | openai/gpt-oss-120b | 131,072 | `evidence/openai-gpt-oss-120b.md`: `131,072 context window` |
| Groq | openai/gpt-oss-20b | 131,072 | `evidence/openai-gpt-oss-20b.md`: `131,072 context window` |
| Baseten | openai/gpt-oss-120b | 131,072 | `evidence/openai-gpt-oss-120b.md`: `131,072 context window` |
| Anthropic | Claude Haiku 4.5 | 200k tokens | `evidence/anthropic-models-overview.md`: `200k tokens` |
| Anthropic | Claude Opus 4.5 | 200k tokens | `evidence/anthropic-models-overview.md`: `200k tokens` |
| Anthropic | Claude Sonnet 4.5 | 200k tokens | `evidence/anthropic-models-overview.md`: `200k tokens` |
| Google Gemini | Gemini 3.1 Pro Preview | 1M | `evidence/google-gemini-3-guide.html`: `1M / 64k` |
| Google Gemini | Gemini 3 Flash Preview | 1M | `evidence/google-gemini-3-guide.html`: `1M / 64k` |
| Google Gemini | Gemini 3.1 Flash-Lite | 1M | `evidence/google-gemini-3-guide.html`: `1M / 64k` |
| Mistral | Mistral Large 3 | 256k | `evidence/mistral-large-3.html`: `children\":\"256k\"` |
| Mistral | Mistral Medium 3.5 | 256k | `evidence/mistral-medium-3.5.html`: `children\":\"256k\"` |

## PAGES I COULD NOT FETCH

- HTTP 404 — `https://tensorwave.com/blog/wafer-reached-1-inference-performance-for-qwen3.5-397b-on-amd`; saved response body: `evidence/tensorwave-wafer-mi355x-blog.html`. It was not used for a finding.

## THINGS I COULD NOT VERIFY

- Crusoe MI355X: product is listed, but the pricing page says Contact sales rather than publishing a number.
- Hot Aisle MI355X: service is mentioned, but no numeric MI355X price appears.
- RunPod AMD pricing: the current pricing HTML and the downloaded first-party page bundles contain no MI300X, MI325X, or MI355X rate and expose no AMD pricing endpoint found in this pass.
- TensorWave commitment class: the product pages say Starting at and per GPU hour, but do not say on-demand.
- DigitalOcean MI300X $1.99: the page labels it On-Demand Price but strikes it through and announces new pricing for August 1, 2026.
- Vast.ai unit: the endpoint/page prove current minimum dollars per hour, but do not explicitly prove per GPU versus per multi-GPU offer.
- Azure per-GPU rate: the official API publishes a per-VM hourly number for an eight-GPU shape. A divided per-GPU value was intentionally not invented.
- Oracle MI325X: no public MI325X row was found in the captured GPU price table.
- Most remaining null context windows: this pass prioritized official flagship/model-owner documentation. Hardware-size-bracket rows and models without captured first-party context documentation remain open.

## HTTP STATUS LOG

Every URL below was fetched with a raw shell HTTP client and its response body was saved unmodified under `evidence/`.

### Primary and model evidence

- 200 — `https://tensorwave.com/products/accelerators/amd-mi355x` → `evidence/tensorwave-mi355x-product.html`
- 200 — `https://tensorwave.com/products/accelerators/amd-mi325x` → `evidence/tensorwave-mi325x-product.html`
- 200 — `https://tensorwave.com/products/accelerators/amd-mi300x` → `evidence/tensorwave-mi300x-product.html`
- 200 — `https://tensorwave.com/blog/enterprise-ai-at-scale-performance-and-efficiency-with-mi355x` → `evidence/tensorwave-modular-mi355x-blog.html`
- 404 — `https://tensorwave.com/blog/wafer-reached-1-inference-performance-for-qwen3.5-397b-on-amd` → `evidence/tensorwave-wafer-mi355x-blog.html`
- 200 — `https://www.crusoe.ai/cloud/pricing` → `evidence/crusoe-pricing.html`
- 200 — `https://www.crusoe.ai/cloud/gpus/amd-mi300x` → `evidence/crusoe-mi300x.html`
- 200 — `https://www.crusoe.ai/cloud/gpus/amd-mi355x` → `evidence/crusoe-mi355x.html`
- 200 — `https://www.vultr.com/pricing/#cloud-gpu` → `evidence/vultr-cloud-gpu-pricing.html`
- 200 — `https://www.digitalocean.com/pricing/gpu-droplets` → `evidence/digitalocean-gpu-droplets-pricing.html`
- 200 — `https://www.oracle.com/cloud/price-list` → `evidence/oracle-cloud-price-list.html`
- 200 — `https://www.oracle.com/a/ocom/docs/pricing/cloud-price-list.json` → `evidence/oracle-cloud-price-list.json`
- 200 — `https://hotaisle.xyz/` → `evidence/hotaisle-home.html`
- 200 — `https://hotaisle.xyz/pricing` → `evidence/hotaisle-pricing.html`
- 200 — `https://hotaisle.xyz/sitemap.xml` → `evidence/hotaisle-sitemap.xml`
- 200 — `https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/ndmi300xv5-series` → `evidence/azure-nd-mi300x-v5.html`
- 200 — Azure Retail Prices API query recorded verbatim in `findings.json` → `evidence/azure-retail-mi300x.json`
- 200 — `https://www.hyperstack.cloud/gpu-pricing` → `evidence/hyperstack-gpu-pricing.html`
- 200 — `https://docs.hyperstack.cloud/docs/billing/pricebook` → `evidence/hyperstack-pricebook.html`
- 200 — `https://lambda.ai/pricing` → `evidence/lambda-pricing.html`
- 200 — `https://docs.lambda.ai/public-cloud/billing/` → `evidence/lambda-billing.html`
- 200 — `https://vast.ai/pricing` → `evidence/vast-pricing.html`
- 200 — `https://storage.googleapis.com/vast-public-gpu-pricing/gpu-pricing-public.json` → `evidence/vast-gpu-pricing-public.json`
- 200 — `https://www.runpod.io/pricing` → `evidence/runpod-pricing.html`
- 200 — `https://developers.openai.com/api/docs/models/gpt-5.6-sol.md` → `evidence/openai-gpt-5.6-sol.md`
- 200 — `https://developers.openai.com/api/docs/models/gpt-5.6-terra.md` → `evidence/openai-gpt-5.6-terra.md`
- 200 — `https://developers.openai.com/api/docs/models/gpt-5.6-luna.md` → `evidence/openai-gpt-5.6-luna.md`
- 200 — `https://developers.openai.com/api/docs/models/gpt-oss-120b.md` → `evidence/openai-gpt-oss-120b.md`
- 200 — `https://developers.openai.com/api/docs/models/gpt-oss-20b.md` → `evidence/openai-gpt-oss-20b.md`
- 200 — `https://platform.claude.com/docs/en/about-claude/models/overview.md` → `evidence/anthropic-models-overview.md`
- 200 — `https://ai.google.dev/gemini-api/docs/gemini-3` → `evidence/google-gemini-3-guide.html`
- 200 — `https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview` → `evidence/google-gemini-3.1-pro.html`
- 200 — `https://docs.mistral.ai/models/model-cards/mistral-large-3-25-12` → `evidence/mistral-large-3.html`
- 200 — `https://docs.mistral.ai/models/model-cards/mistral-medium-3-5-26-04` → `evidence/mistral-medium-3.5.html`

### First-party scripts and exploratory captures

- 200 — `https://www.oracle.com/asset/web/js/redwood-base.js` → `evidence/oracle-redwood-base.js`
- 200 — `https://www.oracle.com/asset/web/js/redwood-lib.js` → `evidence/oracle-redwood-lib.js`
- 200 — `https://www.oracle.com/asset/web/analytics/ora_ocom.js` → `evidence/oracle-ocom.js`
- 200 — `https://docs.hyperstack.cloud/assets/js/runtime~main.d1a615cd.js` → `evidence/hyperstack-docs-runtime.js`
- 200 — `https://docs.hyperstack.cloud/assets/js/main.08e61e88.js` → `evidence/hyperstack-docs-main.js`
- 200 — `https://docs.hyperstack.cloud/assets/js/2b931c2b.41be73cc.js` → `evidence/hyperstack-pricebook-content.js`
- 200 — `https://docs.hyperstack.cloud/docs/hardware/gpu-stock-information` → `evidence/hyperstack-gpu-stock.html`
- 200 — `https://docs.hyperstack.cloud/assets/js/fd533ec9.89a00ae5.js` → `evidence/hyperstack-gpu-stock-content.js`
- 200 — `https://www.hyperstack.cloud/technical-resources/tutorials/deploy-kimi-k3-on-gpu-cloud-for-multi-node-2.8t-inference` → `evidence/hyperstack-kimi-k3.html`
- 200 — `https://vast.ai/_next/static/chunks/pages/pricing-6583595ef438a320.js` → `evidence/vast-pricing-page.js`
- 200 — `https://vast.ai/_next/static/chunks/2827-132b2e2e745e256c.js` → `evidence/vast-chunk-2827.js`
- 200 — `https://vast.ai/_next/static/chunks/pages/_app-9d90c6b337a08e94.js` → `evidence/vast-app.js`
- 200 — `https://vast.ai/_next/static/chunks/webpack-31ac7c827ed334bc.js` → `evidence/vast-webpack.js`
- 200 — `https://vast.ai/_next/static/Em5SapaSxo7hsKlA66oCL/_buildManifest.js` → `evidence/vast-build-manifest.js`
- 200 — `https://vast.ai/_next/static/chunks/7881.2eabab5515a3d7d7.js` → `evidence/vast-live-gpu-grid.js`
- 200 — `https://vast.ai/_next/static/chunks/4816-bdb91222d08563f9.js` → `evidence/vast-chunk-4816.js`
- 200 — `https://vast.ai/_next/static/chunks/4232.c71e74bf90ae20fd.js` → `evidence/vast-chunk-4232.js`
- 200 — `https://cdn.prod.website-files.com/69ce570adca53340abab8376%2F6a132dc4acf7a6f191b1972d%2F6a67910ec52097b235dc715d%2Frunpod_pricing_answer_polish-1.0.1.js` → `evidence/runpod-pricing-polish.js`
- 200 — `https://cdn.prod.website-files.com/69ce570adca53340abab8376/js/runpod-staging.schunk.f2efb3c5440a81cf.js` → `evidence/runpod-site-chunk.js`
- 200 — `https://cdn.prod.website-files.com/69ce570adca53340abab8376/js/runpod-staging.25e43267.c1e6fa75a4a44c97.js` → `evidence/runpod-site-main.js`
