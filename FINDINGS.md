# Current official GPU rental hourly rates

Retrieved on 2026-07-31. Every row in `findings.json` points to a raw saved first-party response and an exact `evidence_literal`. Rates are not normalized across per-GPU and per-node products.

## Evidence-backed row counts

| Provider | Rows |
|---|---:|
| AWS | 69 |
| CoreWeave | 41 |
| Google Cloud | 129 |
| Hyperstack | 30 |
| Lambda | 28 |
| Nebius | 14 |
| RunPod | 32 |
| Together AI GPU clusters | 12 |
| **Total** | **355** |

## RunPod

Secure Cloud and Community Cloud are separate rows. The visible GPU table says `Per hour`; model rows and VRAM are preserved exactly. Network Storage (Standard) is `$0.07/GB/mo` under 1 TB and `$0.05/GB/mo` over 1 TB; Network Storage (High-Performance) is `$0.14/GB/mo`. No egress rate was found on the captured page.

## Lambda

On-demand rows are explicitly `PRICE/GPU/HR*`. 1-Click Cluster rows are `UNCLEAR` because the table gives GPU count and `Price per hour` without declaring whether the price is per GPU or per cluster. The numeric cluster term is `2 weeks – 1 year`. The page states `No egress fees`.

## CoreWeave

Full-instance on-demand and spot rows are per node using the printed GPU count; inference rows use the explicit `Inference Single GPU Price(Per Hour)` column. Reserved compute advertises up to 60% discounts but publishes no exact reserved rates. Storage: AI Object Storage Hot `$0.06/GB/mo`, Warm `$0.03/GB/mo`, Cold `$0.015/GB/mo`, Archive `$0.0125/GB/mo`, and Distributed File Storage `$0.070/GB/mo`. The page states no ingress, egress, or transfer fees; internet and intra-CoreWeave data transfer are Free.

## Vast.ai

No rows emitted. The saved official endpoint is current and first-party, but it exposes min/median offer statistics without an explicit per-GPU versus per-machine unit and without a tier field. The surrounding page says on-demand, interruptible, and reserved are separate choices, so assigning the endpoint values to one tier would be a guess. The page separately states per-second billing, no minimum hours, and reserved terms of 1, 3, or 6 months.

## Hyperstack

On-demand, reservation, and spot tier labels are explicit, but the page never says whether the price is per GPU or per node, so every Hyperstack row is `UNCLEAR`. On-demand is billed each minute; longer-term reservation contracts are invoiced monthly. SSV storage is `$0.000096774 per GB per hour` (approximately `$0.10 per TB per hour`), public IP is `0.00672043 per hour`, and egress/ingress traffic is Free.

## Nebius

The table explicitly labels `Preemptible, GPU-hour` and `On-demand, GPU-hour`. L40S entries printed with `from` are stored as numeric floors and called out in notes. Storage includes Shared Filesystem `$0.0800 GiB/month`, WEKA `$0.1000 GiB/month`, Standard object volume `$0.0147 GiB/month`, Standard object egress `$0.0150/GiB`, and several other saved first-party rates. Networking egress/ingress is printed as Free. GB200 and GB300 cluster offerings with contact-only pricing were not emitted.

## Together AI GPU clusters

The cluster hardware table explicitly says `All prices per gpu per hour`. On-demand and each published reservation duration are separate rows. The `181+` duration is contact-only and has no number. Managed shared-filesystem storage is `$0.16` per GiB-month. No egress rate was found on the captured page.

## AWS

Capacity Block rows use the parenthesized AWS per-accelerator figure, not the whole-instance total. P5 on-demand rows use the official EC2 metered-unit map and are per p5.48xlarge node with 8 H100 GPUs. EC2 on-demand has a 60-second minimum and no long-term commitment. Same-region cross-AZ and public/Elastic IPv4 transfer is `$0.01/GB in each direction`; EBS has separate pricing. No current P6, P5e, or P5en on-demand keys were present in the captured official EC2 map.

## Google Cloud

Accelerator-optimized machine prices are per node using the printed machine type and GPU component count. Attachable GPU and Virtual Workstation tables explicitly say `GPU price (USD)` and are per GPU. The selected region printed by the captured page is Iowa (`us-central1`). DWS Flex-start and DWS Calendar Mode columns were not forced into spot/reserved because those products do not map cleanly to the required tier enum. The malformed `g2-standard-24-spot` cell contains no numeric rate and was omitted.

## FETCH STATUS LEDGER

Every raw HTTP request made for this lane returned HTTP 200. Saved bodies:

