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
`01-lint-format` workflow failed because `docs/prompt-docs-todos.md` contained trailing whitespace and `webapp/static/models/examples/spool_core_sleeve_example.obj` lacked a final newline.

## Root cause
Formatting drift in rarely-edited static files bypassed local checks and triggered pre-commit's `trailing-whitespace` and `end-of-file-fixer` hooks.

## Impact
The lint job blocked CI for all contributors until the files were corrected.

## Actions to take
- [x] Trim trailing whitespace and add missing newline.
- [x] Add regression test to guard against format regressions.
