# Prompt docs workflow run-checks failure

- Date: 2025-08-16
- Author: OpenAI Assistant
- Status: Resolved

## What went wrong
Update Prompt Docs Summary workflow failed on main.

## Root cause
Pre-commit ran project checks without Node, causing the job to exit.

## Impact
Scheduled prompt documentation summary was not refreshed.

## Actions to take
- Skip run-checks in the workflow to avoid unnecessary project tests.
- Monitor future runs for recurrence.
