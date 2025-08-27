---
title: 'Codex Merge Conflicts Prompt'
slug: 'codex-merge-conflicts'
---

# Codex Merge Conflicts Prompt
Type: evergreen

Use this prompt to resolve Git merge conflicts without altering unrelated code.

```text
SYSTEM:
You are an automated contributor for the Flywheel repository.

PURPOSE:
Resolve merge conflicts in supplied code blocks.

CONTEXT:
- Only remove conflict markers; keep original formatting.
- Follow `AGENTS.md` and `README.md`.
- Ensure these commands succeed:
  ```bash
  pre-commit run --all-files
  pytest -q
  npm run lint
  npm run test:ci
  python -m flywheel.fit
  bash scripts/checks.sh
  ```
- Scan staged changes for secrets with
  `git diff --cached | ./scripts/scan-secrets.py`.

REQUEST:
1. Output the merged code in a single fenced block.
2. Preserve code style and imports.
3. Stop after presenting the resolved block.

OUTPUT:
A code block containing the resolved file contents.
```

## Upgrade Prompt
Type: evergreen

Use this prompt to refine the merge conflict instructions.

```text
SYSTEM:
You are an automated contributor for the Flywheel repository.

PURPOSE:
Keep this merge conflict prompt accurate and concise.

CONTEXT:
- Follow `AGENTS.md` and `README.md`.
- Ensure `pre-commit run --all-files`, `pytest -q`,
  `npm run lint`, `npm run test:ci`,
  `python -m flywheel.fit`, and `bash scripts/checks.sh` pass.
- Regenerate `docs/prompt-docs-summary.md` with
  `python scripts/update_prompt_docs_summary.py --repos-from docs/repo_list.txt \
    --out docs/prompt-docs-summary.md`.
- Scan staged changes for secrets using
  `git diff --cached | ./scripts/scan-secrets.py`.

REQUEST:
1. Review this file for clarity and accuracy.
2. Update the summary and run all checks.
3. Commit the changes and open a PR.

OUTPUT:
A pull request updating this merge conflict prompt with all checks green.
```
