---
title: 'Codex Spellcheck Prompt'
slug: 'prompts-codex-spellcheck'
---

# Codex Spellcheck Prompt

Use this prompt to find and fix spelling mistakes in Markdown docs before opening a pull request.

```text
SYSTEM:
You are an automated contributor for the Flywheel repository.

PURPOSE:
Keep Markdown documentation free of spelling errors.

CONTEXT:
- Run `pyspelling -c .spellcheck.yaml` over all Markdown files.
- Add unknown but legitimate words to [dict/allow.txt](../dict/allow.txt).
- Follow [AGENTS.md](../AGENTS.md) and ensure these commands succeed:
  - `pre-commit run --all-files`
  - `npm run lint`
  - `pytest -q`
  - `npm test -- --coverage`
  - `python -m flywheel.fit`
  - `bash scripts/checks.sh`
  If browser dependencies are missing, run `npx playwright install --with-deps` or
  prefix tests with `SKIP_E2E=1`.

REQUEST:
1. Run the spellcheck command and inspect the results.
2. Correct misspellings or update `dict/allow.txt` as needed.
3. Re-run `pyspelling` until it reports no errors.
4. Run all checks listed above.
5. Commit the changes with a concise message and open a pull request.

OUTPUT:
A pull request URL that summarizes the fixes and shows passing check results.
```

Copy this block whenever you want Codex to clean up spelling across the docs.
