# JavaScript Template Missing Lock File

- **Date**: 2025-08-10
- **Author**: Codex
- **Status**: resolved

## What went wrong
`npm ci` failed for `templates/javascript` because `package-lock.json` was missing.

## Root cause
The template lacked a committed lock file required by `npm ci`.

## Impact
Template checks in CI failed, blocking the pipeline.

## Actions to take
- Add `package-lock.json` to `templates/javascript`.
- Add a test to ensure all templates include a lock file.
