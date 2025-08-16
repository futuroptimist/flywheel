# Linkchecker Missing in CI

- Date: 2025-08-16
- Author: OpenAI Codex
- Status: fixed

## What went wrong
The CI `checks.sh` script attempted to run `linkchecker` even when the tool was not installed.

## Root cause
The script unconditionally invoked `linkchecker`, producing `command not found` errors during workflow runs.

## Impact
CI logs were noisy and workflows failed on environments lacking `linkchecker`.

## Actions to take
- Guard linkchecker invocation and skip when the binary is absent.
- Install `linkchecker` locally if link checks are desired.
