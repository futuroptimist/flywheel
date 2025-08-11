# Missing Template Lockfile

- **Date**: 2025-08-10
- **Author**: Codex
- **Status**: resolved

## What went wrong
`npm ci` failed for `templates/javascript` because `package-lock.json` was missing.

## Root cause
The JavaScript template lacked a committed lock file required by `npm ci`.

## Impact
Template checks in CI failed, blocking the pipeline.

## Actions to take
- Commit `package-lock.json` to `templates/javascript`.
- Test templates for required lock files.
- Alert on missing lock files in template directories.
