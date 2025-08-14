# Python 3.13 coverage install failure

- **Date**: 2025-08-14
- **Author**: Codex
- **Status**: resolved

## What went wrong
GitHub Actions runners upgraded to Python 3.13. The tests workflow attempted to
install `pytest-cov` and `coverage` with uv, but those packages lacked wheels for the
new Python release, causing dependency installation to fail.

## Root cause
The workflows requested `python-version: '3.x'`, allowing the unexpected Python
3.13 update that `uv pip install` could not satisfy.

## Impact
The Test Suite job exited before running tests, blocking CI on affected branches.

## Actions to take
- Pin workflows to Python 3.12.
- Add a regression test for the Python version.
