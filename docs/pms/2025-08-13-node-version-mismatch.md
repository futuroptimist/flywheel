# Node version mismatch in CI

- **Date**: 2025-08-13
- **Author**: Codex
- **Status**: resolved

## What went wrong
JavaScript tests ran on Node 18 in GitHub Actions, while the project now
targets Node 20 features. The mismatch caused the test job to fail.

## Root cause
Workflows pinned Node 18 and lacked a guard to ensure the required runtime
version.

## Impact
CI failed on the test job, blocking merges.

## Actions to take
- Upgrade workflow node versions to 20.
- Add a test asserting the Node.js major version.
- Document the Node 20 prerequisite in the README.
