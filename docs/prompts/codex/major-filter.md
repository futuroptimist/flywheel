---
title: 'Prompt Docs Major Filter'
slug: 'prompts-major-filter'
---

# Prompt Docs Major Filter
Type: one-off

This prompt guides an assistant to prune `prompt-docs-summary.md` so it only lists
major prompts that are ready for one-click use or describe pending unimplemented
feature requests.

```text
SYSTEM:
You are an automated contributor for the Flywheel repository.

PURPOSE:
Trim `docs/prompt-docs-summary.md` to include only high-value prompts.

CONTEXT:
- Keep entries with LLM-ready code blocks.
- Retain items that are evergreen one-click prompts or pending feature requests.
- Remove rows that do not meet these criteria.

REQUEST:
1. Review every row in `docs/prompt-docs-summary.md`.
2. Delete rows lacking a prompt code block or actionable feature request.
3. Run `python scripts/update_prompt_docs_summary.py` to regenerate the table.
4. Run `pre-commit run --all-files`, `pytest -q`, `npm run test:ci`,
   `python -m flywheel.fit`, and `bash scripts/checks.sh`.

OUTPUT:
A pull request with the cleaned summary and all checks green.
```

## Specification

An entry in `prompt-docs-summary.md` is *major* when it:

- Contains a code block intended for direct use as an LLM prompt.
- Represents either an evergreen one-click prompt or an unimplemented feature
  request.

Entries failing any condition must be removed from the summary.

## Example Usage

If a summary row points to a doc without a prompt block, delete that row, then
regenerate the table:

```bash
python scripts/update_prompt_docs_summary.py
```

The resulting file keeps only the remaining major prompts.

## API Reference

### `scripts/update_prompt_docs_summary.py`

Scans repositories for prompt docs and rebuilds `prompt-docs-summary.md`.

| Option            | Description                                             |
|-------------------|---------------------------------------------------------|
| `--repos-from`    | Optional extra repo list. Default: `dict/prompt-doc-repos.txt`; repeat to append. |
| `--out`           | Output file path (default: `docs/prompt-docs-summary.md`). |

The generated table contains the columns `Path`, `Prompt`, `Type`, and
`One-click?` for each discovered prompt document.
