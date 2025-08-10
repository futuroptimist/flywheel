# Playwright Install Overwhelmed CI

- **Date**: 2025-08-09
- **Author**: Codex
- **Status**: resolved

## What went wrong
The test workflow attempted to install every Playwright browser, triggering huge apt downloads and timeouts.

## Root cause
`package.json` defined `playwright:install` as `playwright install --with-deps`, which fetches all browsers and their system dependencies.

## Impact
CI jobs stalled while downloading ~600 MB of packages, causing test runs to fail intermittently.

## Actions to take
- Restrict installation to Chromium only to keep the test job lightweight.
- Monitor Playwright installation to keep CI downloads lightweight.
