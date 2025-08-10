# Spellcheck Untriaged Header

- **Date**: 2025-08-10
- **Author**: Codex
- **Status**: resolved

## What went wrong
The spellcheck job flagged the word "Untriaged" in the generated prompt docs summary, failing the workflow.

## Root cause
`docs/prompt-docs-summary.md` includes an "Untriaged" heading not present in the allow list.

## Impact
Spellcheck CI step failed, blocking merges.

## Actions to take
- Add "Untriaged" to the spellcheck dictionary.
- Regenerate the summary without custom headings to allow spellcheck coverage.
