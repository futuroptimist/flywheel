# prompts-docs-summary-cleanup

Future automation should harden `docs/prompt-docs-summary.md` so it only lists high-signal prompts.

## Goals
- Parse candidate markdown files and keep only sections with fenced code blocks that look like LLM prompts (e.g. contain `SYSTEM:` or `USER:`).
- Include only prompts marked as evergreen 1-click or one-off feature requests.
- Drop links to sections lacking code blocks or containing non-prompt code.

## Suggested steps
1. Extend `scripts/update_prompt_docs_summary.py` with filtering logic described above.
2. Add tests covering positive and negative examples.
3. Regenerate `docs/prompt-docs-summary.md` and verify links resolve to prompt code blocks.
4. Iterate in small one-click PRs until the summary stays focused.
