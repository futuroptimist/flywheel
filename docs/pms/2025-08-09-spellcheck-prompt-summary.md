# Spellcheck Prompt Summary Malformed

- **Date**: 2025-08-09
- **Author**: Codex
- **Status**: resolved

## What went wrong
The spellcheck job flagged `htmlcontent` and physics terms, causing CI to fail.

## Root cause
`docs/prompts/summary.md` generated a malformed Markdown table, and `docs/flywheel-physics.md` used notation not in the spellcheck dictionary.

## Impact
CI runs failed on the spelling step, blocking merges.

## Actions to take
- Exclude the generated prompt docs summary from spellcheck.
- Whitelist common physics notation like `precess` and `circ`.
- Regenerate `docs/prompts/summary.md` with a valid Markdown table so spellcheck can cover it.
