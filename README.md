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

## API pricing, closed vendors

Standard realtime tier. Batch, flex, fast, and long-context tiers are separate
rows in `data/providers.json` and are never blended into these numbers. Prices
are USD per 1M tokens **of that model's own tokens** -- see the normalization
section, because a token is not a fixed amount of text.

| Vendor | Model | Input /1M | Cached in | Cache write | Output /1M | Batch out | Source |
|---|---|---|---|---|---|---|---|
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
| xAI | `Grok 4.5` | $2 | not documented | not documented | $6 | -- | [src](https://docs.x.ai/developers/models) |

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
| DeepSeek-R1-0528 | 4x B200 | $24,768 | OpenAI `gpt-5.6-terra` | $12 | 2,064M | 1,157M | no | yes |
| DeepSeek-R1-0528 | 4x B200 | $24,768 | Anthropic `Claude Sonnet 5` | $10 | 2,477M | 1,157M | no | yes |
| DeepSeek-R1-0528 | 4x B200 | $24,768 | Anthropic `Claude Sonnet 5` | $10 | 2,477M | 1,157M | no | yes |
| DeepSeek-R1-0528 | 4x B200 | $24,768 | Anthropic `Claude Sonnet 5` | $15 | 1,651M | 1,157M | no | yes |
| DeepSeek-R1-0528 | 4x B200 | $24,768 | Anthropic `Claude Sonnet 5` | $15 | 1,651M | 1,157M | no | yes |
| DeepSeek-R1-0528 | 4x B200 | $24,768 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 3,302M | 1,157M | no | yes |
| DeepSeek-R1-0528 | 4x B200 | $24,768 | DeepSeek `deepseek-v4-flash` | $0.28 | 88,457M | 1,157M | no | no |
| DeepSeek-R1-0528 | 4x MI355X | $7,459 | OpenAI `gpt-5.6-terra` | $12 | 622M | 1,262M | yes | yes |
| DeepSeek-R1-0528 | 4x MI355X | $7,459 | Anthropic `Claude Sonnet 5` | $10 | 746M | 1,262M | yes | yes |
| DeepSeek-R1-0528 | 4x MI355X | $7,459 | Anthropic `Claude Sonnet 5` | $10 | 746M | 1,262M | yes | yes |
| DeepSeek-R1-0528 | 4x MI355X | $7,459 | Anthropic `Claude Sonnet 5` | $15 | 497M | 1,262M | yes | yes |
| DeepSeek-R1-0528 | 4x MI355X | $7,459 | Anthropic `Claude Sonnet 5` | $15 | 497M | 1,262M | yes | yes |
| DeepSeek-R1-0528 | 4x MI355X | $7,459 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 995M | 1,262M | yes | yes |
| DeepSeek-R1-0528 | 4x MI355X | $7,459 | DeepSeek `deepseek-v4-flash` | $0.28 | 26,640M | 1,262M | no | no |
| DeepSeek-R1-0528 | 4x MI355X | $24,768 | OpenAI `gpt-5.6-terra` | $12 | 2,064M | 1,262M | no | yes |
| DeepSeek-R1-0528 | 4x MI355X | $24,768 | Anthropic `Claude Sonnet 5` | $10 | 2,477M | 1,262M | no | yes |
| DeepSeek-R1-0528 | 4x MI355X | $24,768 | Anthropic `Claude Sonnet 5` | $10 | 2,477M | 1,262M | no | yes |
| DeepSeek-R1-0528 | 4x MI355X | $24,768 | Anthropic `Claude Sonnet 5` | $15 | 1,651M | 1,262M | no | yes |
| DeepSeek-R1-0528 | 4x MI355X | $24,768 | Anthropic `Claude Sonnet 5` | $15 | 1,651M | 1,262M | no | yes |
| DeepSeek-R1-0528 | 4x MI355X | $24,768 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 3,302M | 1,262M | no | yes |
| DeepSeek-R1-0528 | 4x MI355X | $24,768 | DeepSeek `deepseek-v4-flash` | $0.28 | 88,457M | 1,262M | no | no |
| MiniMax-M3 | 4x B300 | $19,987 | OpenAI `gpt-5.6-terra` | $12 | 1,666M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $19,987 | Anthropic `Claude Sonnet 5` | $10 | 1,999M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $19,987 | Anthropic `Claude Sonnet 5` | $10 | 1,999M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $19,987 | Anthropic `Claude Sonnet 5` | $15 | 1,332M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $19,987 | Anthropic `Claude Sonnet 5` | $15 | 1,332M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $19,987 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 2,665M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $19,987 | DeepSeek `deepseek-v4-flash` | $0.28 | 71,383M | 4,883M | no | no |
| MiniMax-M3 | 4x B300 | $22,608 | OpenAI `gpt-5.6-terra` | $12 | 1,884M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $22,608 | Anthropic `Claude Sonnet 5` | $10 | 2,261M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $22,608 | Anthropic `Claude Sonnet 5` | $10 | 2,261M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $22,608 | Anthropic `Claude Sonnet 5` | $15 | 1,507M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $22,608 | Anthropic `Claude Sonnet 5` | $15 | 1,507M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $22,608 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 3,014M | 4,883M | yes | yes |
| MiniMax-M3 | 4x B300 | $22,608 | DeepSeek `deepseek-v4-flash` | $0.28 | 80,743M | 4,883M | no | no |
| MiniMax-M3 | 4x MI355X | $7,459 | OpenAI `gpt-5.6-terra` | $12 | 622M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $7,459 | Anthropic `Claude Sonnet 5` | $10 | 746M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $7,459 | Anthropic `Claude Sonnet 5` | $10 | 746M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $7,459 | Anthropic `Claude Sonnet 5` | $15 | 497M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $7,459 | Anthropic `Claude Sonnet 5` | $15 | 497M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $7,459 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 995M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $7,459 | DeepSeek `deepseek-v4-flash` | $0.28 | 26,640M | 2,968M | no | no |
| MiniMax-M3 | 4x MI355X | $24,768 | OpenAI `gpt-5.6-terra` | $12 | 2,064M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $24,768 | Anthropic `Claude Sonnet 5` | $10 | 2,477M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $24,768 | Anthropic `Claude Sonnet 5` | $10 | 2,477M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $24,768 | Anthropic `Claude Sonnet 5` | $15 | 1,651M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $24,768 | Anthropic `Claude Sonnet 5` | $15 | 1,651M | 2,968M | yes | yes |
| MiniMax-M3 | 4x MI355X | $24,768 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 3,302M | 2,968M | no | yes |
| MiniMax-M3 | 4x MI355X | $24,768 | DeepSeek `deepseek-v4-flash` | $0.28 | 88,457M | 2,968M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | OpenAI `gpt-5.6-terra` | $12 | 1,243M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Anthropic `Claude Sonnet 5` | $10 | 1,492M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Anthropic `Claude Sonnet 5` | $10 | 1,492M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Anthropic `Claude Sonnet 5` | $15 | 995M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Anthropic `Claude Sonnet 5` | $15 | 995M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,989M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | DeepSeek `deepseek-v4-flash` | $0.28 | 53,280M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | OpenAI `gpt-5.6-terra` | $12 | 4,128M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Anthropic `Claude Sonnet 5` | $10 | 4,954M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Anthropic `Claude Sonnet 5` | $10 | 4,954M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Anthropic `Claude Sonnet 5` | $15 | 3,302M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Anthropic `Claude Sonnet 5` | $15 | 3,302M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 6,605M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | DeepSeek `deepseek-v4-flash` | $0.28 | 176,914M | 129M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | OpenAI `gpt-5.6-terra` | $12 | 1,243M | 821M | no | yes |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Anthropic `Claude Sonnet 5` | $10 | 1,492M | 821M | no | yes |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Anthropic `Claude Sonnet 5` | $10 | 1,492M | 821M | no | yes |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Anthropic `Claude Sonnet 5` | $15 | 995M | 821M | no | yes |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Anthropic `Claude Sonnet 5` | $15 | 995M | 821M | no | yes |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,989M | 821M | no | yes |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $14,918 | DeepSeek `deepseek-v4-flash` | $0.28 | 53,280M | 821M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | OpenAI `gpt-5.6-terra` | $12 | 4,128M | 821M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Anthropic `Claude Sonnet 5` | $10 | 4,954M | 821M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Anthropic `Claude Sonnet 5` | $10 | 4,954M | 821M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Anthropic `Claude Sonnet 5` | $15 | 3,302M | 821M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Anthropic `Claude Sonnet 5` | $15 | 3,302M | 821M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 6,605M | 821M | no | no |
| amd/Kimi-K2.5-MXFP4 | 8x MI355X | $49,536 | DeepSeek `deepseek-v4-flash` | $0.28 | 176,914M | 821M | no | no |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $5,170 | OpenAI `gpt-5.6-terra` | $12 | 431M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $10 | 517M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $10 | 517M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $15 | 345M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $5,170 | Anthropic `Claude Sonnet 5` | $15 | 345M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $5,170 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 689M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $5,170 | DeepSeek `deepseek-v4-flash` | $0.28 | 18,463M | 872M | no | no |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $9,086 | OpenAI `gpt-5.6-terra` | $12 | 757M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $10 | 909M | 872M | no | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $10 | 909M | 872M | no | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $15 | 606M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $9,086 | Anthropic `Claude Sonnet 5` | $15 | 606M | 872M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $9,086 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 1,212M | 872M | no | yes |
| Llama-3.3-70B-Instruct-FP8 | 2x H200 | $9,086 | DeepSeek `deepseek-v4-flash` | $0.28 | 32,451M | 872M | no | no |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $1,865 | OpenAI `gpt-5.6-terra` | $12 | 155M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $1,865 | Anthropic `Claude Sonnet 5` | $10 | 186M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $1,865 | Anthropic `Claude Sonnet 5` | $10 | 186M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $1,865 | Anthropic `Claude Sonnet 5` | $15 | 124M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $1,865 | Anthropic `Claude Sonnet 5` | $15 | 124M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $1,865 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 249M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $1,865 | DeepSeek `deepseek-v4-flash` | $0.28 | 6,660M | 755M | no | no |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $6,192 | OpenAI `gpt-5.6-terra` | $12 | 516M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $6,192 | Anthropic `Claude Sonnet 5` | $10 | 619M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $6,192 | Anthropic `Claude Sonnet 5` | $10 | 619M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $6,192 | Anthropic `Claude Sonnet 5` | $15 | 413M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $6,192 | Anthropic `Claude Sonnet 5` | $15 | 413M | 755M | yes | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $6,192 | Google Gemini `Gemini 3.6 Flash` | $7.5 | 826M | 755M | no | yes |
| Llama-3.3-70B-Instruct-FP8 | 1x MI355X | $6,192 | DeepSeek `deepseek-v4-flash` | $0.28 | 22,114M | 755M | no | no |

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
