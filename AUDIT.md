# Adversarial live-source audit

Audit date: 2026-07-31. Raw responses are under `evidence/2026-07-31/`; no data or README file was edited.

## CONFIRMED CORRECT

123 of 126 sampled source rows had every sampled numeric field re-fetched and found literally in the saved official response. This confirms price values only; separate tier-label mismatches are below.

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

No sampled per-1K/per-1M conversion error was found. Cached-input checks used the cache-read/hit column; cache-write fields were checked separately where present. Sampled model names appeared on their official pages except for the Google rows that could not be fetched.

## MISMATCHES FOUND

### Fireworks service-tier labels

Repo says `standard`; the live table says the values are in its `Priority` column. The exact table excerpts are stored per row in `findings.json`. Affected rows:

Literal live quote: "In each <strong>Standard</strong> or <strong>Priority</strong> cell, prices are <strong>input / cached input / output</strong> (USD per 1M tokens), in that order."

- `providers.rows[327]` -- Kimi K3; repo tier `standard`; live tier `Priority`; source: https://docs.fireworks.ai/serverless/pricing
- `providers.rows[330]` -- Kimi K3 US; repo tier `standard`; live tier `Priority`; source: https://docs.fireworks.ai/serverless/pricing
- `providers.rows[332]` -- Kimi K2.7 Code; repo tier `standard`; live tier `Priority`; source: https://docs.fireworks.ai/serverless/pricing
- `providers.rows[335]` -- Kimi K2.6; repo tier `standard`; live tier `Priority`; source: https://docs.fireworks.ai/serverless/pricing
- `providers.rows[338]` -- DeepSeek V4 Pro; repo tier `standard`; live tier `Priority`; source: https://docs.fireworks.ai/serverless/pricing
- `providers.rows[340]` -- DeepSeek V4 Flash; repo tier `standard`; live tier `Priority`; source: https://docs.fireworks.ai/serverless/pricing
- `providers.rows[342]` -- GLM 5.2; repo tier `standard`; live tier `Priority`; source: https://docs.fireworks.ai/serverless/pricing
- `providers.rows[345]` -- GLM 5.1; repo tier `standard`; live tier `Priority`; source: https://docs.fireworks.ai/serverless/pricing
- `providers.rows[349]` -- MiniMax M3; repo tier `standard`; live tier `Priority`; source: https://docs.fireworks.ai/serverless/pricing
- `providers.rows[351]` -- MiniMax M2.7; repo tier `standard`; live tier `Priority`; source: https://docs.fireworks.ai/serverless/pricing
- `providers.rows[353]` -- OpenAI GPT OSS 120B; repo tier `standard`; live tier `Priority`; source: https://docs.fireworks.ai/serverless/pricing

### README uses a future Anthropic price as if it were current

- README line 64 prints Claude Sonnet 5 at `$3 / $0.3 / $3.75 / $15` without an effective-date qualifier. On 2026-07-31 the official page lists the introductory row through August 31, 2026 at `$2 / $0.20 / $2.50 / $4.00 / $10`, and a separate higher row starting September 1, 2026. The repo JSON contains both schedules; the README selected the future schedule. Source: https://platform.claude.com/docs/en/about-claude/pricing

Literal live quote: "Introductory pricing of $2/$10 per million input/output tokens is in effect through August 31, 2026, after which the standard pricing of $3/$15 per million input/output tokens will take effect."

### README one-cent double-rounding mismatch

- README line 304 reports `$17.79` for the RunPod Llama-3.3 70B ten-percent-utilization case. `data/self-host.json` contains `17.785`; recomputing from full inputs gives `17.78499085`, which rounds directly to `$17.78`. This is a README presentation mismatch, not a self-host JSON arithmetic error over the required tolerance.
- No other number in the README closed-API, hosted-API, or self-host price tables failed the JSON membership check.

### OpenAI tier relationship anomalies

