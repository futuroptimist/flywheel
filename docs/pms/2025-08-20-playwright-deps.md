# Playwright deps missing

- Date: 2025-08-20
- Author: codex
- Status: fixed

## What went wrong
Playwright tests failed to launch Chromium during CI runs.

## Root cause
Required system libraries were not installed before executing Playwright.

## Impact
End-to-end test suite exited with errors, blocking merges.

## Actions to take
- Ensure `npm run playwright:install` installs system dependencies in CI.
- Monitor future runs for missing library errors.
