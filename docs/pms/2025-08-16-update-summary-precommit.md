# Update summary pre-commit failure

- Date: 2025-08-16
- Author: Codex Bot
- Status: resolved

## What went wrong
The Update Repo Feature Summary workflow failed during its pre-commit step.

## Root cause
The workflow ran the `run-checks` pre-commit hook, triggering full project checks that require tools not present in the minimal workflow environment.

## Impact
The summary regeneration job failed, leaving `docs/repo-feature-summary.md` outdated.

## Actions to take
- Skip heavy hooks in lightweight workflows using `SKIP=run-checks`.
- Consider dedicated pre-commit configs for doc-only automation.
