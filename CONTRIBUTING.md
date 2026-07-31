# Contributing

This repo is only worth citing if every number in it can be checked. So the bar
for a data change is higher than the bar for a typo fix. The checklists below
are the whole protocol.

Corrections are welcome and wanted. If a number here is wrong, open an issue
with the source and it gets fixed in the next refresh, or sooner.

## Price changes

A PR that adds or changes a price is accepted only with all four:

- [ ] **Source URL** pointing at the vendor's own pricing page or official docs.
      Not a blog, not an aggregator, not a screenshot of someone else's table.
- [ ] **Retrieval date** in ISO format (`YYYY-MM-DD`), the date you actually
      loaded the page.
- [ ] **Screenshot or archive link.** A `web.archive.org` snapshot is ideal
      because it is independently checkable. A screenshot attached to the PR is
      accepted. This exists because vendor pricing pages change without notice
      and reviewers need to see what you saw.
- [ ] **Both files updated.** The JSON under `data/` is the source of truth and
      the README table has to match it. A PR that changes one and not the other
      will be asked to fix the other.

If a price is quoted per 1K tokens on the source page, convert it to per 1M and
say so in the `notes` field. Keep the original printed string in your PR
description so the reviewer can check the conversion.

## Throughput numbers

Throughput is the easiest thing in this domain to get wrong, and a wrong
throughput number silently corrupts every derived cost. A PR that adds a
throughput number is accepted only with all five:

- [ ] **Hardware.** GPU model and count. State whether the number is for one
      GPU or the whole node.
- [ ] **Engine and version.** For example `vllm 0.11.0`, not `vllm`.
- [ ] **Exact command.** The full command line you ran, copy-pasteable.
- [ ] **Raw output.** The benchmark's own output, unedited. Not a summary of
      it, not a number retyped from it.
- [ ] **Sequence lengths and batch size or concurrency.** Input length, output
      length, and the concurrency level. A throughput number without these is
      not a measurement, it is a number.

Also state the quantization or precision, and whether the figure is total
output tokens per second across all concurrent requests or per user. Those two
differ by more than an order of magnitude and mixing them up is the most common
error in published comparisons.

Numbers cited from someone else's published benchmark are accepted under the
same five-field rule, as long as the cited source itself states all five. If it
does not, the number does not go in. Mark cited rows `measured: false` and put
the citation in `source_url`.

## What gets rejected

- Any number without a source.
- An estimate of what a closed provider pays to serve a model. There is no
  markup column here and there will not be one.
- A throughput number reconstructed from a chart with no axis labels.
- "I ran this a while ago and remember it being about X."
- Filling a blank cell with a value copied from a similar provider. Blank cells
  marked "not measured" are correct output.

## Data file rules

Every row in every file under `data/` carries `source_url`, `retrieved_on`,
`measured`, and `notes`. If you add a row, add all four. `measured: true` means
someone ran it or the cited source ran it and published full specs.
`measured: false` means derived, estimated, or cited without full specs, and
`notes` has to say which.

Never edit a file under `data/snapshots/`. Those are immutable dated records. A
new verification round means a new file.

## Running the tokenizer measurements

```
py -m pip install tiktoken transformers mistral-common
py scripts/measure_tokenizers.py
```

This rewrites `data/tokenizers.json` from the two fixed corpus files in
`data/tokenizer-corpus/`. Do not change those corpus files. Changing them
invalidates every published tokens-per-1000-characters number and makes old
snapshots incomparable. If you want a different test text, add a new one
alongside rather than editing the existing ones.

Tokenizers that fail to load are recorded with `measured: false` and the load
error. That is intended output. Gated repositories and vendors who publish no
downloadable tokenizer stay blank rather than getting a guess.
