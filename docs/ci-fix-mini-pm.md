# CI Mini Postmortem

## What went wrong
Spellcheck failed on `docs/prompt-docs-summary.md` due to the word "Untriaged".

## Root cause
The term "Untriaged" was missing from the spellcheck allow list, causing a false positive.

## Impact
CI runs were blocked by the spellcheck job.

## Actions to take
- [x] Add "Untriaged" to the spellcheck dictionary.
- [ ] Regenerate `docs/prompt-docs-summary.md` with sanitized headings.
