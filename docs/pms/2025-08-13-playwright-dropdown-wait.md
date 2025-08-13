# Playwright dropdown wait

- **Date**: 2025-08-13
- **Author**: Codex
- **Status**: resolved

## What went wrong
Viewer model tests queried the dropdown before options loaded, causing Playwright to report interrupted tests in CI.

## Root cause
The tests called `page.$$eval` on `#model-select option` without waiting for the elements to exist.

## Impact
CI `test:ci` workflow failed intermittently, preventing merges.

## Actions to take
- Wait for dropdown options before evaluation.
- Monitor CI for further flakes.
