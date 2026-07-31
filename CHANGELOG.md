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

- 874 per-token price rows after deduplication: 581 closed-vendor across 13
  vendors, 263 open models across 11 hosted providers, 30 dedicated GPU-hour
  rows.
- 378 GPU rental rows across 16 providers, on-demand, spot and reserved kept as
  separate rows.
- 395 cited throughput datapoints across 7 accelerators (B200, B300, H100,
  H200, MI300X, MI325X, MI355X), yielding 338 costed configurations.
- 25 billing-mechanics rows on caching, batch tiers and reasoning tokens.
- 34 long-context threshold rows across 6 vendors.
- 22 provider rows on rate limits, minimum spend, retention and training policy.
- 20 models with params and licenses, active_params stated on 17.
- 10 tokenizer measurements, 5 recorded gaps.

Every row passed a mechanical evidence gate: 1,993 checks, 0 failures. The
number must appear literally inside a raw HTTP capture saved at collection
time, the value must appear inside that quote, and the value must sit near its
model name in the page.

Notable findings recorded at baseline, each of which is the kind of thing that
silently corrupts a cost comparison:

- **OpenAI publishes four service tiers on one page** (standard, batch, flex,
  fast) plus a separate long-context tier for newer models. Reading the wrong
  table is a 2x to 4x error. These are separate rows here and never blended.
  The tier multipliers are NOT uniform, which is worth stating because it is
  tempting to assume they are: across OpenAI models, batch output is 0.5x
  standard on 41 models but 0.562x, 0.833x and 1.0x on three others, and fast
  output ranges from 1.667x to 2.5x, hitting exactly 2.0x on only 10. Do not
  derive one tier's price from another.
- **Multi-tier pricing is not just an OpenAI habit.** Google Gemini publishes a
  Priority tier at 1.8x standard, Anthropic publishes a Fast mode tier at 2.0x
  standard on some models, and Fireworks publishes Standard and Priority as two
  adjacent columns of the same table, where the naive read takes the wrong
  column and overstates price by 50%. Each is a separate row here.
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
- **AMD MI355X rates are published, but not by the mainstream GPU clouds.**
  None of the eight providers surveyed first listed one. Vultr does, at
  $2.59/GPU/hr on demand, under half the cheapest B200 rate found, against
  higher measured throughput on DeepSeek-R1. Finding it required a second,
  targeted search.
- **44 GPU rental rows are marked `UNCLEAR`** on whether the listed price is
  per GPU or per node. That distinction is an 8x error and was not guessed.
- **Two of the most widely served open models have no reproducible serving
  benchmark.** Kimi K3 and GLM 5.2 are priced by eight or more hosts each, and
  neither has a public throughput datapoint stating hardware, engine version,
  precision, concurrency and sequence lengths together. They are therefore
  absent from the head-to-head table.

Errors found in our own work by the audit and fixed before publication, listed
because the protocol is the product:

1. **11 Fireworks rows carried Priority-tier prices labelled standard**, a 50%
   overstatement. Fireworks lists Standard and Priority as adjacent columns of
   one table; the collection lane got it right and the merge script overwrote
   it with a hardcoded "standard".
2. **A 4x understatement on every multi-GPU box.** SemiAnalysis InferenceX
   reports `output_tput_per_gpu`. One lane labelled those rows `total_output`
   while its own quoted literal named the per-GPU field. Introduced twice,
   caught twice; the quoted source field name now overrides the label.
3. **A 13B model priced against a 70B model's API.** Matching "Llama-3.3-70B"
   on its first token also matched a `llama_13b` row, which briefly reversed
   the repo's headline conclusion. Matching is now on a full canonical key.
4. **A claim of uniform tier multipliers** that the data does not support.
5. **Two Baseten rows** carrying a Fast variant's price under the base model
   name, dropped rather than corrected, because a corrected value would have
   come from a different fetch than the row's own quote.
6. **54 cross-lane duplicate rows.** Two collection lanes covered the same
   providers and wrote the same model under different names, so
   `moonshotai/Kimi-K3` and `Kimi K3` from one provider at one price became two
   rows. Duplicates inflate counts and double-count in the price-spread
   analysis. Rows are now keyed on provider, canonical model name, tier and
   price. Tier is kept in that key on purpose: OpenAI prices batch and flex
   identically for several models, and collapsing those would delete a real
   distinction rather than a duplicate.

The 2026-07-31 snapshot was cut, then recut the same day after the duplicate
fix, before any external citation could exist. Snapshots are immutable from
publication onward; this one is the published state.

## Next round

Planned for 2026-08-31. Expect movement in: hosted open-model per-token prices,
which move fastest; GPU on-demand rates; and the open model lineup, which turns
over roughly monthly.
