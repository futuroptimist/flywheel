---
title: 'Codex Merge Conflicts Prompt'
slug: 'codex-merge-conflicts'
conversational: true
---

# Codex Merge Conflicts Prompt
Type: evergreen

Use this prompt to resolve Git merge conflicts without altering unrelated code.

```text
Resolve the merge conflict in the code snippet below. Remove the conflict markers while
preserving existing formatting, imports, and surrounding code. Do not modify lines that are
not part of the conflict.

Return the merged file contents in a single fenced code block, followed by any notes that
help explain the resolution. If more snippets are provided later in this chat, handle them
using the same approach.
```

## Upgrade Prompt
Type: evergreen

Use this prompt to refine the merge conflict instructions.

```text
Review this code snippet for clarity and accuracy. After editing, regenerate
`docs/prompt-docs-summary.md` with `python scripts/update_prompt_docs_summary.py --repos-from
docs/repo_list.txt --out docs/prompt-docs-summary.md`. Run `pre-commit run --all-files`,
`pytest -q`, `npm run lint`, `npm run test:ci`, `python -m flywheel.fit`, and `bash
scripts/checks.sh`, then scan staged changes for secrets using `git diff --cached |
./scripts/scan-secrets.py`.

Share the updated code snippet and test results.
```
