# Docs spellcheck action failure

- Date: 2025-08-22
- Author: Codex
- Status: fixed

## What went wrong
The docs workflow's spellcheck job failed on `rojopolis/spellcheck-github-actions`, causing docs CI to fail.

## Root cause
The action relied on `aspell` and intermittently exited non-zero even with dictionaries installed.

## Impact
Docs previews and link checks were blocked until the spellcheck job completed.

## Actions to take
- Use the more reliable `crate-ci/typos` action for spellchecking.
- Monitor future docs workflow runs for stability.