The row prices match the live tables, but the following live-listed relationships violate the requested rule and have no row-level explanation:
Source for every row below: https://developers.openai.com/api/docs/pricing. Exact raw tier-context quotes are stored per row in `findings.json`.

- `providers.rows[108]` -- gpt-5.5 (<272K context length): official Fast table is not exactly double Standard.
- `providers.rows[114]` -- gpt-5-mini: official Fast table is not exactly double Standard.
- `providers.rows[115]` -- gpt-4.1: official Fast table is not exactly double Standard.
- `providers.rows[116]` -- gpt-4.1-mini: official Fast table is not exactly double Standard.
- `providers.rows[118]` -- gpt-4o: official Fast table is not exactly double Standard.
- `providers.rows[119]` -- gpt-4o-2024-05-13: official Fast table is not exactly double Standard.
- `providers.rows[120]` -- gpt-4o-mini: official Fast table is not exactly double Standard.
- `providers.rows[121]` -- o3: official Fast table is not exactly double Standard.
- `providers.rows[122]` -- o4-mini: official Fast table is not exactly double Standard.
- `providers.rows[74]` -- gpt-3.5-turbo-1106: official Batch table is not exactly half Standard.

## ROWS I COULD NOT RE-VERIFY

- `providers.rows[202]` -- Gemini 3.6 Flash. HTTP 302 led into a 50-redirect OAuth loop; static body contained no pricing data.
- `providers.rows[226]` -- Gemini 3.1 Pro Preview. HTTP 302 led into a 50-redirect OAuth loop; static body contained no pricing data.
- `providers.rows[245]` -- Gemini 2.5 Flash-Lite. HTTP 302 led into a 50-redirect OAuth loop; static body contained no pricing data.

## ARITHMETIC ERRORS

None. All twenty-four recomputations (six rows across four utilization levels) differ from the published JSON values by no more than 0.01.

## PLACES WHERE THE HONEST ANSWER FAVOURS THE API OVER SELF-HOSTING

Every self-host row loses to a comparable hosted API at every published utilization point. The twenty-four comparisons are:

- `DeepSeek-R1-0528-4xB200::RunPod::on_demand` at ten-percent utilization -- DeepInfra `deepseek-ai/DeepSeek-R1-0528` (`providers.rows[375]`) is cheaper.
- `DeepSeek-R1-0528-4xB200::RunPod::on_demand` at thirty-percent utilization -- DeepInfra `deepseek-ai/DeepSeek-R1-0528` (`providers.rows[375]`) is cheaper.
- `DeepSeek-R1-0528-4xB200::RunPod::on_demand` at sixty-percent utilization -- DeepInfra `deepseek-ai/DeepSeek-R1-0528` (`providers.rows[375]`) is cheaper.
- `DeepSeek-R1-0528-4xB200::RunPod::on_demand` at ninety-percent utilization -- DeepInfra `deepseek-ai/DeepSeek-R1-0528` (`providers.rows[375]`) is cheaper.
- `DeepSeek-R1-0528-4xB200::CoreWeave::on_demand` at ten-percent utilization -- DeepInfra `deepseek-ai/DeepSeek-R1-0528` (`providers.rows[375]`) is cheaper.
- `DeepSeek-R1-0528-4xB200::CoreWeave::on_demand` at thirty-percent utilization -- DeepInfra `deepseek-ai/DeepSeek-R1-0528` (`providers.rows[375]`) is cheaper.
- `DeepSeek-R1-0528-4xB200::CoreWeave::on_demand` at sixty-percent utilization -- DeepInfra `deepseek-ai/DeepSeek-R1-0528` (`providers.rows[375]`) is cheaper.
- `DeepSeek-R1-0528-4xB200::CoreWeave::on_demand` at ninety-percent utilization -- DeepInfra `deepseek-ai/DeepSeek-R1-0528` (`providers.rows[375]`) is cheaper.
- `MiniMax-M3-4xB300::RunPod::on_demand` at ten-percent utilization -- Fireworks Standard `MiniMax M3` (`providers.rows[348]`) is cheaper.
- `MiniMax-M3-4xB300::RunPod::on_demand` at thirty-percent utilization -- Fireworks Standard `MiniMax M3` (`providers.rows[348]`) is cheaper.
- `MiniMax-M3-4xB300::RunPod::on_demand` at sixty-percent utilization -- Fireworks Standard `MiniMax M3` (`providers.rows[348]`) is cheaper.
- `MiniMax-M3-4xB300::RunPod::on_demand` at ninety-percent utilization -- Fireworks Standard `MiniMax M3` (`providers.rows[348]`) is cheaper.
- `MiniMax-M3-4xB300::Nebius::on_demand` at ten-percent utilization -- Fireworks Standard `MiniMax M3` (`providers.rows[348]`) is cheaper.
- `MiniMax-M3-4xB300::Nebius::on_demand` at thirty-percent utilization -- Fireworks Standard `MiniMax M3` (`providers.rows[348]`) is cheaper.
- `MiniMax-M3-4xB300::Nebius::on_demand` at sixty-percent utilization -- Fireworks Standard `MiniMax M3` (`providers.rows[348]`) is cheaper.
- `MiniMax-M3-4xB300::Nebius::on_demand` at ninety-percent utilization -- Fireworks Standard `MiniMax M3` (`providers.rows[348]`) is cheaper.
- `Llama-3.3-70B-Instruct-FP8-(InferenceX-key:-llama70b)-2xH200::RunPod::on_demand` at ten-percent utilization -- DeepInfra `meta-llama/Llama-3.3-70B-Instruct-Turbo` (`providers.rows[392]`) is cheaper.
- `Llama-3.3-70B-Instruct-FP8-(InferenceX-key:-llama70b)-2xH200::RunPod::on_demand` at thirty-percent utilization -- DeepInfra `meta-llama/Llama-3.3-70B-Instruct-Turbo` (`providers.rows[392]`) is cheaper.
- `Llama-3.3-70B-Instruct-FP8-(InferenceX-key:-llama70b)-2xH200::RunPod::on_demand` at sixty-percent utilization -- DeepInfra `meta-llama/Llama-3.3-70B-Instruct-Turbo` (`providers.rows[392]`) is cheaper.
- `Llama-3.3-70B-Instruct-FP8-(InferenceX-key:-llama70b)-2xH200::RunPod::on_demand` at ninety-percent utilization -- DeepInfra `meta-llama/Llama-3.3-70B-Instruct-Turbo` (`providers.rows[392]`) is cheaper.
- `Llama-3.3-70B-Instruct-FP8-(InferenceX-key:-llama70b)-2xH200::CoreWeave::on_demand` at ten-percent utilization -- DeepInfra `meta-llama/Llama-3.3-70B-Instruct-Turbo` (`providers.rows[392]`) is cheaper.
- `Llama-3.3-70B-Instruct-FP8-(InferenceX-key:-llama70b)-2xH200::CoreWeave::on_demand` at thirty-percent utilization -- DeepInfra `meta-llama/Llama-3.3-70B-Instruct-Turbo` (`providers.rows[392]`) is cheaper.
- `Llama-3.3-70B-Instruct-FP8-(InferenceX-key:-llama70b)-2xH200::CoreWeave::on_demand` at sixty-percent utilization -- DeepInfra `meta-llama/Llama-3.3-70B-Instruct-Turbo` (`providers.rows[392]`) is cheaper.
- `Llama-3.3-70B-Instruct-FP8-(InferenceX-key:-llama70b)-2xH200::CoreWeave::on_demand` at ninety-percent utilization -- DeepInfra `meta-llama/Llama-3.3-70B-Instruct-Turbo` (`providers.rows[392]`) is cheaper.