- HTTP 200 | https://www.runpod.io/pricing | evidence/runpod-pricing.html
- HTTP 200 | https://lambda.ai/pricing | evidence/lambda-pricing.html
- HTTP 200 | https://www.coreweave.com/pricing | evidence/coreweave-pricing.html
- HTTP 200 | https://vast.ai/pricing | evidence/vast-pricing.html
- HTTP 200 | https://www.hyperstack.cloud/gpu-pricing | evidence/hyperstack-gpu-pricing.html
- HTTP 200 | https://nebius.com/prices | evidence/nebius-prices.html
- HTTP 200 | https://www.together.ai/pricing | evidence/together-pricing.html
- HTTP 200 | https://aws.amazon.com/ec2/capacityblocks/pricing/ | evidence/aws-capacity-blocks-pricing.html
- HTTP 200 | https://cloud.google.com/compute/gpus-pricing | evidence/google-gpu-pricing.html
- HTTP 200 | https://vast.ai/_next/static/chunks/pages/pricing-6583595ef438a320.js | evidence/vast-pricing-page.js
- HTTP 200 | https://vast.ai/_next/static/chunks/2827-132b2e2e745e256c.js | evidence/vast-pricing-components.js
- HTTP 200 | https://vast.ai/_next/static/chunks/webpack-31ac7c827ed334bc.js | evidence/vast-webpack.js
- HTTP 200 | https://vast.ai/_next/static/chunks/7881.2eabab5515a3d7d7.js | evidence/vast-live-gpu-prices.js
- HTTP 200 | https://vast.ai/_next/static/chunks/128.adf0bc4ee1ee5409.js | evidence/vast-pricing-calculator.js
- HTTP 200 | https://vast.ai/_next/static/chunks/4232.c71e74bf90ae20fd.js | evidence/vast-gpu-card.js
- HTTP 200 | https://storage.googleapis.com/vast-public-gpu-pricing/gpu-pricing-public.json | evidence/vast-gpu-pricing-public.json
- HTTP 200 | https://aws.amazon.com/ec2/pricing/on-demand/ | evidence/aws-ec2-on-demand.html
- HTTP 200 | https://aws.amazon.com/ec2/instance-types/p5/ | evidence/aws-p5-instances.html
- HTTP 200 | https://aws.amazon.com/ec2/instance-types/p6/ | evidence/aws-p6-instances.html
- HTTP 200 | https://pricing-table.us-west-2.prod.site.p.awsstatic.com/ | evidence/aws-pricing-widget.html
- HTTP 200 | https://pricing-table.us-west-2.prod.site.p.awsstatic.com/runtime.988787f66552a78f8dec.js | evidence/aws-pricing-runtime.js
- HTTP 200 | https://pricing-table.us-west-2.prod.site.p.awsstatic.com/main.78febbab6955eaf11ea8.js | evidence/aws-pricing-main.js
- HTTP 200 | https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2.json | evidence/aws-ec2-metered-unit-map.json
- HTTP 200 | https://cloud.google.com/products/compute/pricing/accelerator-optimized | evidence/google-accelerator-optimized-pricing.html
- HTTP 200 | https://cloud.google.com/products/compute/pricing | evidence/google-compute-all-pricing.html
- HTTP 200 | https://cloud.google.com/spot-vms/pricing | evidence/google-spot-vms-pricing.html

## PAGES I COULD NOT FETCH

None. All requested starting URLs and all official follow-up URLs used in this lane returned HTTP 200. A successful fetch did not always mean the static HTML contained usable prices; Vast.ai is the key example.

## THINGS I COULD NOT VERIFY

- Vast.ai: the official live pricing endpoint does not state whether its min/median values are per GPU or per machine and does not label their tier. No Vast rates were put in `findings.json`.
- Hyperstack: the per-GPU versus per-node unit is unstated for every rate; all Hyperstack rows are `UNCLEAR`. Its reservation table also gives no minimum term.
- Lambda 1-Click Clusters: `Price per hour` is not explicitly per GPU or per cluster; all six numeric cluster rows are `UNCLEAR`.
- Google Cloud: DWS Flex-start and Calendar Mode prices do not fit the required `on_demand | spot | reserved` enum without interpretation, so they were omitted. The `g2-standard-24` Spot cell is nonnumeric (`g2-standard-24-spot`).
- AWS: the current official EC2 metered-unit map contained p5.48xlarge on-demand prices but no P6, P5e, P5en, or p5.4xlarge on-demand keys. Those missing on-demand rates were not invented.
- Contact-only products were not emitted as numeric rows: CoreWeave reserved capacity, Nebius GB200/GB300 clusters, Together 181+ day clusters, and other contact-sales entries.
- RunPod: the visible table and embedded JSON-LD disagree for a few values; the visible table values were used because they are the actual page table. The conflict is preserved in the raw HTML.
