# Lane progress

## 2026-07-31 initial checkpoint

- Confirmed worktree contains only `README.md` plus Git metadata; no repo-local `AGENTS.md` or prior deliverables.
- Created `evidence/` for unmodified raw HTTP response bodies.
- No Git commands or test runners will be used.
- Next: capture current discovery listings, then official model cards and registry/provider proof.

## 2026-07-31 evidence checkpoint 2

- Saved live discovery responses from Hugging Face and OpenRouter, including `evidence/openrouter_models_api.json`.
- Saved official Hugging Face README/config/tokenizer responses for 19 candidate models spanning DeepSeek, Qwen, Llama, Mistral, GLM, Kimi, MiniMax, gpt-oss, Gemma, and Nemotron.
- Saved Docker Hub tag response `evidence/dockerhub_vllm_tags_page1.json`; literal `"name":"v0.26.0"` is present.
- Saved official Runpod H100 and L40S listing pages and official vLLM benchmark CLI documentation.
- Meta README cards returned HTTP 200; gated config/tokenizer files returned HTTP 401 and will not be used for facts.
- GLM-5.2 and MiniMax M2.5/M2.7 do not state total or active parameter counts in the captured official cards/repos; these will remain null with explicit notes.
- Next: finalize field-level literals, build the exact five-model stack, write outputs, and mechanically grep every evidence literal.

## 2026-07-31 final checkpoint

- Wrote `models.json` with 19 current hosted/open-weight model records.
- Wrote `stack.json` with exactly 5 runnable vLLM stack records.
- Wrote `findings.json` with 148 flattened evidence rows and `FINDINGS.md` with required uncertainty sections.
- Wrote `evidence/http-status.json` with 102 captured URL/status records.
- Final validation result: `VALIDATION_OK`.
- Mechanically checked all 148 `evidence_literal` values against their referenced raw files; all were found.
- Verified Docker image tag literals for `v0.26.0` and `v0.18.1` in exact Docker Hub tag responses.
- Remaining uncertainties are preserved in `FINDINGS.md`; no missing model parameters, release dates, gated tokenizer fields, or unexecuted GPU runtime checks were guessed.
- No Git commands, commits, pushes, or test runners were used.
