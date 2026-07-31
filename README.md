# inference-cost-truth

What LLM inference actually costs, per million tokens, across closed APIs,
hosted open-model APIs, and self-hosted GPUs. Every price carries a source URL
and the date it was read. Verified on **2026-07-31**.

**Who maintains this and why that matters.** This repo is maintained by
RightNow AI, which sells GPU kernel optimization at
[runinfra.ai](https://runinfra.ai). We make money when people run models on
their own GPUs. That is a direct conflict of interest with the question this
repo answers, so read the numbers adversarially.

The finding that cuts against us is in the head-to-head table below. **At 30%
utilization, which is generous for most real deployments, buying the open model
from a hosted API is cheaper than renting GPUs to serve it yourself in every
comparison we could make.** Self-hosting only pulls ahead at 90% utilization,
on the cheapest AMD capacity we could find a published rate for, and even then
only for two of three models. Before counting a single hour of engineer time.

## What this repo is not

- Not a quality benchmark. Nothing here says which model is better.
- Not a recommendation. Your latency floor, data rules, and team size decide
  more than price does.
- Not a claim about anyone's internal costs or margins. There is no markup
  column and there will never be one. Nobody outside a provider knows what it
  costs them to serve a token, and estimating it from public GPU rates is a
  guess dressed as arithmetic.
- Not complete. Blank cells marked "not documented" or "not measured" are
  correct output. A gap with a reason beats a number with none.

## TL;DR

Three categories, one capability tier each, cheapest verified option per
category. Full tables below.

| Tier | A: closed vendor API | B: open model, hosted API | C: open model, self-hosted |
|---|---|---|---|
| Frontier | `gpt-5.6-sol` $5 in / $30 out | no open model at this tier | not applicable |
| Strong general | `Claude Sonnet 5` $2 in / $10 out | `DeepSeek-V3.2` on DeepInfra $0.26 in / $0.38 out | DeepSeek-R1 on 4x MI355X, $1.97 out at 90% util, $5.91 at 30% |
| Cheap general | `deepseek-v4-flash` $0.14 in / $0.28 out | `gpt-oss-120b` on Novita $0.05 in / $0.25 out | Llama-3.3-70B on 1x MI355X, $0.82 out at 90% util, $2.47 at 30% |

**Category B is usually the right answer** and it is the one most comparisons
skip, because "GPT-4 versus self-hosting" is a more exciting headline than
"someone else already runs the open model cheaper than you can".

## Head to head: the same open model, API versus your own GPUs

The only truly like-for-like comparison in this repo. Same weights, same model
id, cheapest published option on each side. Self-host column is the cheapest
GPU rental we found a published on-demand per-GPU rate for.

| Open model | Cheapest hosted API out /1M | Cheapest self-host | Self-host @90% | @60% | @30% | Winner @90% | Winner @30% |
|---|---|---|---|---|---|---|---|
| `DeepSeek-R1-0528` | $2.15 (DeepInfra) | 4x MI355X on Vultr | $1.97 | $2.95 | $5.91 | self-host | **API** |
| `MiniMax-M3` | $1.2 (Nebius AI Studio) | 4x MI355X on Vultr | $0.84 | $1.26 | $2.51 | self-host | **API** |
| `Llama-3.3-70B-Instruct` | $0.32 (DeepInfra) | 1x MI355X on Vultr | $0.82 | $1.24 | $2.47 | **API** | **API** |

Two things to take from this. First, the utilization column you believe about
yourself decides the answer, and it is the number teams are most optimistic
about. Second, self-hosting wins here only on AMD MI355X at $2.59/GPU/hr, which
is less than half the cheapest B200 rate we found, while delivering higher
measured throughput on DeepSeek-R1. If you are going to self-host, the
accelerator you pick matters more than the model does.

## Nine things this data says that the comparisons get wrong

Each of these is derived from the tables below, not from anyone's opinion.

**1. The same open weights cost up to 3.2x more depending on who runs them.**
Identical model id, identical weights, standard tier, one API call away from
each other. This is the cheapest saving on this page and it requires changing a
base URL.

| Open model | Providers | Cheapest output /1M | Dearest output /1M | Spread |
|---|---|---|---|---|
| `meta-llama/llama-3.3-70b-instruct` | 4 | $0.32 (DeepInfra) | $1.04 (Together AI) | **3.2x** |
| `openai/gpt-oss-120b` | 6 | $0.25 (Novita AI) | $0.75 (Cerebras) | **3.0x** |
| `google/gemma-4-31b-it` | 4 | $0.34 (DeepInfra) | $0.97 (Together AI) | **2.9x** |
| `qwen/qwen3.7-max` | 3 | $3.75 (Novita AI) | $7.5 (DeepInfra) | **2.0x** |
| `openai/gpt-oss-20b` | 3 | $0.15 (Novita AI) | $0.3 (Groq) | **2.0x** |
| `google/gemma-3-27b-it` | 3 | $0.16 (DeepInfra) | $0.3 (Nebius AI Studio) | **1.9x** |
| `moonshotai/kimi-k2.6` | 4 | $3.4 (Novita AI) | $4.5 (Together AI) | **1.3x** |
| `qwen/qwen3-235b-a22b-instruct-2507` | 3 | $0.55 (DeepInfra) | $0.6 (Nebius AI Studio) | **1.1x** |

**2. Your batching config moves cost more than your GPU choice does.** Same
model, same 2x H100, same rental rate. Only concurrency changes:

| Total output tok/s | @90% util | @60% | @30% | @10% |
|---|---|---|---|---|
| 658 | $1.867 | $2.800 | $5.601 | $16.803 |
| 998 | $1.230 | $1.846 | $3.692 | $11.075 |
| 1,385 | $0.887 | $1.330 | $2.660 | $7.980 |
| 1,825 | $0.673 | $1.010 | $2.019 | $6.058 |
| 2,282 | $0.538 | $0.807 | $1.615 | $4.845 |

That is a 3.5x swing in cost per token from a config flag. People agonise over
which accelerator to buy and then run it at concurrency 8.

**3. Reasoning tokens are the largest hidden multiplier in the whole stack.**
A 14.3x gap between the tokens you see and the tokens you pay for dwarfs every
price difference between vendors. Optimising your provider choice while
ignoring reasoning-token volume is optimising the wrong term.

**4. Cache writes are not free, and almost nobody accounts for them.** Across
the rows here that price it, writing a cache entry costs 1.25x the input rate
on 61 models and 2.0x on 16. If your prefix changes every request you are
paying a premium to populate a cache you never read.

**5. Tokenizer normalization barely matters for English and does matter for
code.** Measured across 10 tokenizers on fixed text: English spans 3.0%, code
spans 9.7%. The standard blog-post advice to normalize before comparing prices
is right in principle and nearly irrelevant for prose.

**6. Tier multipliers are not uniform, so you cannot derive one from another.**
Across OpenAI models, batch output is 0.5x standard on 41 models but 0.562x,
0.833x and 1.0x on three others; fast ranges 1.667x to 2.5x. Assuming "batch is
half" is wrong often enough to matter.

**7. Multi-tier pricing is a scraping trap, not just a pricing detail.**
Fireworks prints Standard and Priority as adjacent columns of one table. Take
the wrong column and every number is 50% high. We shipped that bug ourselves
and caught it in audit. Any comparison built by scraping is likely carrying it.

**8. If you self-host, the accelerator decides more than the model does.** AMD
MI355X at $2.59/GPU/hr is under half the cheapest B200 rate at $5.89, against
higher measured throughput on DeepSeek-R1. It is also the hardest rate to find:
none of the eight mainstream GPU providers we surveyed first published one.

**9. At any utilization you will actually hit, the API wins.** See the
head-to-head table. Self-hosting only wins at 90% utilization, and 90%
utilization means a saturated box, which means a queue, which means the latency
you were trying to avoid.

## API pricing, closed vendors

Standard realtime tier. Batch, flex, fast, and long-context tiers are separate
rows in `data/providers.json` and are never blended into these numbers. Prices
are USD per 1M tokens **of that model's own tokens** -- see the normalization
section, because a token is not a fixed amount of text.

| Vendor | Model | Input /1M | Cached in | Cache write | Output /1M | Batch out | Source |
|---|---|---|---|---|---|---|---|
| AI21 | `Jamba Large` | $2 | not documented | not documented | $8 | -- | [src](https://www.ai21.com/pricing) |
| AI21 | `Jamba Mini` | $0.2 | not documented | not documented | $0.4 | -- | [src](https://www.ai21.com/pricing) |
| Amazon Bedrock | `GPT-5.5` | $5.5 | $0.55 | not documented | $33 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `GPT-5.6 Sol` | $5.5 | $0.55 | $6.88 | $33 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Claude 3.5 Sonnet (Public Extended Access, Effective 1 Dec 2025)` | $6 | not documented | not documented | $30 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Claude 3.5 Sonnet v2 (Public Extended Access, Effective 1 Dec 2025)` | $6 | $0.6 | $7.5 | $30 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `GPT-5.4` | $2.75 | $0.275 | not documented | $16.5 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `GPT-5.6 Terra` | $2.2 | $0.22 | $2.75 | $13.2 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Palmyra X4` | $2.5 | not documented | not documented | $10 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Palmyra X5` | $0.6 | not documented | not documented | $6 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `GLM 5` | $1 | not documented | not documented | $3.2 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Kimi K2.5` | $0.6 | not documented | not documented | $3 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Qwen3 VL 235B A22B` | $0.53 | not documented | not documented | $2.66 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Llama 2 Chat (70B)` | $1.95 | not documented | not documented | $2.56 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Grok 4.3` | $1.25 | $0.2 | not documented | $2.5 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Kimi K2 Thinking` | $0.6 | not documented | not documented | $2.5 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `GLM 4.7` | $0.6 | not documented | not documented | $2.2 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Devstral 2 123B` | $0.4 | not documented | not documented | $2 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `DeepSeek v3.2` | $0.62 | not documented | not documented | $1.85 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Magistral Small 1.2` | $0.5 | not documented | not documented | $1.5 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Mistral Large 3` | $0.5 | not documented | not documented | $1.5 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `GPT-5.6 Luna` | $0.22 | $0.022 | $0.275 | $1.32 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Minimax M2` | $0.3 | not documented | not documented | $1.2 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Minimax M2.1` | $0.3 | not documented | not documented | $1.2 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `MiniMax M2.5` | $0.3 | not documented | not documented | $1.2 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Qwen3 Coder Next` | $0.5 | not documented | not documented | $1.2 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Qwen3 Next 80B A3B` | $0.15 | not documented | not documented | $1.2 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Llama 2 Chat (13B)` | $0.75 | not documented | not documented | $1 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `NVIDIA Nemotron 3 Super 120B A12B` | $0.15 | not documented | not documented | $0.65 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `NVIDIA Nemotron Nano 2 VL` | $0.2 | not documented | not documented | $0.6 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Palmyra Vision 7B` | $0.15 | not documented | not documented | $0.6 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Gemma 4 26B A4B` | $0.13 | not documented | not documented | $0.4 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Gemma 4 31B` | $0.14 | not documented | not documented | $0.4 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `GLM 4.7 Flash` | $0.07 | not documented | not documented | $0.4 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Gemma 3 27B` | $0.23 | not documented | not documented | $0.38 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Gemma 3 12B` | $0.09 | not documented | not documented | $0.29 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `NVIDIA Nemotron 3 Nano 30B A3B` | $0.06 | not documented | not documented | $0.24 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `NVIDIA Nemotron Nano 2` | $0.06 | not documented | not documented | $0.23 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Ministral 14B 3.0` | $0.2 | not documented | not documented | $0.2 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Ministral 8B 3.0` | $0.15 | not documented | not documented | $0.15 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Ministral 3B 3.0` | $0.1 | not documented | not documented | $0.1 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Gemma 3 4B` | $0.04 | not documented | not documented | $0.08 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Amazon Bedrock | `Gemma 4 E2B` | $0.04 | not documented | not documented | $0.08 | -- | [src](https://aws.amazon.com/bedrock/pricing/) |
| Anthropic | `Claude Fable 5` | $10 | $1 | $12.5 | $50 | -- | [src](https://platform.claude.com/docs/en/about-claude/pricing) |
| Anthropic | `Claude Mythos 5 (limited availability)` | $10 | $1 | $12.5 | $50 | -- | [src](https://platform.claude.com/docs/en/about-claude/pricing) |
| Anthropic | `Claude Opus 5` | $5 | $0.5 | $6.25 | $25 | -- | [src](https://platform.claude.com/docs/en/about-claude/pricing) |
| Anthropic | `Claude Opus 4.8` | $5 | $0.5 | $6.25 | $25 | -- | [src](https://platform.claude.com/docs/en/about-claude/pricing) |
| Anthropic | `Claude Opus 4.7` | $5 | $0.5 | $6.25 | $25 | -- | [src](https://platform.claude.com/docs/en/about-claude/pricing) |
| Anthropic | `Claude Opus 4.6` | $5 | $0.5 | $6.25 | $25 | -- | [src](https://platform.claude.com/docs/en/about-claude/pricing) |
| Anthropic | `Claude Opus 4.5` | $5 | $0.5 | $6.25 | $25 | -- | [src](https://platform.claude.com/docs/en/about-claude/pricing) |
| Anthropic | `Claude Sonnet 5` | $3 | $0.3 | $3.75 | $15 | -- | [src](https://platform.claude.com/docs/en/about-claude/pricing) |
| Anthropic | `Claude Sonnet 4.6` | $3 | $0.3 | $3.75 | $15 | -- | [src](https://platform.claude.com/docs/en/about-claude/pricing) |
| Anthropic | `Claude Sonnet 4.5` | $3 | $0.3 | $3.75 | $15 | -- | [src](https://platform.claude.com/docs/en/about-claude/pricing) |
| Anthropic | `Claude Haiku 4.5` | $1 | $0.1 | $1.25 | $5 | -- | [src](https://platform.claude.com/docs/en/about-claude/pricing) |
| Azure OpenAI | `GPT-5.4 Pro (>272k context length) Global` | $60 | not documented | not documented | $270 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.4 Pro (<272k context length) Global` | $30 | not documented | not documented | $180 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-4.5-Preview-2025-02-27 Global` | $75 | $37.5 | not documented | $150 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-4` | $60 | not documented | not documented | $120 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5 Pro Global` | $15 | not documented | not documented | $120 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.5 Global` | $12.5 | $1.25 | not documented | $75 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.6-sol (short context) Global` | $10 | $1 | $12.5 | $60 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `o1 2024-12-17 Global` | $15 | $7.5 | not documented | $60 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `o1 preview 2024-09-12 Global` | $15 | $7.5 | not documented | $60 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.5 Long Context Global` | $10 | $1 | not documented | $45 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.6-sol (long context) Global` | $10 | $1 | $12.5 | $45 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-4-Turbo` | $11 | not documented | not documented | $33 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-4-Turbo-Vision` | $11 | not documented | not documented | $33 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.4 (<272k context length) Global` | $5 | $0.5 | not documented | $30 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.6-terra (short context) Global` | $5 | $0.5 | $6.25 | $30 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-Chat Latest 05052026 Global` | $5 | $0.5 | not documented | $30 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.2 Global` | $3.5 | $0.35 | not documented | $28 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.3 Codex Global` | $3.5 | $0.35 | not documented | $28 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.4 (>272k context length) Global` | $5 | $0.5 | not documented | $22.5 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.6-terra (long context) Global` | $5 | $0.5 | $6.25 | $22.5 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5 2025-08-07 Global` | $2.5 | $0.25 | not documented | $20 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.1 Global` | $2.5 | $0.25 | not documented | $20 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-4o-2024-0513 Global` | $5 | not documented | not documented | $15 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-4.1-2025-04-14 Global` | $3.5 | $0.875 | not documented | $14 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.2 Codex Global` | $1.75 | $0.175 | not documented | $14 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.2-chat latest Global` | $1.75 | $0.175 | not documented | $14 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.3 Chat Global` | $1.75 | $0.175 | not documented | $14 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-4o-2024-08-06 Global` | $2.5 | $1.25 | not documented | $10 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-4o-2024-1120 Global` | $2.5 | $1.25 | not documented | $10 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5 chat Global` | $1.25 | $0.125 | not documented | $10 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5 Codex Global` | $1.25 | $0.125 | not documented | $10 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.1-chat Global` | $1.25 | $0.125 | not documented | $10 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.1-codex Global` | $1.25 | $0.125 | not documented | $10 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.1-codex-max Global` | $1.25 | $0.125 | not documented | $10 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.4 mini Global` | $1.5 | $0.15 | not documented | $9 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.6-luna (long context) Global` | $2 | $0.2 | $2.5 | $9 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `o3 2025-04-16 Global` | $2 | $0.5 | not documented | $8 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.6-luna (short context) Global` | $1 | $0.1 | $1.25 | $6 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `o1-mini 2024-09-12 Global` | $1.1 | $0.55 | not documented | $4.4 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `o3 mini 2025-01-31 Global` | $1.1 | $0.55 | not documented | $4.4 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `o4-mini 2025-04-16 Global` | $1.1 | $0.275 | not documented | $4.4 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-3.5-Turbo-0613` | $3 | not documented | not documented | $4 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5-mini Global` | $0.45 | $0.045 | not documented | $3.6 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-4.1-mini-2025-04-14 Global` | $0.7 | $0.175 | not documented | $2.8 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-3.5-Turbo-1106` | $1.1 | not documented | not documented | $2.2 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-3.5-Turbo-Instruct` | $1.65 | not documented | not documented | $2.2 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-3.5-Turbo-0301` | $1.5 | not documented | not documented | $2 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.1-codex-mini Global` | $0.25 | $0.025 | not documented | $2 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-3.5-Turbo-0125` | $0.55 | not documented | not documented | $1.65 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5.4 nano Global` | $0.2 | $0.02 | not documented | $1.25 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-4o-mini-0718 Global` | $0.15 | $0.075 | not documented | $0.6 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `gpt-oss-120b` | $0.15 | not documented | not documented | $0.6 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-4.1-nano-2025-04-14 Global` | $0.1 | $0.025 | not documented | $0.4 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Azure OpenAI | `GPT-5-nano Global` | $0.05 | $0.005 | not documented | $0.4 | -- | [src](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Cohere | `Command R+ 04-2024` | $3 | not documented | not documented | $15 | -- | [src](https://cohere.com/pricing) |
| Cohere | `Command A` | $2.5 | not documented | not documented | $10 | -- | [src](https://docs.cohere.com/docs/command-a) |
| Cohere | `Command R+` | $2.5 | not documented | not documented | $10 | -- | [src](https://docs.cohere.com/docs/command-r-plus) |
| Cohere | `Command R+ 08-2024` | $2.5 | not documented | not documented | $10 | -- | [src](https://cohere.com/pricing) |
| Cohere | `Command` | $1 | not documented | not documented | $2 | -- | [src](https://cohere.com/pricing) |
| Cohere | `Aya Expanse 32B` | $0.5 | not documented | not documented | $1.5 | -- | [src](https://cohere.com/pricing) |
| Cohere | `Aya Expanse 8B` | $0.5 | not documented | not documented | $1.5 | -- | [src](https://cohere.com/pricing) |
| Cohere | `Command R 03-2024` | $0.5 | not documented | not documented | $1.5 | -- | [src](https://cohere.com/pricing) |
| Cohere | `Command R` | $0.15 | not documented | not documented | $0.6 | -- | [src](https://docs.cohere.com/docs/command-r) |
| Cohere | `Command-light` | $0.3 | not documented | not documented | $0.6 | -- | [src](https://cohere.com/pricing) |
| Cohere | `Command R7B` | $0.0375 | not documented | not documented | $0.15 | -- | [src](https://docs.cohere.com/docs/command-r7b) |
| DeepSeek | `deepseek-v4-pro` | $0.435 | $0.003625 | not documented | $0.87 | -- | [src](https://api-docs.deepseek.com/quick_start/pricing/) |
| DeepSeek | `deepseek-v4-flash` | $0.14 | $0.0028 | not documented | $0.28 | -- | [src](https://api-docs.deepseek.com/quick_start/pricing/) |
| Google Gemini | `Gemini 3.1 Pro Preview` | $4 | $0.4 | not documented | $18 | -- | [src](https://ai.google.dev/gemini-api/docs/pricing) |
| Google Gemini | `Gemini 2.5 Pro` | $2.5 | $0.25 | not documented | $15 | -- | [src](https://ai.google.dev/gemini-api/docs/pricing) |
| Google Gemini | `Gemini 3.5 Flash` | $1.5 | $0.15 | not documented | $9 | -- | [src](https://ai.google.dev/gemini-api/docs/pricing) |
| Google Gemini | `Gemini Omni Flash Preview` | $1.5 | not documented | not documented | $9 | -- | [src](https://ai.google.dev/gemini-api/docs/pricing) |
| Google Gemini | `Gemini 3.6 Flash` | $1.5 | $0.15 | not documented | $7.5 | -- | [src](https://ai.google.dev/gemini-api/docs/pricing) |
| Google Gemini | `Gemini 3 Flash Preview` | $0.5 | $0.05 | not documented | $3 | -- | [src](https://ai.google.dev/gemini-api/docs/pricing) |
| Google Gemini | `Gemini 3.5 Flash-Lite` | $0.3 | $0.03 | not documented | $2.5 | -- | [src](https://ai.google.dev/gemini-api/docs/pricing) |
| Google Gemini | `Gemini 2.5 Flash` | $0.3 | $0.03 | not documented | $2.5 | -- | [src](https://ai.google.dev/gemini-api/docs/pricing) |
| Google Gemini | `Gemini 3.1 Flash-Lite` | $0.25 | $0.025 | not documented | $1.5 | -- | [src](https://ai.google.dev/gemini-api/docs/pricing) |
| Google Gemini | `Gemini 2.5 Flash-Lite` | $0.1 | $0.01 | not documented | $0.4 | -- | [src](https://ai.google.dev/gemini-api/docs/pricing) |
| Google Gemini | `Gemini 2.5 Flash-Lite Preview` | $0.1 | $0.01 | not documented | $0.4 | -- | [src](https://ai.google.dev/gemini-api/docs/pricing) |
| Google Gemini | `Gemini 2.0 Flash` | $0.1 | $0.025 | not documented | $0.4 | -- | [src](https://ai.google.dev/gemini-api/docs/pricing) |
| Google Gemini | `Gemini 2.0 Flash-Lite` | $0.075 | not documented | not documented | $0.3 | -- | [src](https://ai.google.dev/gemini-api/docs/pricing) |
| Google Vertex AI | `Claude Fable 5 (long-context pricing)` | $10 | $1 | $12.5 | $50 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Claude Fable 5 (short-context pricing)` | $10 | $1 | $12.5 | $50 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Claude Opus 4.5 (short-context pricing)` | $5 | $0.5 | $6.25 | $25 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Claude Opus 4.6 (long-context pricing)` | $5 | $0.5 | $6.25 | $25 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Claude Opus 4.6 (short-context pricing)` | $5 | $0.5 | $6.25 | $25 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Claude Opus 4.7 (long-context pricing)` | $5 | $0.5 | $6.25 | $25 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Claude Opus 4.7 (short-context pricing)` | $5 | $0.5 | $6.25 | $25 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Claude Opus 4.8 (long-context pricing)` | $5 | $0.5 | $6.25 | $25 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Claude Opus 4.8 (short-context pricing)` | $5 | $0.5 | $6.25 | $25 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Opus 5 (long-context pricing)` | $5 | $0.5 | $6.25 | $25 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Opus 5 (short-context pricing)` | $5 | $0.5 | $6.25 | $25 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 3.1 Pro Preview (long-context pricing)` | $4 | $0.4 | not documented | $18 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Claude Sonnet 4.5 (short-context pricing)` | $3 | $0.3 | $3.75 | $15 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Claude Sonnet 4.6 (long-context pricing)` | $3 | $0.3 | $3.75 | $15 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Claude Sonnet 4.6 (short-context pricing)` | $3 | $0.3 | $3.75 | $15 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Claude Sonnet 5 (Standard Price beginning September 1st, 2026) (long-context pricing)` | $3 | $0.3 | $3.75 | $15 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Claude Sonnet 5 (Standard Price beginning September 1st, 2026) (short-context pricing)` | $3 | $0.3 | $3.75 | $15 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 2.5 Pro (long-context pricing)` | $2.5 | $0.25 | not documented | $15 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 3.1 Pro Preview (short-context pricing)` | $2 | $0.2 | not documented | $12 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Claude Sonnet 5 (Promotional Price through August 31, 2026) (long-context pricing)` | $2 | $0.2 | $2.5 | $10 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Claude Sonnet 5 (Promotional Price through August 31, 2026) (short-context pricing)` | $2 | $0.2 | $2.5 | $10 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 2.5 Pro (short-context pricing)` | $1.25 | $0.13 | not documented | $10 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 3.5 Flash (long-context pricing)` | $1.5 | $0.15 | not documented | $9 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 3.5 Flash (short-context pricing)` | $1.5 | $0.15 | not documented | $9 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini Omni Flash` | $1.5 | not documented | not documented | $9 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 3.6 Flash (long-context pricing)` | $1.5 | $0.15 | not documented | $7.5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 3.6 Flash (short-context pricing)` | $1.5 | $0.15 | not documented | $7.5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `DeepSeek-R1 (0528)` | $1.35 | not documented | not documented | $5.4 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Claude Haiku 4.5 (short-context pricing)` | $1 | $0.1 | $1.25 | $5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Grok 4.20 Non-Reasoning (long-context pricing)` | $2.5 | $0.4 | not documented | $5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Grok 4.20 Reasoning (long-context pricing)` | $2.5 | $0.4 | not documented | $5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Grok 4.3 (long-context pricing)` | $2.5 | $0.4 | not documented | $5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `GLM-5 *` | $1 | $0.1 | not documented | $3.2 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 3 Flash Preview (long-context pricing)` | $0.5 | $0.05 | not documented | $3 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 3 Flash Preview (short-context pricing)` | $0.5 | $0.05 | not documented | $3 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 2.5 Flash (long-context pricing)` | $0.3 | $0.03 | not documented | $2.5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 2.5 Flash (short-context pricing)` | $0.3 | $0.03 | not documented | $2.5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 3.5 Flash-Lite (long-context pricing)` | $0.3 | $0.03 | not documented | $2.5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 3.5 Flash-Lite (short-context pricing)` | $0.3 | $0.03 | not documented | $2.5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Grok 4.20 Non-Reasoning (short-context pricing)` | $1.25 | $0.2 | not documented | $2.5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Grok 4.20 Reasoning (short-context pricing)` | $1.25 | $0.2 | not documented | $2.5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Grok 4.3 (short-context pricing)` | $1.25 | $0.2 | not documented | $2.5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Kimi-K2-Thinking` | $0.6 | $0.06 | not documented | $2.5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `GLM-4.7` | $0.6 | not documented | not documented | $2.2 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 2.0 Flash Live API` | $0.5 | not documented | not documented | $2 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 2.5 Flash Live API (long-context pricing)` | $0.5 | not documented | not documented | $2 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 2.5 Flash Live API (short-context pricing)` | $0.5 | not documented | not documented | $2 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Mistral Medium 3` | $0.4 | not documented | not documented | $2 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Qwen3-Coder-480B-A35B-Instruct` | $0.22 | $0.022 | not documented | $1.8 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `DeepSeek-V3.1` | $0.6 | $0.06 | not documented | $1.7 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `DeepSeek-V3.2` | $0.56 | $0.056 | not documented | $1.68 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 3.1 Flash-Lite (long-context pricing)` | $0.25 | $0.025 | not documented | $1.5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 3.1 Flash-Lite (short-context pricing)` | $0.25 | $0.025 | not documented | $1.5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `MiniMax-M2` | $0.3 | $0.03 | not documented | $1.2 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Qwen3-Next-80B-Instruct` | $0.15 | not documented | not documented | $1.2 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Qwen3-Next-80B-Thinking` | $0.15 | not documented | not documented | $1.2 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Llama 4 Maverick` | $0.35 | not documented | not documented | $1.15 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Codestral 2` | $0.3 | not documented | not documented | $0.9 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Qwen3-235B-A22B-Instruct-2507` | $0.22 | not documented | not documented | $0.88 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Llama 3.3 70B` | $0.72 | not documented | not documented | $0.72 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Llama 4 Scout` | $0.25 | not documented | not documented | $0.7 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 2.0 Flash` | $0.15 | not documented | not documented | $0.6 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemma 4 26B` | $0.15 | $0.015 | not documented | $0.6 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Grok 4.1 Fast Non-Reasoning` | $0.2 | $0.05 | not documented | $0.5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Grok 4.1 Fast Reasoning` | $0.2 | $0.05 | not documented | $0.5 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 2.5 Flash Lite (long-context pricing)` | $0.1 | $0.01 | not documented | $0.4 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 2.5 Flash Lite (short-context pricing)` | $0.1 | $0.01 | not documented | $0.4 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `gpt-oss-120b` | $0.09 | not documented | not documented | $0.36 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Gemini 2.0 Flash Lite` | $0.075 | not documented | not documented | $0.3 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `Mistral Small 3.1 (25.03)` | $0.1 | not documented | not documented | $0.3 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Google Vertex AI | `gpt-oss-20b` | $0.07 | $0.007 | not documented | $0.25 | -- | [src](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Mistral | `Mistral Medium 3.5` | $1.5 | not documented | not documented | $7.5 | -- | [src](https://mistral.ai/pricing/api/) |
| Mistral | `Mixtral 8x22B` | $2 | not documented | not documented | $6 | -- | [src](https://mistral.ai/pricing/api/) |
| Mistral | `Magistral Medium` | $2 | not documented | not documented | $5 | -- | [src](https://mistral.ai/pricing/api/) |
| Mistral | `Devstral 2` | $0.4 | not documented | not documented | $2 | -- | [src](https://mistral.ai/pricing/api/) |
| Mistral | `Mistral Large 3` | $0.5 | not documented | not documented | $1.5 | -- | [src](https://mistral.ai/pricing/api/) |
| Mistral | `Magistral Small` | $0.5 | not documented | not documented | $1.5 | -- | [src](https://mistral.ai/pricing/api/) |
| Mistral | `Codestral` | $0.3 | not documented | not documented | $0.9 | -- | [src](https://mistral.ai/pricing/api/) |
| Mistral | `Mixtral 8x7B` | $0.7 | not documented | not documented | $0.7 | -- | [src](https://mistral.ai/pricing/api/) |
| Mistral | `Mistral Small 4` | $0.15 | not documented | not documented | $0.6 | -- | [src](https://mistral.ai/pricing/api/) |
| Mistral | `Devstral Small 2` | $0.1 | not documented | not documented | $0.3 | -- | [src](https://mistral.ai/pricing/api/) |
| Mistral | `Ministral 3 - 14B` | $0.2 | not documented | not documented | $0.2 | -- | [src](https://mistral.ai/pricing/api/) |
| Mistral | `Ministral 3 - 8B` | $0.15 | not documented | not documented | $0.15 | -- | [src](https://mistral.ai/pricing/api/) |
| Mistral | `Mistral NeMo` | $0.15 | not documented | not documented | $0.15 | -- | [src](https://mistral.ai/pricing/api/) |
| Mistral | `Ministral 3 - 3B` | $0.1 | not documented | not documented | $0.1 | -- | [src](https://mistral.ai/pricing/api/) |
| OpenAI | `o1-pro` | $150 | not documented | not documented | $600 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5.5-pro (<272K context length)` | $30 | not documented | not documented | $180 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5.4-pro (<272K context length)` | $30 | not documented | not documented | $180 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5.2-pro` | $21 | not documented | not documented | $168 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5-pro` | $15 | not documented | not documented | $120 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `o3-pro` | $20 | not documented | not documented | $80 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5.5-cyber` | $12.5 | $1.25 | not documented | $75 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `o1` | $15 | $7.5 | not documented | $60 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-4-0613` | $30 | not documented | not documented | $60 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5.6-sol` | $5 | $0.5 | $6.25 | $30 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5.5 (<272K context length)` | $5 | $0.5 | not documented | $30 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-4-turbo-2024-04-09` | $10 | not documented | not documented | $30 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `chat-latest` | $5 | $0.5 | not documented | $30 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `o4-mini-2025-04-16` | $4 | $1 | not documented | $16 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5.4 (<272K context length)` | $2.5 | $0.25 | not documented | $15 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-4o-2024-05-13` | $5 | not documented | not documented | $15 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-4o-2024-08-06` | $3.75 | $1.875 | not documented | $15 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5.2` | $1.75 | $0.175 | not documented | $14 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5.3-chat-latest` | $1.75 | $0.175 | not documented | $14 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5.2-chat-latest` | $1.75 | $0.175 | not documented | $14 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5.3-codex` | $1.75 | $0.175 | not documented | $14 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5.6-terra` | $2 | $0.2 | $2.5 | $12 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-4.1-2025-04-14` | $3 | $0.75 | not documented | $12 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `davinci-002 Legacy` | $12 | not documented | not documented | $12 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5.1` | $1.25 | $0.125 | not documented | $10 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5` | $1.25 | $0.125 | not documented | $10 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-4o` | $2.5 | $1.25 | not documented | $10 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-4.1` | $2 | $0.5 | not documented | $8 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `o3` | $2 | $0.5 | not documented | $8 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `o4-mini-2025-04-16 with data sharing` | $2 | $0.5 | not documented | $8 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-3.5-turbo Legacy` | $3 | not documented | not documented | $6 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5.4-mini` | $0.75 | $0.075 | not documented | $4.5 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `o4-mini` | $1.1 | $0.275 | not documented | $4.4 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `o3-mini` | $1.1 | $0.55 | not documented | $4.4 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-4.1-mini-2025-04-14` | $0.8 | $0.2 | not documented | $3.2 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5-mini` | $0.25 | $0.025 | not documented | $2 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-3.5-turbo-1106` | $1 | not documented | not documented | $2 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-3.5-turbo-instruct` | $1.5 | not documented | not documented | $2 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `davinci-002` | $2 | not documented | not documented | $2 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-4.1-mini` | $0.4 | $0.1 | not documented | $1.6 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `babbage-002 Legacy` | $1.6 | not documented | not documented | $1.6 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-3.5-turbo` | $0.5 | not documented | not documented | $1.5 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-3.5-turbo-0125` | $0.5 | not documented | not documented | $1.5 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5.4-nano` | $0.2 | $0.02 | not documented | $1.25 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5.6-luna` | $0.2 | $0.02 | $0.25 | $1.2 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-4o-mini-2024-07-18` | $0.3 | $0.15 | not documented | $1.2 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-4.1-nano-2025-04-14` | $0.2 | $0.05 | not documented | $0.8 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-4o-mini` | $0.15 | $0.075 | not documented | $0.6 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-5-nano` | $0.05 | $0.005 | not documented | $0.4 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `gpt-4.1-nano` | $0.1 | $0.025 | not documented | $0.4 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| OpenAI | `babbage-002` | $0.4 | not documented | not documented | $0.4 | -- | [src](https://developers.openai.com/api/docs/pricing) |
| Perplexity | `Sonar Pro` | $3 | not documented | not documented | $15 | -- | [src](https://docs.perplexity.ai/docs/getting-started/pricing) |
| Perplexity | `Sonar Reasoning Pro` | $2 | not documented | not documented | $8 | -- | [src](https://docs.perplexity.ai/docs/getting-started/pricing) |
| Perplexity | `Sonar` | $1 | not documented | not documented | $1 | -- | [src](https://docs.perplexity.ai/docs/getting-started/pricing) |
| Reka | `Reka Core` | $2 | not documented | not documented | $6 | -- | [src](https://docs.reka.ai/pricing) |
| Reka | `Reka Flash` | $0.8 | not documented | not documented | $2 | -- | [src](https://docs.reka.ai/pricing) |
| Reka | `Reka Edge` | $0.1 | not documented | not documented | $0.1 | -- | [src](https://docs.reka.ai/pricing) |
| xAI | `grok-4.5 (long context)` | $4 | $0.6 | not documented | $12 | -- | [src](https://docs.x.ai/developers/pricing) |
| xAI | `Grok 4.5` | $2 | not documented | not documented | $6 | -- | [src](https://docs.x.ai/developers/models) |
| xAI | `grok-4.5 (short context)` | $2 | $0.3 | not documented | $6 | -- | [src](https://docs.x.ai/developers/pricing) |
| xAI | `grok-4.20-0309-non-reasoning (long context)` | $2.5 | $0.4 | not documented | $5 | -- | [src](https://docs.x.ai/developers/pricing) |
| xAI | `grok-4.20-0309-reasoning (long context)` | $2.5 | $0.4 | not documented | $5 | -- | [src](https://docs.x.ai/developers/pricing) |
| xAI | `grok-4.20-multi-agent-0309 (long context)` | $2.5 | $0.4 | not documented | $5 | -- | [src](https://docs.x.ai/developers/pricing) |
| xAI | `grok-4.3 (long context)` | $2.5 | $0.4 | not documented | $5 | -- | [src](https://docs.x.ai/developers/pricing) |
| xAI | `grok-build-0.1 (long context)` | $2 | $0.4 | not documented | $4 | -- | [src](https://docs.x.ai/developers/pricing) |
| xAI | `grok-4.20-0309-non-reasoning (short context)` | $1.25 | $0.2 | not documented | $2.5 | -- | [src](https://docs.x.ai/developers/pricing) |
| xAI | `grok-4.20-0309-reasoning (short context)` | $1.25 | $0.2 | not documented | $2.5 | -- | [src](https://docs.x.ai/developers/pricing) |
| xAI | `grok-4.20-multi-agent-0309 (short context)` | $1.25 | $0.2 | not documented | $2.5 | -- | [src](https://docs.x.ai/developers/pricing) |
| xAI | `grok-4.3 (short context)` | $1.25 | $0.2 | not documented | $2.5 | -- | [src](https://docs.x.ai/developers/pricing) |
| xAI | `grok-build-0.1 (short context)` | $1 | $0.2 | not documented | $2 | -- | [src](https://docs.x.ai/developers/pricing) |

## API pricing, open models on hosted APIs

The same open weights cost different amounts depending on who runs them. Spread
across providers for one model reaches 10x.

| Model family | Provider | Model id | Input /1M | Cached in | Output /1M | Quant | Source |
|---|---|---|---|---|---|---|---|
| DeepSeek-V3.2 | DeepInfra | `deepseek-ai/DeepSeek-V3.2` | $0.26 | $0.13 | $0.38 | not stated | [src](https://deepinfra.com/pricing) |
| DeepSeek-V3.2 | Novita AI | `deepseek/deepseek-v3.2` | $0.269 | $0.1345 | $0.4 | fp8 | [src](https://novita.ai/pricing) |
| DeepSeek-V3.2 | Novita AI | `deepseek/deepseek-v3.2-exp` | $0.27 | not offered | $0.41 | fp8 | [src](https://novita.ai/pricing) |
| DeepSeek-R1-0528 | Novita AI | `deepseek/deepseek-r1-0528-qwen3-8b` | $0.06 | not offered | $0.09 | bf16 | [src](https://novita.ai/pricing) |
| DeepSeek-R1-0528 | DeepInfra | `deepseek-ai/DeepSeek-R1-0528` | $0.5 | $0.35 | $2.15 | not stated | [src](https://deepinfra.com/pricing) |
| DeepSeek-R1-0528 | Novita AI | `deepseek/deepseek-r1-0528` | $0.7 | $0.35 | $2.5 | fp8 | [src](https://novita.ai/pricing) |
| Qwen3-235B-A22B-Instruct-2507 | DeepInfra | `Qwen/Qwen3-235B-A22B-Instruct-2507` | $0.09 | not offered | $0.55 | not stated | [src](https://deepinfra.com/pricing) |
| Qwen3-235B-A22B-Instruct-2507 | Novita AI | `qwen/qwen3-235b-a22b-instruct-2507` | $0.09 | not offered | $0.58 | fp8 | [src](https://novita.ai/pricing) |
| Qwen3-235B-A22B-Instruct-2507 | Together AI | `Qwen/Qwen3-235B-A22B-Instruct-2507-tput` | $0.2 | not offered | $0.6 | FP8 | [src](https://www.together.ai/models/qwen3-235b-a22b-instruct-2507-fp8) |
| Qwen3-235B-A22B-Instruct-2507 | Nebius AI Studio | `Qwen/Qwen3-235B-A22B-Instruct-2507` | $0.2 | not offered | $0.6 | fp8 | [src](https://tokenfactory.nebius.com/api/public/models_info) |
| Kimi-K2-Instruct | Novita AI | `moonshotai/kimi-k2-instruct` | $0.57 | not offered | $2.3 | fp8 | [src](https://novita.ai/pricing) |
| Kimi-K2-Instruct | Groq | `moonshotai/kimi-k2-instruct-0905` | $1 | $0.5 | $3 | not stated | [src](https://groq.com/pricing) |
| gpt-oss-120b | Novita AI | `openai/gpt-oss-120b` | $0.05 | not offered | $0.25 | fp4 | [src](https://novita.ai/pricing) |
| gpt-oss-120b | Baseten | `openai/gpt-oss-120b` | $0.1 | not offered | $0.5 | not stated | [src](https://www.baseten.co/pricing/) |
| gpt-oss-120b | Together AI | `openai/gpt-oss-120b` | $0.15 | not offered | $0.6 | not stated | [src](https://www.together.ai/models/gpt-oss-120b) |
| gpt-oss-120b | Groq | `openai/gpt-oss-120b` | $0.15 | $0.075 | $0.6 | not stated | [src](https://groq.com/pricing) |
| gpt-oss-120b | Nebius AI Studio | `openai/gpt-oss-120b` | $0.15 | not offered | $0.6 | fp4 | [src](https://tokenfactory.nebius.com/api/public/models_info) |
| gpt-oss-120b | Cerebras | `openai/gpt-oss-120b` | $0.35 | not offered | $0.75 | fp16 | [src](https://inference-docs.cerebras.ai/api-reference/models/public-models) |
| Llama-3.3-70B-Instruct | DeepInfra | `meta-llama/Llama-3.3-70B-Instruct-Turbo` | $0.1 | not offered | $0.32 | not stated | [src](https://deepinfra.com/pricing) |
| Llama-3.3-70B-Instruct | Novita AI | `meta-llama/llama-3.3-70b-instruct` | $0.135 | not offered | $0.4 | bf16 | [src](https://novita.ai/pricing) |
| Llama-3.3-70B-Instruct | Nebius AI Studio | `meta-llama/Llama-3.3-70B-Instruct` | $0.13 | not offered | $0.4 | fp8 | [src](https://tokenfactory.nebius.com/api/public/models_info) |
| Llama-3.3-70B-Instruct | Together AI | `meta-llama/Llama-3.3-70B-Instruct-Turbo` | $1.04 | not offered | $1.04 | FP8 | [src](https://www.together.ai/models/llama-3-3-70b) |
| MiniMax-M3 | Together AI | `MiniMaxAI/MiniMax-M3` | $0.3 | $0.06 | $1.2 | not stated | [src](https://www.together.ai/models/minimax-m3) |
| MiniMax-M3 | Novita AI | `minimax/minimax-m3` | $0.3 | $0.06 | $1.2 | fp8 | [src](https://novita.ai/pricing) |
| MiniMax-M3 | Nebius AI Studio | `MiniMaxAI/MiniMax-M3` | $0.3 | not offered | $1.2 | fp4 | [src](https://tokenfactory.nebius.com/api/public/models_info) |
| GLM-4.7 | Novita AI | `zai-org/glm-4.7-flash` | $0.07 | $0.01 | $0.4 | bf16 | [src](https://novita.ai/pricing) |
| GLM-4.7 | Novita AI | `zai-org/glm-4.7` | $0.6 | $0.11 | $2.2 | fp8 | [src](https://novita.ai/pricing) |
| Kimi-K3 | Together AI | `moonshotai/Kimi-K3` | $3 | $0.3 | $15 | FP4 | [src](https://www.together.ai/models/kimi-k3) |
| Kimi-K3 | Baseten | `moonshotai/Kimi-K3` | $3 | $0.3 | $15 | not stated | [src](https://www.baseten.co/pricing/) |
| Kimi-K3 | Novita AI | `moonshotai/kimi-k3` | $3 | $0.3 | $15 | not stated | [src](https://novita.ai/pricing) |
| Kimi-K3 | Nebius AI Studio | `moonshotai/Kimi-K3` | $3 | not offered | $15 | fp4 | [src](https://tokenfactory.nebius.com/api/public/models_info) |
| GLM-5.2 | Together AI | `zai-org/GLM-5.2` | $1.4 | $0.26 | $4.4 | FP4 | [src](https://www.together.ai/models/glm-52) |
| GLM-5.2 | Novita AI | `zai-org/glm-5.2` | $1.4 | $0.26 | $4.4 | fp8 | [src](https://novita.ai/pricing) |
| GLM-5.2 | Nebius AI Studio | `zai-org/GLM-5.2` | $1.4 | not offered | $4.4 | fp4 | [src](https://tokenfactory.nebius.com/api/public/models_info) |
| GLM-5.2 | Baseten | `zai-org/GLM-5.2-Fast` | $2.1 | $0.21 | $6.6 | not stated | [src](https://www.baseten.co/pricing/) |

## Prompt caching

The discount is large and the terms are not standard. Minimum cacheable prefix
and TTL are the two fields most comparisons omit, and both decide whether you
get the discount at all.

| Provider | Cache read | Cache write | TTL | Min prefix | Mode | Doc |
|---|---|---|---|---|---|---|
| OpenAI | Model-specific cached-input rate; the guid | GPT-5.6 and later model families:  | GPT-5.6 and later: minimum 30m and may | 1024 | explicit_breakpoints | [doc](https://developers.openai.com/api/docs/guides/prompt-caching) |
| Anthropic | 0.1Ã— the base input-token price. | 5-minute writes: 1.25Ã— base input | 5 minutes by default and refreshed on  | 512 for Claude Opus 5, Claude  | explicit_breakpoints | [doc](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) |
| Google Gemini | Model-specific cached-token pricing; the c | Explicit caching adds model-specif | Explicit cache objects default to 1 ho | Gemini 3.5 Flash and Gemini 3. | automatic | [doc](https://ai.google.dev/gemini-api/docs/generate-content/caching) |
| xAI | Model-specific reduced cached-prompt-token | not documented | not documented | not documented | automatic | [doc](https://docs.x.ai/developers/advanced-api-usage/prompt-caching) |
| DeepSeek | Model-specific cache-hit prices are listed | not documented | Usually cleared within a few hours to  | not documented | automatic | [doc](https://api-docs.deepseek.com/guides/kv_cache) |
| Mistral | 10% of the standard input-token price. | not documented | not documented | 64 | automatic | [doc](https://docs.mistral.ai/studio-api/conversations/advanced/prompt-caching) |
| Together AI | Model-specific cached-input price; only ch | not documented | Best-effort and short-lived; no config | not documented | automatic | [doc](https://docs.together.ai/docs/serverless/overview) |
| Fireworks AI | Default discount is 50%, but the exact dis | not documented | Usually at least several minutes and,  | not documented | automatic | [doc](https://docs.fireworks.ai/guides/prompt-caching) |
| DeepInfra | Model-specific cached-input prices are pre | not documented | not documented | not documented | not documented | [doc](https://deepinfra.com/models/featured) |
| Groq | 50% discount for cached input tokens. | None; the page says prompt caching | 2 hours without use. | 128 to 1024 tokens depending o | automatic | [doc](https://console.groq.com/docs/prompt-caching) |

## Batch and async tiers

Separate products with different latency contracts. Never blend these into a
realtime price.

| Provider | Offered | Discount | Turnaround | Restrictions | Doc |
|---|---|---|---|---|---|
| OpenAI | True | 50 | Each batch completes within 24 hou | ['Up to 50,000 requests per batch.', 'Input file up to 200 M | [doc](https://developers.openai.com/api/docs/guides/batch) |
| Anthropic | True | 50 | Most batches finish in less than 1 | ['Maximum 100,000 Message requests or 256 MB per batch, whic | [doc](https://docs.claude.com/en/docs/build-with-claude/batch-processing) |
| Google Gemini | True | 50 | Target turnaround time is 24 hours | ['GenerateContent Batch is the documented primary API; batch | [doc](https://ai.google.dev/gemini-api/docs/batch-api) |
| xAI | True | 20 | Most batches complete within 24 ho | ['The 20% discount applies to grok-4.3, grok-4.20-0309-reaso | [doc](https://docs.x.ai/developers/advanced-api-usage/batch-api) |
| DeepSeek | not documented | not documented | not documented | ['No Batch API or asynchronous batch-processing page was fou | [doc](https://api-docs.deepseek.com/) |
| Mistral | True | 50 | timeout_hours defaults to 24 hours | ['Maximum 1 million pending requests per workspace.', 'No do | [doc](https://docs.mistral.ai/studio-api/batch-processing) |
| Together AI | True | Up to 50; only the current | 24-hour completion window is a bes | ['Up to 50,000 requests per batch.', 'Up to 100 MB per input | [doc](https://docs.together.ai/docs/inference/batch/overview) |
| Fireworks AI | True | 50 | The settings section offers 12, 24 | ['Input dataset maximum 1GB; output dataset maximum 8GB.', ' | [doc](https://docs.fireworks.ai/guides/batch-inference) |
| DeepInfra | True | 20 | Results are returned within 24 hou | ['Supported endpoints: /v1/chat/completions, /v1/completions | [doc](https://docs.deepinfra.com/batch/introduction) |
| Groq | True | 50 | Selectable processing window from  | ['Batch chat models listed are openai/gpt-oss-20b, openai/gp | [doc](https://console.groq.com/docs/batch) |

## Reasoning tokens

On reasoning models the tokens you are billed for are not the tokens you see.
Reasoning tokens bill at the output rate and are invisible or summarized.

| Provider | Billed as output | Visible | Usage field | Effort levels | Doc |
|---|---|---|---|---|---|
| OpenAI | True | summarized | `['usage.output_tokens_details.reasoning_tokens', 'us` | Model-dependent values can include none, minimal, low, m | [doc](https://developers.openai.com/api/docs/guides/reasoning) |
| Anthropic | True | summarized | `usage.output_tokens_details.thinking_tokens` | low, medium, high, xhigh, and max, with availability var | [doc](https://docs.claude.com/en/docs/build-with-claude/thinking-steering-and-cost) |
| Google Gemini | True | summarized | `interaction.usage.total_thought_tokens` | thinking_level is model-dependent and supports combinati | [doc](https://ai.google.dev/gemini-api/docs/thinking) |
| xAI | True | summarized | `['usage.completion_tokens_details.reasoning_tokens',` | The current reasoning guide documents low, medium, and h | [doc](https://docs.x.ai/developers/model-capabilities/text/reasoning) |
| DeepSeek | True | full | `usage.completion_tokens_details.reasoning_tokens` | Thinking is enabled by default at high effort. The guide | [doc](https://api-docs.deepseek.com/guides/thinking_mode/) |

**Worked example.** Take a request to `gpt-5.6-sol` at $30 per 1M output that
returns 300 visible tokens after 4,000 reasoning tokens. Billed output is 4,300
tokens, not 300. Cost is 4,300 / 1,000,000 x $30 = **$0.129**, against
**$0.009** for the visible text alone. That is 14.3x. The token counts here are
an illustrative scenario, not a measurement; the $30 rate is verified. Read
`usage.completion_tokens_details.reasoning_tokens` on your own traffic rather
than trusting this ratio.

## Tokenizer normalization

All per-1M prices in this repo are per that model's own tokens. Two tokenizers
given identical text return different counts, so comparing two per-token prices
without normalizing compares numbers in different units.

Measured by `scripts/measure_tokenizers.py` against two fixed files in
`data/tokenizer-corpus/`: a 739-character English paragraph and a
1,376-character Python file.

| Tokenizer | Source | English tokens | English /1k chars | Code tokens | Code /1k chars |
|---|---|---|---|---|---|
| `o200k_base` | tiktoken | 133 | 179.97 | 365 | 265.26 |
| `cl100k_base` | tiktoken | 134 | 181.33 | 360 | 261.63 |
| `Qwen/Qwen3-235B-A22B` | huggingface | 134 | 181.33 | 373 | 271.08 |
| `Qwen/Qwen2.5-72B-Instruct` | huggingface | 134 | 181.33 | 373 | 271.08 |
| `deepseek-ai/DeepSeek-V3` | huggingface | 137 | 185.39 | 391 | 284.16 |
| `deepseek-ai/DeepSeek-R1` | huggingface | 137 | 185.39 | 391 | 284.16 |
| `openai/gpt-oss-120b` | huggingface | 133 | 179.97 | 365 | 265.26 |
| `meta-llama/Llama-3.3-70B-Instruct` | huggingface | not measured | not measured | not measured | You are trying to access a gated repo. |
| `moonshotai/Kimi-K2-Instruct` | huggingface | not measured | not measured | not measured | The repository moonshotai/Kimi-K2-Instruct contains custom |
| `zai-org/GLM-4.5` | huggingface | 134 | 181.33 | 360 | 261.63 |
| `google/gemma-3-27b-it` | huggingface | not measured | not measured | not measured | You are trying to access a gated repo. |
| `mistralai/Mistral-Small-3.1-24B-Instruct-2503` | mistral-common | 134 | 181.33 | 395 | 287.06 |
| `mistralai/Magistral-Small-2509` | mistral-common | 134 | 181.33 | 395 | 287.06 |
| `Anthropic (Claude family)` | none_published | not measured | not measured | not measured | no downloadable tokenizer published; token counts are only |
| `Google (Gemini family)` | none_published | not measured | not measured | not measured | no downloadable tokenizer published; token counts are only |

**Correction factor.** Against `o200k_base` as the baseline, English spans
179.97 to 185.39 tokens per 1,000 characters, a spread of **3.0%**. Code spans
261.63 to 287.06, a spread of **9.7%**. So tokenizer differences are close to
noise for English prose and worth correcting for code. To compare a price on
model X against a price on model Y for the same text, multiply X's price by
(X tokens per 1k chars / Y tokens per 1k chars).

Anthropic and Google publish no downloadable tokenizer. Their counts are only
obtainable from an authenticated endpoint, so their rows are blank rather than
guessed.

## Self-hosting

The formula, applied identically to every row:

```
cost_per_1M_tokens = (gpu_hourly_rate * gpu_count)
                     / (throughput_tok_per_s * 3600 * utilization)
                     * 1_000_000
```

Throughput here is cited, not measured by us, and every figure is total output
tokens per second across the whole deployment. Where a source published
per-GPU throughput it has been multiplied by GPU count, which is recorded per
row in `data/self-host-inputs.json`. Getting that wrong understates cost by the
GPU count, so check it before reusing any throughput number.

| Model | GPUs | Rental | $/GPU/hr | Tok/s total | Throughput | 10% util | 30% util | 60% util | 90% util |
|---|---|---|---|---|---|---|---|---|---|
| DeepSeek-R1-0528 | 4x B200 | RunPod | $5.89 | 1,488 | cited | $43.99 | $14.66 | $7.33 | $4.89 |
| DeepSeek-R1-0528 | 4x B200 | CoreWeave | $8.6 | 1,488 | cited | $64.23 | $21.41 | $10.71 | $7.14 |
| DeepSeek-R1-0528 | 4x MI355X | Vultr | $2.59 | 1,624 | cited | $17.73 | $5.91 | $2.95 | $1.97 |
| DeepSeek-R1-0528 | 4x MI355X | Oracle Cloud | $8.6 | 1,624 | cited | $58.86 | $19.62 | $9.81 | $6.54 |
| MiniMax-M3 | 4x B300 | RunPod | $6.94 | 6,280 | cited | $12.28 | $4.09 | $2.05 | $1.36 |
| MiniMax-M3 | 4x B300 | Nebius | $7.85 | 6,280 | cited | $13.89 | $4.63 | $2.31 | $1.54 |
| MiniMax-M3 | 4x MI355X | Vultr | $2.59 | 3,817 | cited | $7.54 | $2.51 | $1.26 | $0.84 |
| MiniMax-M3 | 4x MI355X | Oracle Cloud | $8.6 | 3,817 | cited | $25.03 | $8.34 | $4.17 | $2.78 |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | Vultr | $2.59 | 165 | cited | $348.19 | $116.06 | $58.03 | $38.69 |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | Oracle Cloud | $8.6 | 165 | cited | $1156.15 | $385.38 | $192.69 | $128.46 |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | Vultr | $2.59 | 1,056 | cited | $54.51 | $18.17 | $9.08 | $6.06 |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | Oracle Cloud | $8.6 | 1,056 | cited | $180.99 | $60.33 | $30.16 | $20.11 |
| Llama-3.3-70B-Instruct-FP8 (In | 2x H200 | RunPod | $3.59 | 1,121 | cited | $17.79 | $5.93 | $2.96 | $1.98 |
| Llama-3.3-70B-Instruct-FP8 (In | 2x H200 | CoreWeave | $6.31 | 1,121 | cited | $31.26 | $10.42 | $5.21 | $3.47 |
| Llama-3.3-70B-Instruct-FP8 (In | 1x MI355X | Vultr | $2.59 | 971 | cited | $7.41 | $2.47 | $1.24 | $0.82 |
| Llama-3.3-70B-Instruct-FP8 (In | 1x MI355X | Oracle Cloud | $8.6 | 971 | cited | $24.61 | $8.20 | $4.10 | $2.73 |
| gptoss120b | 2x H100 | RunPod | $1.99 | 658 | cited | $16.80 | $5.60 | $2.80 | $1.87 |
| gptoss120b | 2x H100 | CoreWeave | $6.16 | 658 | cited | $52.01 | $17.34 | $8.67 | $5.78 |
| gptoss120b | 2x H100 | RunPod | $1.99 | 998 | cited | $11.07 | $3.69 | $1.85 | $1.23 |
| gptoss120b | 2x H100 | CoreWeave | $6.16 | 998 | cited | $34.28 | $11.43 | $5.71 | $3.81 |
| gptoss120b | 2x H100 | RunPod | $1.99 | 1,385 | cited | $7.98 | $2.66 | $1.33 | $0.89 |
| gptoss120b | 2x H100 | CoreWeave | $6.16 | 1,385 | cited | $24.70 | $8.23 | $4.12 | $2.74 |
| gptoss120b | 2x H100 | RunPod | $1.99 | 1,825 | cited | $6.06 | $2.02 | $1.01 | $0.67 |
| gptoss120b | 2x H100 | CoreWeave | $6.16 | 1,825 | cited | $18.75 | $6.25 | $3.13 | $2.08 |
| gptoss120b | 2x H100 | RunPod | $1.99 | 2,282 | cited | $4.84 | $1.61 | $0.81 | $0.54 |
| gptoss120b | 2x H100 | CoreWeave | $6.16 | 2,282 | cited | $15.00 | $5.00 | $2.50 | $1.67 |
| gptoss120b | 2x H200 | RunPod | $3.59 | 694 | cited | $28.75 | $9.58 | $4.79 | $3.19 |
| gptoss120b | 2x H200 | CoreWeave | $6.31 | 694 | cited | $50.53 | $16.84 | $8.42 | $5.61 |
| gptoss120b | 2x H200 | RunPod | $3.59 | 431 | cited | $46.24 | $15.41 | $7.71 | $5.14 |
| gptoss120b | 2x H200 | CoreWeave | $6.31 | 431 | cited | $81.27 | $27.09 | $13.55 | $9.03 |
| gptoss120b | 2x H200 | RunPod | $3.59 | 1,453 | cited | $13.72 | $4.58 | $2.29 | $1.52 |
| gptoss120b | 2x H200 | CoreWeave | $6.31 | 1,453 | cited | $24.12 | $8.04 | $4.02 | $2.68 |
| gptoss120b | 2x H200 | RunPod | $3.59 | 1,238 | cited | $16.11 | $5.37 | $2.69 | $1.79 |
| gptoss120b | 2x H200 | CoreWeave | $6.31 | 1,238 | cited | $28.32 | $9.44 | $4.72 | $3.15 |
| gptoss120b | 2x H200 | RunPod | $3.59 | 2,421 | cited | $8.24 | $2.75 | $1.37 | $0.92 |
| gptoss120b | 2x H200 | CoreWeave | $6.31 | 2,421 | cited | $14.48 | $4.83 | $2.41 | $1.61 |
| qwen3.5 | 8x H100 | RunPod | $1.99 | 160 | cited | $276.77 | $92.26 | $46.13 | $30.75 |
| qwen3.5 | 8x H100 | CoreWeave | $6.16 | 160 | cited | $856.73 | $285.58 | $142.79 | $95.19 |
| qwen3.5 | 8x H100 | RunPod | $1.99 | 279 | cited | $158.26 | $52.75 | $26.38 | $17.58 |
| qwen3.5 | 8x H100 | CoreWeave | $6.16 | 279 | cited | $489.89 | $163.30 | $81.65 | $54.43 |
| qwen3.5 | 8x H100 | RunPod | $1.99 | 457 | cited | $96.69 | $32.23 | $16.11 | $10.74 |
| qwen3.5 | 8x H100 | CoreWeave | $6.16 | 457 | cited | $299.30 | $99.77 | $49.88 | $33.26 |
| qwen3.5 | 8x H100 | RunPod | $1.99 | 472 | cited | $93.72 | $31.24 | $15.62 | $10.41 |
| qwen3.5 | 8x H100 | CoreWeave | $6.16 | 472 | cited | $290.12 | $96.71 | $48.35 | $32.24 |
| llama_13b | 1x H200 | RunPod | $3.59 | 11,819 | cited | $0.84 | $0.28 | $0.14 | $0.09 |
| llama_13b | 1x H200 | CoreWeave | $6.31 | 11,819 | cited | $1.48 | $0.49 | $0.25 | $0.16 |
| llama_13b | 1x H200 | RunPod | $3.59 | 4,750 | cited | $2.10 | $0.70 | $0.35 | $0.23 |
| llama_13b | 1x H200 | CoreWeave | $6.31 | 4,750 | cited | $3.69 | $1.23 | $0.61 | $0.41 |
| llama_13b | 1x H200 | RunPod | $3.59 | 1,349 | cited | $7.39 | $2.46 | $1.23 | $0.82 |
| llama_13b | 1x H200 | CoreWeave | $6.31 | 1,349 | cited | $12.99 | $4.33 | $2.17 | $1.44 |
| Llama-70B | 1x H200 | RunPod | $3.59 | 3,803 | cited | $2.62 | $0.87 | $0.44 | $0.29 |
| Llama-70B | 1x H200 | CoreWeave | $6.31 | 3,803 | cited | $4.61 | $1.54 | $0.77 | $0.51 |
| Llama-70B | 8x H200 | RunPod | $3.59 | 3,803 | cited | $20.98 | $6.99 | $3.50 | $2.33 |
| Llama-70B | 8x H200 | CoreWeave | $6.31 | 3,803 | cited | $36.87 | $12.29 | $6.15 | $4.10 |
| Llama-70B | 1x H200 | RunPod | $3.59 | 2,941 | cited | $3.39 | $1.13 | $0.57 | $0.38 |
| Llama-70B | 1x H200 | CoreWeave | $6.31 | 2,941 | cited | $5.96 | $1.99 | $0.99 | $0.66 |
| Llama-70B | 8x H200 | RunPod | $3.59 | 3,163 | cited | $25.22 | $8.41 | $4.20 | $2.80 |
| Llama-70B | 8x H200 | CoreWeave | $6.31 | 3,163 | cited | $44.33 | $14.78 | $7.39 | $4.93 |
| Llama-70B | 1x H200 | RunPod | $3.59 | 1,946 | cited | $5.12 | $1.71 | $0.85 | $0.57 |
| Llama-70B | 1x H200 | CoreWeave | $6.31 | 1,946 | cited | $9.01 | $3.00 | $1.50 | $1.00 |
| Llama-70B | 8x H200 | RunPod | $3.59 | 2,263 | cited | $35.25 | $11.75 | $5.88 | $3.92 |
| Llama-70B | 8x H200 | CoreWeave | $6.31 | 2,263 | cited | $61.96 | $20.65 | $10.33 | $6.88 |

Utilization is the assumption that moves these numbers most, by 9x across the
range shown. It is also the one nobody measures honestly before committing.

Configurations dropped for lack of a published rate: every AMD MI355X result in
`data/self-host-inputs.json`. The throughput data exists and is good, but no
surveyed provider publishes an on-demand per-GPU MI355X price, so those rows
have no cost and are left empty rather than costed against a guess.

## Break-even

Self-hosting is a fixed monthly bill. An API is purely variable. Break-even is
where the fixed bill divided by monthly volume equals the API's unit price.
"Capacity" is the most tokens the box can physically emit at that utilization.

| Self-host model | GPUs | Fixed $/mo | Compared to API | API out /1M | Break-even tokens/mo | Capacity @30% | Beats API @30%? | Beats API @90%? |
|---|---|---|---|---|---|---|---|---|
| DeepSeek-R1-0528 | 4x B200 | $16,963 | OpenAI `gpt-5.6-terra` | $12 | 1,414M | 1,157M | no | yes |
| DeepSeek-R1-0528 | 4x B200 | $16,963 | Anthropic `Claude Sonnet 5` | $10 | 1,696M | 1,157M | no | yes |
| DeepSeek-R1-0528 | 4x B200 | $16,963 | Anthropic `Claude Sonnet 5` | $10 | 1,696M | 1,157M | no | yes |
| DeepSeek-R1-0528 | 4x B200 | $16,963 | Anthropic `Claude Sonnet 5` | $15 | 1,131M | 1,157M | yes | yes |
| DeepSeek-R1-0528 | 4x B200 | $16,963 | Anthropic `Claude Sonnet 5` | $15 | 1,131M | 1,157M | yes | yes |
| DeepSeek-R1-0528 | 4x B200 | $16,963 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 2,262M | 1,157M | no | yes |
| DeepSeek-R1-0528 | 4x B200 | $16,963 | DeepSeek `deepseek-v4-flash` | $0.28 | 60,583M | 1,157M | no | no |
| DeepSeek-R1-0528 | 4x B200 | $16,963 | DeepSeek `deepseek-v4-flash` | $0.28 | 60,583M | 1,157M | no | no |
| DeepSeek-R1-0528 | 4x B200 | $24,768 | OpenAI `gpt-5.6-terra` | $12 | 2,064M | 1,157M | no | yes |
| DeepSeek-R1-0528 | 4x B200 | $24,768 | Anthropic `Claude Sonnet 5` | $10 | 2,477M | 1,157M | no | yes |
| DeepSeek-R1-0528 | 4x B200 | $24,768 | Anthropic `Claude Sonnet 5` | $10 | 2,477M | 1,157M | no | yes |
| DeepSeek-R1-0528 | 4x B200 | $24,768 | Anthropic `Claude Sonnet 5` | $15 | 1,651M | 1,157M | no | yes |
| DeepSeek-R1-0528 | 4x B200 | $24,768 | Anthropic `Claude Sonnet 5` | $15 | 1,651M | 1,157M | no | yes |
| DeepSeek-R1-0528 | 4x B200 | $24,768 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 3,302M | 1,157M | no | yes |
| DeepSeek-R1-0528 | 4x B200 | $24,768 | DeepSeek `deepseek-v4-flash` | $0.28 | 88,457M | 1,157M | no | no |
| DeepSeek-R1-0528 | 4x B200 | $24,768 | DeepSeek `deepseek-v4-flash` | $0.28 | 88,457M | 1,157M | no | no |
| DeepSeek-R1-0528 | 4x MI355X | $7,459 | OpenAI `gpt-5.6-terra` | $12 | 622M | 1,262M | yes | yes |
| DeepSeek-R1-0528 | 4x MI355X | $7,459 | Anthropic `Claude Sonnet 5` | $10 | 746M | 1,262M | yes | yes |
| DeepSeek-R1-0528 | 4x MI355X | $7,459 | Anthropic `Claude Sonnet 5` | $10 | 746M | 1,262M | yes | yes |
| DeepSeek-R1-0528 | 4x MI355X | $7,459 | Anthropic `Claude Sonnet 5` | $15 | 497M | 1,262M | yes | yes |
| DeepSeek-R1-0528 | 4x MI355X | $7,459 | Anthropic `Claude Sonnet 5` | $15 | 497M | 1,262M | yes | yes |
| DeepSeek-R1-0528 | 4x MI355X | $7,459 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 995M | 1,262M | yes | yes |
| DeepSeek-R1-0528 | 4x MI355X | $7,459 | DeepSeek `deepseek-v4-flash` | $0.28 | 26,640M | 1,262M | no | no |
| DeepSeek-R1-0528 | 4x MI355X | $7,459 | DeepSeek `deepseek-v4-flash` | $0.28 | 26,640M | 1,262M | no | no |
| DeepSeek-R1-0528 | 4x MI355X | $24,768 | OpenAI `gpt-5.6-terra` | $12 | 2,064M | 1,262M | no | yes |
| DeepSeek-R1-0528 | 4x MI355X | $24,768 | Anthropic `Claude Sonnet 5` | $10 | 2,477M | 1,262M | no | yes |
| DeepSeek-R1-0528 | 4x MI355X | $24,768 | Anthropic `Claude Sonnet 5` | $10 | 2,477M | 1,262M | no | yes |
| DeepSeek-R1-0528 | 4x MI355X | $24,768 | Anthropic `Claude Sonnet 5` | $15 | 1,651M | 1,262M | no | yes |
| DeepSeek-R1-0528 | 4x MI355X | $24,768 | Anthropic `Claude Sonnet 5` | $15 | 1,651M | 1,262M | no | yes |
| DeepSeek-R1-0528 | 4x MI355X | $24,768 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 3,302M | 1,262M | no | yes |
| DeepSeek-R1-0528 | 4x MI355X | $24,768 | DeepSeek `deepseek-v4-flash` | $0.28 | 88,457M | 1,262M | no | no |
| DeepSeek-R1-0528 | 4x MI355X | $24,768 | DeepSeek `deepseek-v4-flash` | $0.28 | 88,457M | 1,262M | no | no |
| MiniMax-M3 | 4x B300 | $19,987 | OpenAI `gpt-5.6-terra` | $12 | 1,666M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $19,987 | Anthropic `Claude Sonnet 5` | $10 | 1,999M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $19,987 | Anthropic `Claude Sonnet 5` | $10 | 1,999M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $19,987 | Anthropic `Claude Sonnet 5` | $15 | 1,332M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $19,987 | Anthropic `Claude Sonnet 5` | $15 | 1,332M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $19,987 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 2,665M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $19,987 | DeepSeek `deepseek-v4-flash` | $0.28 | 71,383M | 4,883M | no | no |
| MiniMax-M3 | 4x B300 | $19,987 | DeepSeek `deepseek-v4-flash` | $0.28 | 71,383M | 4,883M | no | no |
| MiniMax-M3 | 4x B300 | $22,608 | OpenAI `gpt-5.6-terra` | $12 | 1,884M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $22,608 | Anthropic `Claude Sonnet 5` | $10 | 2,261M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $22,608 | Anthropic `Claude Sonnet 5` | $10 | 2,261M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $22,608 | Anthropic `Claude Sonnet 5` | $15 | 1,507M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $22,608 | Anthropic `Claude Sonnet 5` | $15 | 1,507M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $22,608 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 3,014M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $22,608 | DeepSeek `deepseek-v4-flash` | $0.28 | 80,743M | 4,883M | no | no |
| MiniMax-M3 | 4x B300 | $22,608 | DeepSeek `deepseek-v4-flash` | $0.28 | 80,743M | 4,883M | no | no |
| MiniMax-M3 | 4x MI355X | $7,459 | OpenAI `gpt-5.6-terra` | $12 | 622M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $7,459 | Anthropic `Claude Sonnet 5` | $10 | 746M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $7,459 | Anthropic `Claude Sonnet 5` | $10 | 746M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $7,459 | Anthropic `Claude Sonnet 5` | $15 | 497M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $7,459 | Anthropic `Claude Sonnet 5` | $15 | 497M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $7,459 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 995M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $7,459 | DeepSeek `deepseek-v4-flash` | $0.28 | 26,640M | 2,968M | no | no |
| MiniMax-M3 | 4x MI355X | $7,459 | DeepSeek `deepseek-v4-flash` | $0.28 | 26,640M | 2,968M | no | no |
| MiniMax-M3 | 4x MI355X | $24,768 | OpenAI `gpt-5.6-terra` | $12 | 2,064M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $24,768 | Anthropic `Claude Sonnet 5` | $10 | 2,477M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $24,768 | Anthropic `Claude Sonnet 5` | $10 | 2,477M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $24,768 | Anthropic `Claude Sonnet 5` | $15 | 1,651M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $24,768 | Anthropic `Claude Sonnet 5` | $15 | 1,651M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $24,768 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 3,302M | 2,968M | no | yes |
| MiniMax-M3 | 4x MI355X | $24,768 | DeepSeek `deepseek-v4-flash` | $0.28 | 88,457M | 2,968M | no | no |
| MiniMax-M3 | 4x MI355X | $24,768 | DeepSeek `deepseek-v4-flash` | $0.28 | 88,457M | 2,968M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | OpenAI `gpt-5.6-terra` | $12 | 1,243M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Anthropic `Claude Sonnet 5` | $10 | 1,492M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Anthropic `Claude Sonnet 5` | $10 | 1,492M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Anthropic `Claude Sonnet 5` | $15 | 995M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Anthropic `Claude Sonnet 5` | $15 | 995M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,989M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | DeepSeek `deepseek-v4-flash` | $0.28 | 53,280M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | DeepSeek `deepseek-v4-flash` | $0.28 | 53,280M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | OpenAI `gpt-5.6-terra` | $12 | 4,128M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Anthropic `Claude Sonnet 5` | $10 | 4,954M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Anthropic `Claude Sonnet 5` | $10 | 4,954M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Anthropic `Claude Sonnet 5` | $15 | 3,302M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Anthropic `Claude Sonnet 5` | $15 | 3,302M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 6,605M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | DeepSeek `deepseek-v4-flash` | $0.28 | 176,914M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | DeepSeek `deepseek-v4-flash` | $0.28 | 176,914M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | OpenAI `gpt-5.6-terra` | $12 | 1,243M | 821M | no | yes |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Anthropic `Claude Sonnet 5` | $10 | 1,492M | 821M | no | yes |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Anthropic `Claude Sonnet 5` | $10 | 1,492M | 821M | no | yes |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Anthropic `Claude Sonnet 5` | $15 | 995M | 821M | no | yes |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Anthropic `Claude Sonnet 5` | $15 | 995M | 821M | no | yes |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,989M | 821M | no | yes |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | DeepSeek `deepseek-v4-flash` | $0.28 | 53,280M | 821M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | DeepSeek `deepseek-v4-flash` | $0.28 | 53,280M | 821M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | OpenAI `gpt-5.6-terra` | $12 | 4,128M | 821M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Anthropic `Claude Sonnet 5` | $10 | 4,954M | 821M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Anthropic `Claude Sonnet 5` | $10 | 4,954M | 821M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Anthropic `Claude Sonnet 5` | $15 | 3,302M | 821M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Anthropic `Claude Sonnet 5` | $15 | 3,302M | 821M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 6,605M | 821M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | DeepSeek `deepseek-v4-flash` | $0.28 | 176,914M | 821M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | DeepSeek `deepseek-v4-flash` | $0.28 | 176,914M | 821M | no | no |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $5,170 | OpenAI `gpt-5.6-terra` | $12 | 431M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $10 | 517M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $10 | 517M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $15 | 345M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $15 | 345M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $5,170 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 689M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $5,170 | DeepSeek `deepseek-v4-flash` | $0.28 | 18,463M | 872M | no | no |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $5,170 | DeepSeek `deepseek-v4-flash` | $0.28 | 18,463M | 872M | no | no |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $9,086 | OpenAI `gpt-5.6-terra` | $12 | 757M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $10 | 909M | 872M | no | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $10 | 909M | 872M | no | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $15 | 606M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $15 | 606M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $9,086 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,212M | 872M | no | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $9,086 | DeepSeek `deepseek-v4-flash` | $0.28 | 32,451M | 872M | no | no |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $9,086 | DeepSeek `deepseek-v4-flash` | $0.28 | 32,451M | 872M | no | no |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $1,865 | OpenAI `gpt-5.6-terra` | $12 | 155M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $1,865 | Anthropic `Claude Sonnet 5` | $10 | 186M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $1,865 | Anthropic `Claude Sonnet 5` | $10 | 186M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $1,865 | Anthropic `Claude Sonnet 5` | $15 | 124M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $1,865 | Anthropic `Claude Sonnet 5` | $15 | 124M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $1,865 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 249M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $1,865 | DeepSeek `deepseek-v4-flash` | $0.28 | 6,660M | 755M | no | no |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $1,865 | DeepSeek `deepseek-v4-flash` | $0.28 | 6,660M | 755M | no | no |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $6,192 | OpenAI `gpt-5.6-terra` | $12 | 516M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $6,192 | Anthropic `Claude Sonnet 5` | $10 | 619M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $6,192 | Anthropic `Claude Sonnet 5` | $10 | 619M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $6,192 | Anthropic `Claude Sonnet 5` | $15 | 413M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $6,192 | Anthropic `Claude Sonnet 5` | $15 | 413M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $6,192 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 826M | 755M | no | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $6,192 | DeepSeek `deepseek-v4-flash` | $0.28 | 22,114M | 755M | no | no |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $6,192 | DeepSeek `deepseek-v4-flash` | $0.28 | 22,114M | 755M | no | no |
| gptoss120b | 2x H100 | $2,866 | OpenAI `gpt-5.6-terra` | $12 | 239M | 512M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $10 | 287M | 512M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $10 | 287M | 512M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $15 | 191M | 512M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $15 | 191M | 512M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 382M | 512M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | DeepSeek `deepseek-v4-flash` | $0.28 | 10,234M | 512M | no | no |
| gptoss120b | 2x H100 | $2,866 | DeepSeek `deepseek-v4-flash` | $0.28 | 10,234M | 512M | no | no |
| gptoss120b | 2x H100 | $8,870 | OpenAI `gpt-5.6-terra` | $12 | 739M | 512M | no | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $10 | 887M | 512M | no | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $10 | 887M | 512M | no | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $15 | 591M | 512M | no | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $15 | 591M | 512M | no | yes |
| gptoss120b | 2x H100 | $8,870 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,183M | 512M | no | yes |
| gptoss120b | 2x H100 | $8,870 | DeepSeek `deepseek-v4-flash` | $0.28 | 31,680M | 512M | no | no |
| gptoss120b | 2x H100 | $8,870 | DeepSeek `deepseek-v4-flash` | $0.28 | 31,680M | 512M | no | no |
| gptoss120b | 2x H100 | $2,866 | OpenAI `gpt-5.6-terra` | $12 | 239M | 776M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $10 | 287M | 776M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $10 | 287M | 776M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $15 | 191M | 776M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $15 | 191M | 776M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 382M | 776M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | DeepSeek `deepseek-v4-flash` | $0.28 | 10,234M | 776M | no | no |
| gptoss120b | 2x H100 | $2,866 | DeepSeek `deepseek-v4-flash` | $0.28 | 10,234M | 776M | no | no |
| gptoss120b | 2x H100 | $8,870 | OpenAI `gpt-5.6-terra` | $12 | 739M | 776M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $10 | 887M | 776M | no | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $10 | 887M | 776M | no | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $15 | 591M | 776M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $15 | 591M | 776M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,183M | 776M | no | yes |
| gptoss120b | 2x H100 | $8,870 | DeepSeek `deepseek-v4-flash` | $0.28 | 31,680M | 776M | no | no |
| gptoss120b | 2x H100 | $8,870 | DeepSeek `deepseek-v4-flash` | $0.28 | 31,680M | 776M | no | no |
| gptoss120b | 2x H100 | $2,866 | OpenAI `gpt-5.6-terra` | $12 | 239M | 1,077M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $10 | 287M | 1,077M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $10 | 287M | 1,077M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $15 | 191M | 1,077M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $15 | 191M | 1,077M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 382M | 1,077M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | DeepSeek `deepseek-v4-flash` | $0.28 | 10,234M | 1,077M | no | no |
| gptoss120b | 2x H100 | $2,866 | DeepSeek `deepseek-v4-flash` | $0.28 | 10,234M | 1,077M | no | no |
| gptoss120b | 2x H100 | $8,870 | OpenAI `gpt-5.6-terra` | $12 | 739M | 1,077M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $10 | 887M | 1,077M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $10 | 887M | 1,077M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $15 | 591M | 1,077M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $15 | 591M | 1,077M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,183M | 1,077M | no | yes |
| gptoss120b | 2x H100 | $8,870 | DeepSeek `deepseek-v4-flash` | $0.28 | 31,680M | 1,077M | no | no |
| gptoss120b | 2x H100 | $8,870 | DeepSeek `deepseek-v4-flash` | $0.28 | 31,680M | 1,077M | no | no |
| gptoss120b | 2x H100 | $2,866 | OpenAI `gpt-5.6-terra` | $12 | 239M | 1,419M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $10 | 287M | 1,419M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $10 | 287M | 1,419M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $15 | 191M | 1,419M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $15 | 191M | 1,419M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 382M | 1,419M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | DeepSeek `deepseek-v4-flash` | $0.28 | 10,234M | 1,419M | no | no |
| gptoss120b | 2x H100 | $2,866 | DeepSeek `deepseek-v4-flash` | $0.28 | 10,234M | 1,419M | no | no |
| gptoss120b | 2x H100 | $8,870 | OpenAI `gpt-5.6-terra` | $12 | 739M | 1,419M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $10 | 887M | 1,419M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $10 | 887M | 1,419M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $15 | 591M | 1,419M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $15 | 591M | 1,419M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,183M | 1,419M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | DeepSeek `deepseek-v4-flash` | $0.28 | 31,680M | 1,419M | no | no |
| gptoss120b | 2x H100 | $8,870 | DeepSeek `deepseek-v4-flash` | $0.28 | 31,680M | 1,419M | no | no |
| gptoss120b | 2x H100 | $2,866 | OpenAI `gpt-5.6-terra` | $12 | 239M | 1,774M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $10 | 287M | 1,774M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $10 | 287M | 1,774M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $15 | 191M | 1,774M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Anthropic `Claude Sonnet 5` | $15 | 191M | 1,774M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 382M | 1,774M | yes | yes |
| gptoss120b | 2x H100 | $2,866 | DeepSeek `deepseek-v4-flash` | $0.28 | 10,234M | 1,774M | no | no |
| gptoss120b | 2x H100 | $2,866 | DeepSeek `deepseek-v4-flash` | $0.28 | 10,234M | 1,774M | no | no |
| gptoss120b | 2x H100 | $8,870 | OpenAI `gpt-5.6-terra` | $12 | 739M | 1,774M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $10 | 887M | 1,774M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $10 | 887M | 1,774M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $15 | 591M | 1,774M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Anthropic `Claude Sonnet 5` | $15 | 591M | 1,774M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,183M | 1,774M | yes | yes |
| gptoss120b | 2x H100 | $8,870 | DeepSeek `deepseek-v4-flash` | $0.28 | 31,680M | 1,774M | no | no |
| gptoss120b | 2x H100 | $8,870 | DeepSeek `deepseek-v4-flash` | $0.28 | 31,680M | 1,774M | no | no |
| gptoss120b | 2x H200 | $5,170 | OpenAI `gpt-5.6-terra` | $12 | 431M | 539M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $10 | 517M | 539M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $10 | 517M | 539M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $15 | 345M | 539M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $15 | 345M | 539M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 689M | 539M | no | yes |
| gptoss120b | 2x H200 | $5,170 | DeepSeek `deepseek-v4-flash` | $0.28 | 18,463M | 539M | no | no |
| gptoss120b | 2x H200 | $5,170 | DeepSeek `deepseek-v4-flash` | $0.28 | 18,463M | 539M | no | no |
| gptoss120b | 2x H200 | $9,086 | OpenAI `gpt-5.6-terra` | $12 | 757M | 539M | no | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $10 | 909M | 539M | no | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $10 | 909M | 539M | no | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $15 | 606M | 539M | no | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $15 | 606M | 539M | no | yes |
| gptoss120b | 2x H200 | $9,086 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,212M | 539M | no | yes |
| gptoss120b | 2x H200 | $9,086 | DeepSeek `deepseek-v4-flash` | $0.28 | 32,451M | 539M | no | no |
| gptoss120b | 2x H200 | $9,086 | DeepSeek `deepseek-v4-flash` | $0.28 | 32,451M | 539M | no | no |
| gptoss120b | 2x H200 | $5,170 | OpenAI `gpt-5.6-terra` | $12 | 431M | 335M | no | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $10 | 517M | 335M | no | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $10 | 517M | 335M | no | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $15 | 345M | 335M | no | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $15 | 345M | 335M | no | yes |
| gptoss120b | 2x H200 | $5,170 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 689M | 335M | no | yes |
| gptoss120b | 2x H200 | $5,170 | DeepSeek `deepseek-v4-flash` | $0.28 | 18,463M | 335M | no | no |
| gptoss120b | 2x H200 | $5,170 | DeepSeek `deepseek-v4-flash` | $0.28 | 18,463M | 335M | no | no |
| gptoss120b | 2x H200 | $9,086 | OpenAI `gpt-5.6-terra` | $12 | 757M | 335M | no | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $10 | 909M | 335M | no | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $10 | 909M | 335M | no | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $15 | 606M | 335M | no | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $15 | 606M | 335M | no | yes |
| gptoss120b | 2x H200 | $9,086 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,212M | 335M | no | no |
| gptoss120b | 2x H200 | $9,086 | DeepSeek `deepseek-v4-flash` | $0.28 | 32,451M | 335M | no | no |
| gptoss120b | 2x H200 | $9,086 | DeepSeek `deepseek-v4-flash` | $0.28 | 32,451M | 335M | no | no |
| gptoss120b | 2x H200 | $5,170 | OpenAI `gpt-5.6-terra` | $12 | 431M | 1,130M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $10 | 517M | 1,130M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $10 | 517M | 1,130M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $15 | 345M | 1,130M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $15 | 345M | 1,130M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 689M | 1,130M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | DeepSeek `deepseek-v4-flash` | $0.28 | 18,463M | 1,130M | no | no |
| gptoss120b | 2x H200 | $5,170 | DeepSeek `deepseek-v4-flash` | $0.28 | 18,463M | 1,130M | no | no |
| gptoss120b | 2x H200 | $9,086 | OpenAI `gpt-5.6-terra` | $12 | 757M | 1,130M | yes | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $10 | 909M | 1,130M | yes | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $10 | 909M | 1,130M | yes | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $15 | 606M | 1,130M | yes | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $15 | 606M | 1,130M | yes | yes |
| gptoss120b | 2x H200 | $9,086 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,212M | 1,130M | no | yes |
| gptoss120b | 2x H200 | $9,086 | DeepSeek `deepseek-v4-flash` | $0.28 | 32,451M | 1,130M | no | no |
| gptoss120b | 2x H200 | $9,086 | DeepSeek `deepseek-v4-flash` | $0.28 | 32,451M | 1,130M | no | no |
| gptoss120b | 2x H200 | $5,170 | OpenAI `gpt-5.6-terra` | $12 | 431M | 963M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $10 | 517M | 963M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $10 | 517M | 963M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $15 | 345M | 963M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $15 | 345M | 963M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 689M | 963M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | DeepSeek `deepseek-v4-flash` | $0.28 | 18,463M | 963M | no | no |
| gptoss120b | 2x H200 | $5,170 | DeepSeek `deepseek-v4-flash` | $0.28 | 18,463M | 963M | no | no |
| gptoss120b | 2x H200 | $9,086 | OpenAI `gpt-5.6-terra` | $12 | 757M | 963M | yes | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $10 | 909M | 963M | yes | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $10 | 909M | 963M | yes | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $15 | 606M | 963M | yes | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $15 | 606M | 963M | yes | yes |
| gptoss120b | 2x H200 | $9,086 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,212M | 963M | no | yes |
| gptoss120b | 2x H200 | $9,086 | DeepSeek `deepseek-v4-flash` | $0.28 | 32,451M | 963M | no | no |
| gptoss120b | 2x H200 | $9,086 | DeepSeek `deepseek-v4-flash` | $0.28 | 32,451M | 963M | no | no |
| gptoss120b | 2x H200 | $5,170 | OpenAI `gpt-5.6-terra` | $12 | 431M | 1,883M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $10 | 517M | 1,883M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $10 | 517M | 1,883M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $15 | 345M | 1,883M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $15 | 345M | 1,883M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 689M | 1,883M | yes | yes |
| gptoss120b | 2x H200 | $5,170 | DeepSeek `deepseek-v4-flash` | $0.28 | 18,463M | 1,883M | no | no |
| gptoss120b | 2x H200 | $5,170 | DeepSeek `deepseek-v4-flash` | $0.28 | 18,463M | 1,883M | no | no |
| gptoss120b | 2x H200 | $9,086 | OpenAI `gpt-5.6-terra` | $12 | 757M | 1,883M | yes | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $10 | 909M | 1,883M | yes | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $10 | 909M | 1,883M | yes | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $15 | 606M | 1,883M | yes | yes |
| gptoss120b | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $15 | 606M | 1,883M | yes | yes |
| gptoss120b | 2x H200 | $9,086 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,212M | 1,883M | yes | yes |
| gptoss120b | 2x H200 | $9,086 | DeepSeek `deepseek-v4-flash` | $0.28 | 32,451M | 1,883M | no | no |
| gptoss120b | 2x H200 | $9,086 | DeepSeek `deepseek-v4-flash` | $0.28 | 32,451M | 1,883M | no | no |
| qwen3.5 | 8x H100 | $11,462 | OpenAI `gpt-5.6-terra` | $12 | 955M | 124M | no | no |
| qwen3.5 | 8x H100 | $11,462 | Anthropic `Claude Sonnet 5` | $10 | 1,146M | 124M | no | no |
| qwen3.5 | 8x H100 | $11,462 | Anthropic `Claude Sonnet 5` | $10 | 1,146M | 124M | no | no |
| qwen3.5 | 8x H100 | $11,462 | Anthropic `Claude Sonnet 5` | $15 | 764M | 124M | no | no |
| qwen3.5 | 8x H100 | $11,462 | Anthropic `Claude Sonnet 5` | $15 | 764M | 124M | no | no |
| qwen3.5 | 8x H100 | $11,462 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,528M | 124M | no | no |
| qwen3.5 | 8x H100 | $11,462 | DeepSeek `deepseek-v4-flash` | $0.28 | 40,937M | 124M | no | no |
| qwen3.5 | 8x H100 | $11,462 | DeepSeek `deepseek-v4-flash` | $0.28 | 40,937M | 124M | no | no |
| qwen3.5 | 8x H100 | $35,482 | OpenAI `gpt-5.6-terra` | $12 | 2,957M | 124M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Anthropic `Claude Sonnet 5` | $10 | 3,548M | 124M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Anthropic `Claude Sonnet 5` | $10 | 3,548M | 124M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Anthropic `Claude Sonnet 5` | $15 | 2,365M | 124M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Anthropic `Claude Sonnet 5` | $15 | 2,365M | 124M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 4,731M | 124M | no | no |
| qwen3.5 | 8x H100 | $35,482 | DeepSeek `deepseek-v4-flash` | $0.28 | 126,720M | 124M | no | no |
| qwen3.5 | 8x H100 | $35,482 | DeepSeek `deepseek-v4-flash` | $0.28 | 126,720M | 124M | no | no |
| qwen3.5 | 8x H100 | $11,462 | OpenAI `gpt-5.6-terra` | $12 | 955M | 217M | no | no |
| qwen3.5 | 8x H100 | $11,462 | Anthropic `Claude Sonnet 5` | $10 | 1,146M | 217M | no | no |
| qwen3.5 | 8x H100 | $11,462 | Anthropic `Claude Sonnet 5` | $10 | 1,146M | 217M | no | no |
| qwen3.5 | 8x H100 | $11,462 | Anthropic `Claude Sonnet 5` | $15 | 764M | 217M | no | no |
| qwen3.5 | 8x H100 | $11,462 | Anthropic `Claude Sonnet 5` | $15 | 764M | 217M | no | no |
| qwen3.5 | 8x H100 | $11,462 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,528M | 217M | no | no |
| qwen3.5 | 8x H100 | $11,462 | DeepSeek `deepseek-v4-flash` | $0.28 | 40,937M | 217M | no | no |
| qwen3.5 | 8x H100 | $11,462 | DeepSeek `deepseek-v4-flash` | $0.28 | 40,937M | 217M | no | no |
| qwen3.5 | 8x H100 | $35,482 | OpenAI `gpt-5.6-terra` | $12 | 2,957M | 217M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Anthropic `Claude Sonnet 5` | $10 | 3,548M | 217M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Anthropic `Claude Sonnet 5` | $10 | 3,548M | 217M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Anthropic `Claude Sonnet 5` | $15 | 2,365M | 217M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Anthropic `Claude Sonnet 5` | $15 | 2,365M | 217M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 4,731M | 217M | no | no |
| qwen3.5 | 8x H100 | $35,482 | DeepSeek `deepseek-v4-flash` | $0.28 | 126,720M | 217M | no | no |
| qwen3.5 | 8x H100 | $35,482 | DeepSeek `deepseek-v4-flash` | $0.28 | 126,720M | 217M | no | no |
| qwen3.5 | 8x H100 | $11,462 | OpenAI `gpt-5.6-terra` | $12 | 955M | 356M | no | yes |
| qwen3.5 | 8x H100 | $11,462 | Anthropic `Claude Sonnet 5` | $10 | 1,146M | 356M | no | no |
| qwen3.5 | 8x H100 | $11,462 | Anthropic `Claude Sonnet 5` | $10 | 1,146M | 356M | no | no |
| qwen3.5 | 8x H100 | $11,462 | Anthropic `Claude Sonnet 5` | $15 | 764M | 356M | no | yes |
| qwen3.5 | 8x H100 | $11,462 | Anthropic `Claude Sonnet 5` | $15 | 764M | 356M | no | yes |
| qwen3.5 | 8x H100 | $11,462 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,528M | 356M | no | no |
| qwen3.5 | 8x H100 | $11,462 | DeepSeek `deepseek-v4-flash` | $0.28 | 40,937M | 356M | no | no |
| qwen3.5 | 8x H100 | $11,462 | DeepSeek `deepseek-v4-flash` | $0.28 | 40,937M | 356M | no | no |
| qwen3.5 | 8x H100 | $35,482 | OpenAI `gpt-5.6-terra` | $12 | 2,957M | 356M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Anthropic `Claude Sonnet 5` | $10 | 3,548M | 356M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Anthropic `Claude Sonnet 5` | $10 | 3,548M | 356M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Anthropic `Claude Sonnet 5` | $15 | 2,365M | 356M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Anthropic `Claude Sonnet 5` | $15 | 2,365M | 356M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 4,731M | 356M | no | no |
| qwen3.5 | 8x H100 | $35,482 | DeepSeek `deepseek-v4-flash` | $0.28 | 126,720M | 356M | no | no |
| qwen3.5 | 8x H100 | $35,482 | DeepSeek `deepseek-v4-flash` | $0.28 | 126,720M | 356M | no | no |
| qwen3.5 | 8x H100 | $11,462 | OpenAI `gpt-5.6-terra` | $12 | 955M | 367M | no | yes |
| qwen3.5 | 8x H100 | $11,462 | Anthropic `Claude Sonnet 5` | $10 | 1,146M | 367M | no | no |
| qwen3.5 | 8x H100 | $11,462 | Anthropic `Claude Sonnet 5` | $10 | 1,146M | 367M | no | no |
| qwen3.5 | 8x H100 | $11,462 | Anthropic `Claude Sonnet 5` | $15 | 764M | 367M | no | yes |
| qwen3.5 | 8x H100 | $11,462 | Anthropic `Claude Sonnet 5` | $15 | 764M | 367M | no | yes |
| qwen3.5 | 8x H100 | $11,462 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,528M | 367M | no | no |
| qwen3.5 | 8x H100 | $11,462 | DeepSeek `deepseek-v4-flash` | $0.28 | 40,937M | 367M | no | no |
| qwen3.5 | 8x H100 | $11,462 | DeepSeek `deepseek-v4-flash` | $0.28 | 40,937M | 367M | no | no |
| qwen3.5 | 8x H100 | $35,482 | OpenAI `gpt-5.6-terra` | $12 | 2,957M | 367M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Anthropic `Claude Sonnet 5` | $10 | 3,548M | 367M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Anthropic `Claude Sonnet 5` | $10 | 3,548M | 367M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Anthropic `Claude Sonnet 5` | $15 | 2,365M | 367M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Anthropic `Claude Sonnet 5` | $15 | 2,365M | 367M | no | no |
| qwen3.5 | 8x H100 | $35,482 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 4,731M | 367M | no | no |
| qwen3.5 | 8x H100 | $35,482 | DeepSeek `deepseek-v4-flash` | $0.28 | 126,720M | 367M | no | no |
| qwen3.5 | 8x H100 | $35,482 | DeepSeek `deepseek-v4-flash` | $0.28 | 126,720M | 367M | no | no |
| llama_13b | 1x H200 | $2,585 | OpenAI `gpt-5.6-terra` | $12 | 215M | 9,190M | yes | yes |
| llama_13b | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $10 | 258M | 9,190M | yes | yes |
| llama_13b | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $10 | 258M | 9,190M | yes | yes |
| llama_13b | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $15 | 172M | 9,190M | yes | yes |
| llama_13b | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $15 | 172M | 9,190M | yes | yes |
| llama_13b | 1x H200 | $2,585 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 345M | 9,190M | yes | yes |
| llama_13b | 1x H200 | $2,585 | DeepSeek `deepseek-v4-flash` | $0.28 | 9,231M | 9,190M | no | yes |
| llama_13b | 1x H200 | $2,585 | DeepSeek `deepseek-v4-flash` | $0.28 | 9,231M | 9,190M | no | yes |
| llama_13b | 1x H200 | $4,543 | OpenAI `gpt-5.6-terra` | $12 | 379M | 9,190M | yes | yes |
| llama_13b | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $10 | 454M | 9,190M | yes | yes |
| llama_13b | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $10 | 454M | 9,190M | yes | yes |
| llama_13b | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $15 | 303M | 9,190M | yes | yes |
| llama_13b | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $15 | 303M | 9,190M | yes | yes |
| llama_13b | 1x H200 | $4,543 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 606M | 9,190M | yes | yes |
| llama_13b | 1x H200 | $4,543 | DeepSeek `deepseek-v4-flash` | $0.28 | 16,226M | 9,190M | no | yes |
| llama_13b | 1x H200 | $4,543 | DeepSeek `deepseek-v4-flash` | $0.28 | 16,226M | 9,190M | no | yes |
| llama_13b | 1x H200 | $2,585 | OpenAI `gpt-5.6-terra` | $12 | 215M | 3,694M | yes | yes |
| llama_13b | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $10 | 258M | 3,694M | yes | yes |
| llama_13b | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $10 | 258M | 3,694M | yes | yes |
| llama_13b | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $15 | 172M | 3,694M | yes | yes |
| llama_13b | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $15 | 172M | 3,694M | yes | yes |
| llama_13b | 1x H200 | $2,585 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 345M | 3,694M | yes | yes |
| llama_13b | 1x H200 | $2,585 | DeepSeek `deepseek-v4-flash` | $0.28 | 9,231M | 3,694M | no | yes |
| llama_13b | 1x H200 | $2,585 | DeepSeek `deepseek-v4-flash` | $0.28 | 9,231M | 3,694M | no | yes |
| llama_13b | 1x H200 | $4,543 | OpenAI `gpt-5.6-terra` | $12 | 379M | 3,694M | yes | yes |
| llama_13b | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $10 | 454M | 3,694M | yes | yes |
| llama_13b | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $10 | 454M | 3,694M | yes | yes |
| llama_13b | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $15 | 303M | 3,694M | yes | yes |
| llama_13b | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $15 | 303M | 3,694M | yes | yes |
| llama_13b | 1x H200 | $4,543 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 606M | 3,694M | yes | yes |
| llama_13b | 1x H200 | $4,543 | DeepSeek `deepseek-v4-flash` | $0.28 | 16,226M | 3,694M | no | no |
| llama_13b | 1x H200 | $4,543 | DeepSeek `deepseek-v4-flash` | $0.28 | 16,226M | 3,694M | no | no |
| llama_13b | 1x H200 | $2,585 | OpenAI `gpt-5.6-terra` | $12 | 215M | 1,049M | yes | yes |
| llama_13b | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $10 | 258M | 1,049M | yes | yes |
| llama_13b | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $10 | 258M | 1,049M | yes | yes |
| llama_13b | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $15 | 172M | 1,049M | yes | yes |
| llama_13b | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $15 | 172M | 1,049M | yes | yes |
| llama_13b | 1x H200 | $2,585 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 345M | 1,049M | yes | yes |
| llama_13b | 1x H200 | $2,585 | DeepSeek `deepseek-v4-flash` | $0.28 | 9,231M | 1,049M | no | no |
| llama_13b | 1x H200 | $2,585 | DeepSeek `deepseek-v4-flash` | $0.28 | 9,231M | 1,049M | no | no |
| llama_13b | 1x H200 | $4,543 | OpenAI `gpt-5.6-terra` | $12 | 379M | 1,049M | yes | yes |
| llama_13b | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $10 | 454M | 1,049M | yes | yes |
| llama_13b | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $10 | 454M | 1,049M | yes | yes |
| llama_13b | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $15 | 303M | 1,049M | yes | yes |
| llama_13b | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $15 | 303M | 1,049M | yes | yes |
| llama_13b | 1x H200 | $4,543 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 606M | 1,049M | yes | yes |
| llama_13b | 1x H200 | $4,543 | DeepSeek `deepseek-v4-flash` | $0.28 | 16,226M | 1,049M | no | no |
| llama_13b | 1x H200 | $4,543 | DeepSeek `deepseek-v4-flash` | $0.28 | 16,226M | 1,049M | no | no |
| Llama-70B | 1x H200 | $2,585 | OpenAI `gpt-5.6-terra` | $12 | 215M | 2,957M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $10 | 258M | 2,957M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $10 | 258M | 2,957M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $15 | 172M | 2,957M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $15 | 172M | 2,957M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 345M | 2,957M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | DeepSeek `deepseek-v4-flash` | $0.28 | 9,231M | 2,957M | no | no |
| Llama-70B | 1x H200 | $2,585 | DeepSeek `deepseek-v4-flash` | $0.28 | 9,231M | 2,957M | no | no |
| Llama-70B | 1x H200 | $4,543 | OpenAI `gpt-5.6-terra` | $12 | 379M | 2,957M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $10 | 454M | 2,957M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $10 | 454M | 2,957M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $15 | 303M | 2,957M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $15 | 303M | 2,957M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 606M | 2,957M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | DeepSeek `deepseek-v4-flash` | $0.28 | 16,226M | 2,957M | no | no |
| Llama-70B | 1x H200 | $4,543 | DeepSeek `deepseek-v4-flash` | $0.28 | 16,226M | 2,957M | no | no |
| Llama-70B | 8x H200 | $20,678 | OpenAI `gpt-5.6-terra` | $12 | 1,723M | 2,957M | yes | yes |
| Llama-70B | 8x H200 | $20,678 | Anthropic `Claude Sonnet 5` | $10 | 2,068M | 2,957M | yes | yes |
| Llama-70B | 8x H200 | $20,678 | Anthropic `Claude Sonnet 5` | $10 | 2,068M | 2,957M | yes | yes |
| Llama-70B | 8x H200 | $20,678 | Anthropic `Claude Sonnet 5` | $15 | 1,379M | 2,957M | yes | yes |
| Llama-70B | 8x H200 | $20,678 | Anthropic `Claude Sonnet 5` | $15 | 1,379M | 2,957M | yes | yes |
| Llama-70B | 8x H200 | $20,678 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 2,757M | 2,957M | yes | yes |
| Llama-70B | 8x H200 | $20,678 | DeepSeek `deepseek-v4-flash` | $0.28 | 73,851M | 2,957M | no | no |
| Llama-70B | 8x H200 | $20,678 | DeepSeek `deepseek-v4-flash` | $0.28 | 73,851M | 2,957M | no | no |
| Llama-70B | 8x H200 | $36,346 | OpenAI `gpt-5.6-terra` | $12 | 3,029M | 2,957M | no | yes |
| Llama-70B | 8x H200 | $36,346 | Anthropic `Claude Sonnet 5` | $10 | 3,635M | 2,957M | no | yes |
| Llama-70B | 8x H200 | $36,346 | Anthropic `Claude Sonnet 5` | $10 | 3,635M | 2,957M | no | yes |
| Llama-70B | 8x H200 | $36,346 | Anthropic `Claude Sonnet 5` | $15 | 2,423M | 2,957M | yes | yes |
| Llama-70B | 8x H200 | $36,346 | Anthropic `Claude Sonnet 5` | $15 | 2,423M | 2,957M | yes | yes |
| Llama-70B | 8x H200 | $36,346 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 4,846M | 2,957M | no | yes |
| Llama-70B | 8x H200 | $36,346 | DeepSeek `deepseek-v4-flash` | $0.28 | 129,806M | 2,957M | no | no |
| Llama-70B | 8x H200 | $36,346 | DeepSeek `deepseek-v4-flash` | $0.28 | 129,806M | 2,957M | no | no |
| Llama-70B | 1x H200 | $2,585 | OpenAI `gpt-5.6-terra` | $12 | 215M | 2,287M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $10 | 258M | 2,287M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $10 | 258M | 2,287M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $15 | 172M | 2,287M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $15 | 172M | 2,287M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 345M | 2,287M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | DeepSeek `deepseek-v4-flash` | $0.28 | 9,231M | 2,287M | no | no |
| Llama-70B | 1x H200 | $2,585 | DeepSeek `deepseek-v4-flash` | $0.28 | 9,231M | 2,287M | no | no |
| Llama-70B | 1x H200 | $4,543 | OpenAI `gpt-5.6-terra` | $12 | 379M | 2,287M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $10 | 454M | 2,287M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $10 | 454M | 2,287M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $15 | 303M | 2,287M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $15 | 303M | 2,287M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 606M | 2,287M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | DeepSeek `deepseek-v4-flash` | $0.28 | 16,226M | 2,287M | no | no |
| Llama-70B | 1x H200 | $4,543 | DeepSeek `deepseek-v4-flash` | $0.28 | 16,226M | 2,287M | no | no |
| Llama-70B | 8x H200 | $20,678 | OpenAI `gpt-5.6-terra` | $12 | 1,723M | 2,460M | yes | yes |
| Llama-70B | 8x H200 | $20,678 | Anthropic `Claude Sonnet 5` | $10 | 2,068M | 2,460M | yes | yes |
| Llama-70B | 8x H200 | $20,678 | Anthropic `Claude Sonnet 5` | $10 | 2,068M | 2,460M | yes | yes |
| Llama-70B | 8x H200 | $20,678 | Anthropic `Claude Sonnet 5` | $15 | 1,379M | 2,460M | yes | yes |
| Llama-70B | 8x H200 | $20,678 | Anthropic `Claude Sonnet 5` | $15 | 1,379M | 2,460M | yes | yes |
| Llama-70B | 8x H200 | $20,678 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 2,757M | 2,460M | no | yes |
| Llama-70B | 8x H200 | $20,678 | DeepSeek `deepseek-v4-flash` | $0.28 | 73,851M | 2,460M | no | no |
| Llama-70B | 8x H200 | $20,678 | DeepSeek `deepseek-v4-flash` | $0.28 | 73,851M | 2,460M | no | no |
| Llama-70B | 8x H200 | $36,346 | OpenAI `gpt-5.6-terra` | $12 | 3,029M | 2,460M | no | yes |
| Llama-70B | 8x H200 | $36,346 | Anthropic `Claude Sonnet 5` | $10 | 3,635M | 2,460M | no | yes |
| Llama-70B | 8x H200 | $36,346 | Anthropic `Claude Sonnet 5` | $10 | 3,635M | 2,460M | no | yes |
| Llama-70B | 8x H200 | $36,346 | Anthropic `Claude Sonnet 5` | $15 | 2,423M | 2,460M | yes | yes |
| Llama-70B | 8x H200 | $36,346 | Anthropic `Claude Sonnet 5` | $15 | 2,423M | 2,460M | yes | yes |
| Llama-70B | 8x H200 | $36,346 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 4,846M | 2,460M | no | yes |
| Llama-70B | 8x H200 | $36,346 | DeepSeek `deepseek-v4-flash` | $0.28 | 129,806M | 2,460M | no | no |
| Llama-70B | 8x H200 | $36,346 | DeepSeek `deepseek-v4-flash` | $0.28 | 129,806M | 2,460M | no | no |
| Llama-70B | 1x H200 | $2,585 | OpenAI `gpt-5.6-terra` | $12 | 215M | 1,513M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $10 | 258M | 1,513M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $10 | 258M | 1,513M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $15 | 172M | 1,513M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | Anthropic `Claude Sonnet 5` | $15 | 172M | 1,513M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 345M | 1,513M | yes | yes |
| Llama-70B | 1x H200 | $2,585 | DeepSeek `deepseek-v4-flash` | $0.28 | 9,231M | 1,513M | no | no |
| Llama-70B | 1x H200 | $2,585 | DeepSeek `deepseek-v4-flash` | $0.28 | 9,231M | 1,513M | no | no |
| Llama-70B | 1x H200 | $4,543 | OpenAI `gpt-5.6-terra` | $12 | 379M | 1,513M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $10 | 454M | 1,513M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $10 | 454M | 1,513M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $15 | 303M | 1,513M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | Anthropic `Claude Sonnet 5` | $15 | 303M | 1,513M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 606M | 1,513M | yes | yes |
| Llama-70B | 1x H200 | $4,543 | DeepSeek `deepseek-v4-flash` | $0.28 | 16,226M | 1,513M | no | no |
| Llama-70B | 1x H200 | $4,543 | DeepSeek `deepseek-v4-flash` | $0.28 | 16,226M | 1,513M | no | no |
| Llama-70B | 8x H200 | $20,678 | OpenAI `gpt-5.6-terra` | $12 | 1,723M | 1,760M | yes | yes |
| Llama-70B | 8x H200 | $20,678 | Anthropic `Claude Sonnet 5` | $10 | 2,068M | 1,760M | no | yes |
| Llama-70B | 8x H200 | $20,678 | Anthropic `Claude Sonnet 5` | $10 | 2,068M | 1,760M | no | yes |
| Llama-70B | 8x H200 | $20,678 | Anthropic `Claude Sonnet 5` | $15 | 1,379M | 1,760M | yes | yes |
| Llama-70B | 8x H200 | $20,678 | Anthropic `Claude Sonnet 5` | $15 | 1,379M | 1,760M | yes | yes |
| Llama-70B | 8x H200 | $20,678 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 2,757M | 1,760M | no | yes |
| Llama-70B | 8x H200 | $20,678 | DeepSeek `deepseek-v4-flash` | $0.28 | 73,851M | 1,760M | no | no |
| Llama-70B | 8x H200 | $20,678 | DeepSeek `deepseek-v4-flash` | $0.28 | 73,851M | 1,760M | no | no |
| Llama-70B | 8x H200 | $36,346 | OpenAI `gpt-5.6-terra` | $12 | 3,029M | 1,760M | no | yes |
| Llama-70B | 8x H200 | $36,346 | Anthropic `Claude Sonnet 5` | $10 | 3,635M | 1,760M | no | yes |
| Llama-70B | 8x H200 | $36,346 | Anthropic `Claude Sonnet 5` | $10 | 3,635M | 1,760M | no | yes |
| Llama-70B | 8x H200 | $36,346 | Anthropic `Claude Sonnet 5` | $15 | 2,423M | 1,760M | no | yes |
| Llama-70B | 8x H200 | $36,346 | Anthropic `Claude Sonnet 5` | $15 | 2,423M | 1,760M | no | yes |
| Llama-70B | 8x H200 | $36,346 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 4,846M | 1,760M | no | yes |
| Llama-70B | 8x H200 | $36,346 | DeepSeek `deepseek-v4-flash` | $0.28 | 129,806M | 1,760M | no | no |
| Llama-70B | 8x H200 | $36,346 | DeepSeek `deepseek-v4-flash` | $0.28 | 129,806M | 1,760M | no | no |

When capacity is below break-even, the box cannot emit enough tokens to ever
beat that API price, at any volume. That is the common case against cheap
models, and it is why "self-host to save money" fails most often for exactly
the workloads people try it on first.

## Steal this stack

### `openai/gpt-oss-20b`

[model card](https://huggingface.co/openai/gpt-oss-20b) | 1x NVIDIA L40S 48 GB on [Runpod](https://www.runpod.io/gpu-models/l40s) | vLLM | MXFP4 MoE weights

The official card says the MXFP4 model runs within 16GB of memory; one Runpod L40S exposes 48 GB, leaving capacity for the runtime and KV cache.

```bash
docker run --rm --gpus all --ipc=host --network=host -v "${HOME}/.cache/huggingface:/root/.cache/huggingface" vllm/vllm-openai:v0.26.0 --model openai/gpt-oss-20b --port 8000
```

Reproduce a throughput number on it:

```bash
docker run --rm --network=host --entrypoint vllm vllm/vllm-openai:v0.26.0 bench serve --backend openai --endpoint /v1/completions --model openai/gpt-oss-20b --dataset-name random --num-prompts 1000 --random-input-len 1024 --random-output-len 128 --port 8000
```

Image `vllm/vllm-openai:v0.26.0` confirmed to exist at [https://hub.docker.com/v2/repositories/vllm/vllm-openai/tags/v0.26.0](https://hub.docker.com/v2/repositories/vllm/vllm-openai/tags/v0.26.0).

### `openai/gpt-oss-120b`

[model card](https://huggingface.co/openai/gpt-oss-120b) | 1x NVIDIA H100 80 GB on [Runpod](https://www.runpod.io/gpu-models/h100) | vLLM | MXFP4 MoE weights

The official card states that the 117B/5.1B-active MXFP4 model fits into a single 80GB GPU and names NVIDIA H100 as an example.

```bash
docker run --rm --gpus all --ipc=host --network=host -v "${HOME}/.cache/huggingface:/root/.cache/huggingface" vllm/vllm-openai:v0.26.0 --model openai/gpt-oss-120b --port 8000
```

Reproduce a throughput number on it:

```bash
docker run --rm --network=host --entrypoint vllm vllm/vllm-openai:v0.26.0 bench serve --backend openai --endpoint /v1/completions --model openai/gpt-oss-120b --dataset-name random --num-prompts 1000 --random-input-len 1024 --random-output-len 128 --port 8000
```

Image `vllm/vllm-openai:v0.26.0` confirmed to exist at [https://hub.docker.com/v2/repositories/vllm/vllm-openai/tags/v0.26.0](https://hub.docker.com/v2/repositories/vllm/vllm-openai/tags/v0.26.0).

### `mistralai/Mistral-Small-4-119B-2603`

[model card](https://huggingface.co/mistralai/Mistral-Small-4-119B-2603) | 2x NVIDIA H100 80 GB on [Runpod](https://www.runpod.io/gpu-models/h100) | vLLM | FP8

The official checkpoint is 119B with FP8 weights, and its official vLLM launch uses tensor parallel size 2; two Runpod H100 GPUs provide 80 GB each.

```bash
docker run --rm --gpus all --ipc=host --network=host -v "${HOME}/.cache/huggingface:/root/.cache/huggingface" vllm/vllm-openai:v0.26.0 --model mistralai/Mistral-Small-4-119B-2603 --port 8000 --max-model-len 262144 --tensor-parallel-size 2 --attention-backend FLASH_ATTN_MLA --tool-call-parser mistral --enable-auto-tool-choice --reasoning-parser mistral --max_num_batched_tokens 16384 --max_num_seqs 128 --gpu_memory_utilization 0.8
```

Reproduce a throughput number on it:

```bash
docker run --rm --network=host --entrypoint vllm vllm/vllm-openai:v0.26.0 bench serve --backend openai --endpoint /v1/completions --model mistralai/Mistral-Small-4-119B-2603 --dataset-name random --num-prompts 1000 --random-input-len 1024 --random-output-len 128 --port 8000
```

Image `vllm/vllm-openai:v0.26.0` confirmed to exist at [https://hub.docker.com/v2/repositories/vllm/vllm-openai/tags/v0.26.0](https://hub.docker.com/v2/repositories/vllm/vllm-openai/tags/v0.26.0).

### `Qwen/Qwen3.6-35B-A3B`

[model card](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) | 8x NVIDIA H100 80 GB on [Runpod](https://www.runpod.io/gpu-models/h100) | vLLM | BF16

The official 35B/3B-active BF16 card explicitly recommends tensor parallel on 8 GPUs for the 262,144-token endpoint; H100 is a listed 80 GB rental GPU.

```bash
docker run --rm --gpus all --ipc=host --network=host -v "${HOME}/.cache/huggingface:/root/.cache/huggingface" vllm/vllm-openai:v0.26.0 --model Qwen/Qwen3.6-35B-A3B --port 8000 --tensor-parallel-size 8 --max-model-len 262144 --reasoning-parser qwen3 --enable-auto-tool-choice --tool-call-parser qwen3_coder
```

Reproduce a throughput number on it:

```bash
docker run --rm --network=host --entrypoint vllm vllm/vllm-openai:v0.26.0 bench serve --backend openai --endpoint /v1/completions --model Qwen/Qwen3.6-35B-A3B --dataset-name random --num-prompts 1000 --random-input-len 1024 --random-output-len 128 --port 8000
```

Image `vllm/vllm-openai:v0.26.0` confirmed to exist at [https://hub.docker.com/v2/repositories/vllm/vllm-openai/tags/v0.26.0](https://hub.docker.com/v2/repositories/vllm/vllm-openai/tags/v0.26.0).

### `nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16`

[model card](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16) | 8x NVIDIA H100-80GB on [Runpod](https://www.runpod.io/gpu-models/h100) | vLLM | BF16 weights with FP8 KV cache

NVIDIA states a minimum requirement of 8 H100-80GB GPUs for the 120B/12B-active BF16 checkpoint.

```bash
docker run --rm --gpus all --ipc=host --network=host -v "${HOME}/.cache/huggingface:/root/.cache/huggingface" vllm/vllm-openai:v0.18.1 --model nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16 --port 8000 --async-scheduling --dtype auto --kv-cache-dtype fp8 --tensor-parallel-size 8 --max-model-len 262144 --enable-expert-parallel --swap-space 0 --trust-remote-code --gpu-memory-utilization 0.9 --max-cudagraph-capture-size 128 --enable-chunked-prefill --mamba-ssm-cache-dtype float32
```

Reproduce a throughput number on it:

```bash
docker run --rm --network=host --entrypoint vllm vllm/vllm-openai:v0.18.1 bench serve --backend openai --endpoint /v1/completions --model nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16 --dataset-name random --num-prompts 1000 --random-input-len 1024 --random-output-len 128 --port 8000
```

Image `vllm/vllm-openai:v0.18.1` confirmed to exist at [https://hub.docker.com/v2/repositories/vllm/vllm-openai/tags/v0.18.1](https://hub.docker.com/v2/repositories/vllm/vllm-openai/tags/v0.18.1).

## When the API is the right choice

Most of the time. Specifically:

- **Low or spiky volume.** Under roughly 100M output tokens a month against a
  cheap model, the GPU bill alone exceeds the API bill before you hire anyone.
- **No infra team.** The cost model below excludes engineer time. One engineer
  at a loaded $200k/year is about $16.7k/month, which buys a lot of tokens.
- **Bursty traffic.** You pay for idle GPUs. Utilization is the dominant term
  and burst traffic destroys it.
- **Strict latency floors.** High utilization means queueing. The cheap end of
  every self-hosted row assumes a saturated box, which is the opposite of a
  tight p99.
- **You need frontier capability.** No open model reaches the top closed tier,
  so category C is not on the menu.

Self-hosting wins on things that are not price: data residency, no rate limits,
model pinning, custom weights, and no vendor deprecation schedule. If you are
self-hosting, those are usually the honest reasons.

## Methodology

- Prices are read from official vendor pages only. No aggregators, no blogs.
  Each row carries `source_url` and `retrieved_on`.
- Every number in the data files was checked by three mechanical gates: the
  quoted literal must appear in a saved raw capture of the page, the numeric
  value must appear inside that literal, and the value must sit near its model
  name in the page. Scripts are in `scripts/`.
- GPU rates are on-demand per-GPU list prices. Reserved and spot rates are
  separate rows. Where a page was ambiguous about per-GPU versus per-node, the
  row is marked `UNCLEAR` rather than guessed, because that error is 8x.
- Throughput is cited with hardware, engine, version, precision, concurrency,
  and sequence lengths. Sources missing any of those are marked INCOMPLETE.
- Ranges are driven by utilization: low = 90%, mid = 30%, high = 10%.

**Excluded from the cost model, explicitly:** engineer time, storage, image
registry, network egress, cold starts, weight load time, idle outside the
assumed utilization, on-call, redundancy for uptime, load balancers, and
evaluation of the self-hosted model. Including any of them makes self-hosting
look worse, not better.

## Where this is wrong

Known weaknesses in our own model. This list is not decoration.

1. **The formula charges the entire GPU bill to output tokens.** Prefill burns
   real compute. For input-heavy workloads this overstates output cost.
2. **Utilization is assumed, not measured.** Every row is a straight-line
   assumption. Real deployments see diurnal traffic and idle overnight.
3. **The throughput points are somebody else's operating point.** The
   DeepSeek-R1 figure is at concurrency 32 and the MiniMax figure at 512. A
   throughput-tuned deployment would beat both and would look much cheaper.
   Cost per token is a function of the operating point, not of the hardware.
4. **Cited throughput is mostly vendor-adjacent.** Benchmarks are published by
   parties with an interest in the result, at favorable sequence lengths.
5. **Quantization is not held constant.** Comparing an FP4 self-hosted number
   against an API serving unknown precision is not apples to apples.
6. **On-demand is the worst GPU price.** Committed contracts cut it
   substantially and would improve every self-hosted row, at the cost of
   lock-in this model does not represent.
7. **Break-even uses uncached output price.** Agent workloads with long stable
   prefixes get cache discounts that move the API side sharply in its favor.
8. **The tokenizer corpus is one paragraph and one file.** It is not a
   representative sample of anyone's traffic.
9. **No latency or SLA modeling.** Nothing here says whether the cheap
   configuration meets your p99.

## Freshness and citation

Data files are refreshed on a rolling basis. Next planned refresh:
**2026-08-31**. Dated immutable snapshots are in `data/snapshots/`; past
snapshots are never edited. Price changes are logged in `CHANGELOG.md`.

```
RightNow AI, inference-cost-truth, snapshot 2026-07-31.
https://github.com/RightNow-AI/inference-cost-truth
Licensed CC BY 4.0.
```

Data files are licensed [CC BY 4.0](LICENSE-DATA). Reuse the numbers, link
back.

## Corrections

If a number here is wrong, open an issue with the source URL and it gets fixed.
Price and throughput PRs need the checklists in
[CONTRIBUTING.md](CONTRIBUTING.md).

Maintained by RightNow AI. We sell GPU kernel optimization at
[runinfra.ai](https://runinfra.ai).
