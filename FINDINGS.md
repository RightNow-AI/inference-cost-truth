# Hidden costs and constraints

All exact limits, commitments, retention periods, SLA percentages, fees, and billing increments are in `findings.json`. Each provider row uses aligned `evidence_file`, `evidence_literal`, `source_url`, and `http_status` arrays so every reported number can be checked against a saved first-party response.

## Transparency summary

Together AI was the most complete hosted-open provider for this question: its official material covered dynamic rate limits, access funding, free-trial status, billing, retention controls, training, and a provisioned-service SLA. OpenAI, Google Gemini, Anthropic, Fireworks AI, RunPod, and Baseten also published useful detail across several requested fields.

The least transparent were TensorWave, whose public pages established only an hourly GPU pricing unit; CoreWeave, whose captured public pages did not expose numeric object-storage, egress, or SLA terms; and providers whose public docs withheld the exact default account limit table, notably Mistral, Novita AI, and DeepSeek. An honest `not documented` is used wherever the requested fact was absent.

## Closed vendors

### OpenAI

Published tier qualification, prepaid-credit rules, default retention, zero-retention eligibility, and API-training policy. Exact model-specific limits for the new account were delegated to the account limits page, and no public uptime SLA was verified.

### Anthropic

Published the new commercial tier's model limit table, retention and ZDR rules, training policy, and the status of its priority service tier. Minimum spend, free credits, and ordinary payment terms were not verified.

### Google Gemini

Published named usage tiers, tier qualifications, prepayment behavior, credit expiry, retention exceptions, and paid-service training policy. Exact default model limits remain account- and model-specific, and no public uptime SLA was verified.

### xAI

Published default-tier model limits, hybrid credit/invoice behavior, default retention, self-service ZDR, and an API-training statement. Minimum spend and an uptime SLA were not verified.

### Mistral

Published its free and paid API modes, automatic monthly charging, invoice terms, and training exceptions. Exact new-account RPM/TPM, the normal paid-API retention duration, and a public SLA percentage were not verified.

### DeepSeek

Published concurrency and queue-time behavior, balance/prepayment language, and general-service privacy and training terms. RPM/TPM, an API-specific ZDR option, and an uptime SLA were not verified.

### Cohere

Published trial and production request limits, free trial-key use, deletion timing, enterprise ZDR requirements, and different training treatment for enterprise versus trial/research use. TPM, payment model, and an uptime SLA were not verified.

## Hosted open models

### Together AI

Published dynamic-limit behavior, minimum platform funding, lack of a free trial, prepaid billing, no-retention controls, training policy, and provisioned-throughput service commitments. It does not publish a fixed default RPM/TPM table for serverless use.

### Fireworks AI

Published account and token ceilings, spending-tier qualification, prepaid billing, retention behavior, and the absence of a multi-tenant serverless SLA. Training-on-inputs policy and a minimum credit purchase were not verified.

### DeepInfra

Published concurrency, top-up, recurring free-credit, balance, in-memory inference handling, and training-policy details. An uptime SLA and serverless storage/request surcharges were not verified.

### Groq

Published model-specific developer limits, progressive billing thresholds, default inference handling, abuse-log retention, and customer-accessible ZDR. Free-tier entitlement, minimum spend, training policy, and an uptime SLA were not verified.

### Cerebras

Published free and developer limit tables, activation requirements, free credits, expiry, and prepaid behavior. Retention, training, and SLA terms were not verified from a working official privacy page.

### Baseten

Published account-tier RPM/TPM, invoice timing, minute-based billing, billable cold starts, and cold-start guidance. Free credits, retention, training, and SLA terms were not verified.

### Novita AI

Published funding-tier qualifications, a promotional voucher reference, automatic top-ups, a personal-information training statement, included storage, and a serverless billing unit. The static page did not expose the tier RPM/TPM table; API-specific retention and SLA terms were not verified.

### Nebius AI Studio

Published an illustrative baseline and directed users to the dashboard for exact limits. It also published prepaid-credit expiry, storage opt-out, and speculative-decoding training behavior. Default retention duration and an uptime SLA were not verified.

## GPU rental

### RunPod

Published deployment funding requirements, term commitments, balance behavior, ingress/egress treatment, storage prices, per-second compute/storage billing, and cold-start metric definitions. No numeric cold-start duration or uptime SLA was verified.

### Lambda

Published card pre-authorization, weekly invoicing, filesystem pricing, no filesystem ingress/egress charge, and instance/filesystem billing boundaries. Retention, training, SLA, and cold-start terms were not verified.

### CoreWeave

Published capacity-plan commitment behavior, GPU-hour inference measurement, storage measurement cadence, and short-interval capacity attribution. Numeric object-storage/egress pricing and a working public SLA percentage were not verified.

### Vultr

Published an uptime guarantee, included object-storage capacity and transfer, overage/storage charges, hourly minimum billing, and treatment of stopped resources. Data handling, training, payment model, and cold-start terms were not verified.

### Nebius

Published compute service level, object-storage and egress pricing, and second-level GPU billing with an hourly pricing unit. Payment, privacy/training, and cold-start terms were not verified.

### Hyperstack

The static documentation routes were JavaScript shells, but their official route chunks published prepaid and contract billing behavior, volume-storage pricing, hourly resource billing, and continued stopped-VM billing. Egress, SLA, privacy/training, and cold-start terms were not verified.

### TensorWave

The public accelerator pages established that prices are quoted per GPU hour. Minimum rental duration, finer billing granularity, storage/egress, payment, privacy/training, SLA, and cold-start terms were not verified.

## PAGES I COULD NOT FETCH

- `https://docs.mistral.ai/admin/billing-usage/usage-limits.md` — HTTP 404 with a custom not-found HTML body; the working HTML route was captured instead.
- `https://docs.mistral.ai/admin/billing-usage/billing.md` — HTTP 404 with a custom not-found HTML body; the working HTML route was captured instead.
- `https://docs.mistral.ai/admin/billing-usage/subscriptions.md` — HTTP 404 with a custom not-found HTML body; the working HTML route was captured instead.
- `https://inference-docs.cerebras.ai/security/data-privacy.md` — HTTP 404 with a minimal response body.
- `https://docs.baseten.co/security/data-and-privacy.md` — HTTP 404 with a minimal response body.
- `https://www.coreweave.com/legal/sla` — HTTP 404/custom not-found page.

## THINGS I COULD NOT VERIFY

- Exact new-paying-account RPM and TPM when the provider exposes them only inside an authenticated dashboard or returns a dynamic account-specific value.
- A default retention duration when a page documented ZDR or opt-out behavior but did not state the normal retention period.
- An enterprise requirement for an SLA unless the official page explicitly connected the SLA to that plan.
- Numeric cold-start/model-load times for providers that documented only the concept, monitoring percentile, or optimization guidance.
- CoreWeave numeric object-storage and egress prices: the official pricing page was fetched successfully, but those figures were absent from the static body and no usable first-party pricing payload was found.
- Hyperstack's human-facing billing routes returned `NOT_IN_STATIC_HTML`; official JavaScript route chunks were saved and used, but no numeric egress rate was present.
- Novita AI's tier RPM/TPM values: tier qualification text was present, but the actual limit table was not in the captured static response.
- API-input training treatment where a privacy page discussed only personal information or general service data rather than prompts and outputs specifically.
