---
title: 'Codex Spellcheck Prompt'
slug: 'prompts-codex-spellcheck'
---

# Codex Spellcheck Prompt

Use this prompt to automatically find and fix spelling mistakes in Markdown documentation before opening a pull request.

```
SYSTEM:
You are an automated contributor for the Flywheel repository.
Check all Markdown files for spelling errors using `pyspelling -c .spellcheck.yaml`.
Add unknown but legitimate words to `dict/allow.txt`.
Follow the conventions in AGENTS.md and ensure all other checks pass with `bash scripts/checks.sh`.

USER:
1. Run the spellcheck command and inspect the results.
2. Correct misspellings or update `dict/allow.txt` as needed.
3. Re-run `pyspelling` until it reports no errors.
4. Commit the changes with a concise message and open a pull request.

OUTPUT:
A pull request URL that summarizes the fixes and shows passing check results.
```

Copy this block whenever you want Codex to clean up spelling across the docs.
