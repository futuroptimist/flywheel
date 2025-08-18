---
title: 'Codex Spellcheck Prompt'
slug: 'codex-spellcheck'
---

# Codex Spellcheck Prompt
Type: evergreen

Use this prompt to find and fix spelling mistakes in Markdown docs before opening a pull request.

```text
SYSTEM:
You are an automated contributor for the Flywheel repository.

PURPOSE:
Keep Markdown documentation free of spelling errors.

CONTEXT:
- Run `pre-commit run codespell --files $(git ls-files '*.md')` to spell-check
  Markdown documentation.
- Add unknown but legitimate words to
  [`dict/allow.txt`](../../../dict/allow.txt).
- Follow [`AGENTS.md`](../../../AGENTS.md) and [`README.md`](../../../README.md).
  Ensure these commands succeed:

  ```bash
  pre-commit run --all-files
  pytest -q
  npm run test:ci
  python -m flywheel.fit
  bash scripts/checks.sh
  ```
- Run `git diff --cached | ./scripts/scan-secrets.py` before committing.
- If browser dependencies are missing, run `npx playwright install chromium` or
  prefix tests with `SKIP_E2E=1`.

REQUEST:
1. Run the spellcheck command and inspect the results.
2. Correct misspellings or update `dict/allow.txt` as needed.
3. Re-run the spellcheck until it reports no errors.
4. Run all checks listed above.
5. Commit the changes with a concise message and open a pull request.

OUTPUT:
A pull request summarizing the fixes and showing passing check results.
```

Copy this block whenever you want Codex to clean up spelling across the docs.

## Upgrade Prompt
Type: evergreen

Use this prompt to refine the spellcheck instructions.

```text
SYSTEM:
You are an automated contributor for the Flywheel repository.

PURPOSE:
Keep this spellcheck prompt accurate as tooling evolves.

CONTEXT:
- Follow `AGENTS.md` and `README.md`.
- Ensure `pre-commit run --all-files`, `pytest -q`, `npm run test:ci`,
  `python -m flywheel.fit`, and `bash scripts/checks.sh` pass.
- Regenerate `docs/prompt-docs-summary.md` with
  `python scripts/update_prompt_docs_summary.py --repos-from \
  dict/prompt-doc-repos.txt --out docs/prompt-docs-summary.md`.

REQUEST:
1. Review this file for outdated commands or paths.
2. Update content and regenerate the summary.
3. Run the checks above.

OUTPUT:
A pull request updating this spellcheck prompt with all checks green.
```
