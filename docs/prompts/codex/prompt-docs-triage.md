---
title: 'Codex Prompt Docs Triage Prompt'
slug: 'codex-prompt-docs-triage'
---

# Codex Prompt Docs Triage Prompt
Type: evergreen

Use this prompt to consolidate outstanding prompt documentation tasks from `docs/prompt-docs-todos.md`
into `docs/prompt-docs-summary.md`.

**Human set-up steps:**

1. Ensure `docs/prompt-docs-todos.md` lists TODO entries in the four-column table format.
2. Run `python scripts/update_prompt_docs_summary.py --repos-from docs/repo_list.txt --out docs/prompt-docs-summary.md`.
   The script automatically sorts the TODO table by type and repository, so manual edits
   can be added in any order.
3. Review the updated summary and commit both files.

```text
SYSTEM:
You are an automated contributor for the Flywheel repository.

PURPOSE:
Incorporate rows from `docs/prompt-docs-todos.md` into `docs/prompt-docs-summary.md` and keep
the TODO table sorted by type and repository.

CONTEXT:
- Follow `AGENTS.md` and repository conventions.
- Categorize each entry as `evergreen`, `one-off`, or `unknown`.
- After updating the TODO file, regenerate the summary with the script above.
- Run `pre-commit run --all-files`, `pytest -q`, `npm run test:ci`,
  `python -m flywheel.fit`, and `bash scripts/checks.sh` before committing.

REQUEST:
1. Update `docs/prompt-docs-todos.md` and regenerate the summary.
2. Commit changes on branch `codex/prompt-docs`.
3. Return the pull request URL.

OUTPUT:
A pull request link with the updated prompt docs tables.
```
