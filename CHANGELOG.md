# Changelog

Every price change with the date it was observed. Dates are when the page was
read, not when the vendor made the change. We cannot know the latter.

Format: one section per verification round. New rounds are added at the top and
old entries are never edited. The corresponding immutable snapshot is in
`data/snapshots/`.

## 2026-07-31 -- first verification round

Initial publication. Everything is new, so this is a baseline rather than a
diff. Future rounds will list only what moved.

Collected in this round:

- 586 per-token price rows across 14 providers, split into closed vendor APIs
  (281) and open models on hosted APIs (305, of which 48 are dedicated GPU-hour
  rows rather than per-token).
- 355 GPU rental rows across 8 providers, covering on-demand, spot, and
  reserved tiers.
- 25 billing-mechanics rows covering prompt caching, batch tiers, and reasoning
  tokens across 10 providers.
- 9 cited throughput datapoints, 6 complete and 3 incomplete.
- 10 tokenizer measurements, 5 recorded gaps.

Notable findings recorded at baseline, each of which is the kind of thing that
silently corrupts a cost comparison:

- **OpenAI publishes four service tiers on one page** (standard, batch, flex,
  fast) plus a separate long-context tier for newer models. Batch is 50% of
  standard, fast is 200%, and the long-context tier is 200% of standard input
  and 150% of standard output. Reading the wrong table is a 2x to 4x error.
  These are separate rows here and are never blended.
- **OpenAI now prices cache writes** as a fourth column at 1.25x the input
  rate on models that carry it. Most published comparisons omit this entirely.
- **SemiAnalysis InferenceX reports `output_tput_per_gpu`**, not whole-system
  throughput. Feeding it straight into a deployment cost formula understates
  cost by the GPU count. Corrected here by multiplying by GPU count, recorded
  per row in `data/self-host-inputs.json`.
- **Mistral's HuggingFace tokenizer loads with a known-bad regex** under
  transformers 5.2.0, which warns that it "will lead to incorrect tokenization"
  and returns 164 tokens for our English sample on some repos against 134 from
  Mistral's own `mistral-common` library. The first-party library is treated as
  authoritative here.
- **No surveyed provider publishes an on-demand per-GPU AMD MI355X rate.**
  Good throughput data for MI355X exists and is recorded, but it produces no
  cost row because there is no rate to multiply it by.
- **36 GPU rental rows are marked `UNCLEAR`** on whether the listed price is
  per GPU or per node. That distinction is an 8x error and was not guessed.

## Next round

Planned for 2026-08-31. Expect movement in: hosted open-model per-token prices,
which move fastest; GPU on-demand rates; and the open model lineup, which turns
over roughly monthly.
