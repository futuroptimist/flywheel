# Playwright Apt Failure

- **Date**: 2025-08-16
- **Author**: Codex
- **Status**: resolved

## What went wrong
CI tests attempted to install system dependencies for Playwright using the `--with-deps` flag, leading to apt errors.

## Root cause
The Playwright install script fetched OS packages via apt, which occasionally failed in the GitHub Actions environment.

## Impact
JavaScript test jobs failed before executing tests, blocking merges.

## Actions to take
- Install only the Chromium browser without system dependencies.
- Update checks and tests to prevent regression.
