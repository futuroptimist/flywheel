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

---

## What went wrong
`npm ci` failed for `templates/javascript` because `package-lock.json` was missing.

## Root cause
The JavaScript template lacked a committed lock file required by `npm ci`.

## Impact
Template checks in CI failed, blocking the pipeline.

## Actions to take
- [x] Add `package-lock.json` to `templates/javascript`.
- [x] Add test to ensure all templates include a lock file.

---

## What went wrong
`Docs Preview & Link Check` failed when `linkchecker` was missing, producing a
`command not found` error.

## Root cause
`scripts/checks.sh` invoked `linkchecker` unconditionally, so environments
without the tool surfaced errors during docs checks.

## Impact
Docs jobs emitted noisy failures and could block CI in environments lacking
`linkchecker`.

## Actions to take
- [x] Skip `linkchecker` when the binary is absent.
- [ ] Document how to install `linkchecker` locally.
