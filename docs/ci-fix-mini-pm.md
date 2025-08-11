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
Pre-commit failed on trailing whitespace in `docs/prompt-docs-todos.md` and a missing end-of-file newline in `webapp/static/models/examples/spool_core_sleeve_example.obj`.

## Root cause
Both files were committed with formatting issues that violate repository pre-commit hooks.

## Impact
The pre-commit step in CI failed, blocking merges.

## Actions to take
- [x] Trim trailing whitespace in `docs/prompt-docs-todos.md`.
- [x] Add a newline at the end of `webapp/static/models/examples/spool_core_sleeve_example.obj`.
- [ ] Audit remaining docs and static assets for similar issues.
