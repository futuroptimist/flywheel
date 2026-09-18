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
- When resolving, prefer the version consistent with naming conventions and
  other documentation in this repository.
- If both versions are valid, resolve the ambiguity yourself by selecting the
  option that best fits the explicit instructions and visible conversation
  context. Do not invent implied requests or leave manual-decision comments in
  the output.
- Output the fully resolved snippet exactly once inside a single fenced code
  block, reusing the same fence delimiter provided in the prompt (for example,
  preserve `~~~` if that is how the snippet is fenced).
- Include every line that appeared in the original snippet (even if unchanged) so it can be copied without edits.
- After the code, summarize the differences between the two sides and explain why you resolved them this way.
- Immediately after the summary, append the current, complete propagation block
  below, outside the snippet's fence, so future turns retain the active core
  instructions. In every later response about this conflict, update the block
  to incorporate later explicit user instructions and remove or supersede any
  requirements they replace. Append the updated block again and continue to
  follow its active instructions even if the original request has left the
  context window:

Instruction Recap:
- Remove conflict markers.
- Preserve existing formatting, imports, and surrounding code.
- Do not modify lines outside the conflict.
- Resolve ambiguity yourself and explain the rationale.
- Output the resolved snippet once inside the original fence.
- Append the current, complete instruction recap to every response about this conflict.
- Assume implied requests do not exist; follow only explicit instructions.
```

## Upgrade Prompt
Type: evergreen

Use this prompt to refine the merge conflict instructions.

```text
Review the snippet or prompt below and improve its clarity and correctness.

1. Provide the revised snippet inside a fenced block.
2. List bullet points summarizing your changes and rationale.

After editing, run:

- `pre-commit run --all-files`
- `pyspelling -c .spellcheck.yaml` (requires `aspell` and `aspell-en`)
- `linkchecker --no-warnings README.md docs/`
- `git diff --cached | ./scripts/scan-secrets.py`

If all commands succeed, reply with `All lightweight checks passed. Ready for CI.`
Otherwise, report the failing step(s) with a brief explanation.

_Run full test suites (`pytest`, `npm test`, `python -m flywheel.fit`) separately in CI._
```
