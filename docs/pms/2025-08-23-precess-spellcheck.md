# Precess term not whitelisted

- **Date**: 2025-08-23
- **Author**: Codex
- **Status**: resolved

## What went wrong
The docs spellcheck workflow failed on the term `precess`.

## Root cause
`precess` and `circ` were missing from the `.typos.toml` allow list,
so the spellcheck job flagged them as misspellings.

## Impact
Docs changes could not merge due to failing spellcheck job.

## Actions to take
- Add `precess` and `circ` to the `.typos.toml` `extend-words` list.
- Keep physics terminology whitelisted to avoid future failures.
