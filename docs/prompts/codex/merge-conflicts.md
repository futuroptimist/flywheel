---
title: 'Codex Merge Conflicts Prompt'
slug: 'codex-merge-conflicts'
conversational: true
---

# Codex Merge Conflicts Prompt
Type: evergreen

Use this prompt to resolve Git merge conflicts without altering unrelated code.

```text
Resolve the merge conflict in the code snippet below.

- Remove the conflict markers.
- Preserve existing formatting, imports, and surrounding code.
- Do not modify lines outside the conflict.
- When resolving, prefer the version consistent with naming conventions and other docs in this repo.
- If both versions are valid and a manual choice is required, include both in the merged code as commented alternatives marked with `// MANUAL DECISION REQUIRED`.
- After the code, summarize the differences between the two sides and explain why you resolved them this way.

```

## Upgrade Prompt
Type: evergreen

Use this prompt to refine the merge conflict instructions.

```text
Review the following code snippet or prompt, refine its clarity and accuracy, then output:

1. The improved version of the snippet or prompt (in a fenced block).
2. A bullet-point summary of your changes and reasoning.

After updating, run these lightweight checks:

- `pre-commit run --all-files`
- `pyspelling -c .spellcheck.yaml` (requires `aspell` and `aspell-en`)
- `linkchecker --no-warnings README.md docs/`
- `git diff --cached | ./scripts/scan-secrets.py`

If everything passes, output:
`“All lightweight checks passed. Ready for CI.”`
Otherwise, list the failing steps with concise explanations.

_*Note: Full test suites (`pytest`, `npm test`, `python -m flywheel.fit`) should be run separately in CI, not here.*_
```
