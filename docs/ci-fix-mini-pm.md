# CI Mini Postmortem

## What went wrong
Pre-commit's `run project checks` hook executed Playwright end-to-end tests, leading to long runtimes and occasional timeouts during CI runs.

## Root cause
`scripts/checks.sh` only skipped Playwright when `SKIP_E2E` was set. Pre-commit runs did not set this flag, so the hook downloaded browsers and ran e2e tests.

## Impact
Developers and CI pipelines were slowed or blocked when the hook attempted to download and run Playwright assets.

## Actions to take
- [x] Skip Playwright steps when the `PRE_COMMIT` flag is present.
- [ ] Monitor pre-commit runtime and evaluate re-enabling e2e tests if overhead drops.
