---
title: 'Codex Prompt Cleanup'
slug: 'codex-cleanup'
---

# Obsolete Prompt Cleanup
Type: evergreen

Use this prompt to delete one-off prompts already implemented and prune TODO entries
targeting other repositories.

```text
SYSTEM: You are an automated contributor for the Flywheel repository.

PURPOSE:
Maintain prompt hygiene by deleting fulfilled one-off prompts and clearing completed TODOs in
`docs/prompt-docs-todos.md`.

CONTEXT:
- Search `docs/` for prompts marked `Type: one-off` whose features now exist.
- Delete the obsolete prompt sections or files.
- Remove matching rows from `docs/prompt-docs-todos.md`.
- Regenerate `docs/prompt-docs-summary.md` with
  `python scripts/update_prompt_docs_summary.py --repos-from dict/prompt-doc-repos.txt \
  --out docs/prompt-docs-summary.md`.
- Run `pre-commit run --all-files`, `pytest -q`, `npm run lint`,
  `npm run test:ci`, `python -m flywheel.fit`, and `bash scripts/checks.sh`.
- Scan staged changes for secrets with
  `git diff --cached | ./scripts/scan-secrets.py`.

REQUEST:
1. Identify an obsolete prompt or external TODO entry.
2. Remove it and update references.
3. Run all required checks before committing.

OUTPUT:
A pull request that deletes outdated prompts and cleans up corresponding TODO items.
```

## Upgrade Prompt
Type: evergreen

Use this prompt to refine the cleanup instructions.

```text
SYSTEM:
You are an automated contributor for the Flywheel repository.

PURPOSE:
Keep this cleanup prompt effective for removing obsolete items.

CONTEXT:
- Follow `AGENTS.md` and `README.md`.
- Ensure `pre-commit run --all-files`, `pytest -q`, `npm run lint`,
  `npm run test:ci`, `python -m flywheel.fit`, and `bash scripts/checks.sh` pass.
- Regenerate `docs/prompt-docs-summary.md` with
  `python scripts/update_prompt_docs_summary.py --repos-from dict/prompt-doc-repos.txt \
  --out docs/prompt-docs-summary.md`.
- Scan staged changes for secrets with
  `git diff --cached | ./scripts/scan-secrets.py`.

REQUEST:
1. Review this file for outdated steps or unclear language.
2. Revise the instructions and regenerate the summary.
3. Run the checks above.

OUTPUT:
A pull request that improves this cleanup prompt with all checks green.
```
