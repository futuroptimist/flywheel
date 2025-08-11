# Pre-commit Formatting Failure

- **Date**: 2025-08-10
- **Author**: Codex
- **Status**: resolved

## What went wrong
Pre-commit failed on trailing whitespace in `docs/prompt-docs-todos.md` and a missing end-of-file newline in `webapp/static/models/examples/spool_core_sleeve_example.obj`.

## Root cause
Both files were committed with formatting issues that violate repository pre-commit hooks.

## Impact
The pre-commit step in CI failed, blocking merges.

## Actions to take
- Trim trailing whitespace in `docs/prompt-docs-todos.md`.
- Add a newline at the end of `webapp/static/models/examples/spool_core_sleeve_example.obj`.
- Audit remaining docs and static assets for similar issues.
