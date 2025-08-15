# Prompt summary spellcheck failure

date: 2025-08-15
author: codex-bot
status: resolved

## What went wrong
The docs workflow's spellcheck job flagged the auto-generated `prompt-docs-summary.md` file.

## Root cause
The summary file lacked a `<!-- spellchecker: disable -->` marker, so the spell checker parsed its generated content and reported errors.

## Impact
Docs pull requests could not merge until the spellcheck failure was addressed.

## Actions to take
- Keep `prompt-docs-summary.md` excluded from spellcheck with a disable marker.
- Test to ensure the marker is present.
