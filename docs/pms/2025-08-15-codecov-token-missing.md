# Codecov token missing in CI

- **Date**: 2025-08-15
- **Author**: Codex
- **Status**: resolved

## What went wrong
Codecov upload steps failed when the required CODECOV_TOKEN secret was absent on forked pull requests, causing the test workflow to error.

## Root cause
The test workflow always invoked the Codecov action with a token, which is unavailable to external contributors.

## Impact
Fork-based pull requests could not complete the test job, blocking merges.

## Actions to take
- Guard Codecov steps on token presence.
- Allow coverage uploads to fail without breaking CI.
