# CI Fix Mini Postmortem

## What went wrong
The CI fix prompt lacked guidance to create postmortems after failures.

## Root cause
No instruction directed contributors to document background, impact, and follow-up steps.

## Impact
Teams missed context from past failures, slowing diagnosis of future CI issues.

## Actions
Document future CI fixes with a mini postmortem and track follow-up items in `docs/ci-fix-action-items.md`.
