# Prompt Docs Cleanup Plan

This document provides step-by-step instructions for a future LLM to refine
[prompt-docs-summary.md](prompt-docs-summary.md) so it only lists major prompts
that are either ready for one-click use or describe pending unimplemented feature
requests.

## Goals
- Keep the summary focused on high-value prompts.
- Remove entries that lack LLM-ready code blocks or that do not correspond to
  actionable feature requests.
- Maintain links to evergreen one-click prompts.

## Review Procedure
1. Open `prompt-docs-summary.md` and inspect each linked section.
2. Follow the link and verify that:
   - The section contains a code block intended as an LLM prompt.
   - The prompt is either evergreen one-click or an unimplemented feature request.
3. If either condition fails, remove the row from the summary.
4. When in doubt, err on the side of trimming the entry and note it for review.

## Regeneration
After editing, run:

```bash
python scripts/update_prompt_docs_summary.py
```

This regenerates the table to include only approved prompts. Repeat the review
process if new entries appear.

## Incremental Improvements
Apply these steps in small commits, gradually converging on a concise summary.
Future agents should continue pruning as new prompt docs are added.
