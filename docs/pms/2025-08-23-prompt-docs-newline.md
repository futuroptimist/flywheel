# 2025-08-23: Prompt docs newline

- **Date:** 2025-08-23
- **Author:** codex-bot
- **Status:** fixed

## What went wrong
Docs workflow failed because `docs/prompt-docs-summary.md` lacked a trailing newline, causing the
`end-of-file-fixer` pre-commit hook to modify the file and exit non-zero.

## Root cause
The summary generator did not ensure a newline at end of file.

## Impact
`Docs Preview & Link Check` workflow failed on `main`.

## Actions to take
- enforce newline in generated files
- update generator to write newline explicitly
