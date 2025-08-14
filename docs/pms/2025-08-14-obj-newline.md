# OBJ model missing trailing newline

- Date: 2025-08-14
- Author: Codex
- Status: fixed

## What went wrong
A static OBJ model lacked a trailing newline, causing the `end-of-file-fixer`
pre-commit hook to fail and block CI.

## Root cause
The file `webapp/static/models/spool_core_sleeve/sunlu55_to73_len60.obj` did not
terminate with a newline character, which violated repository formatting rules.

## Impact
Pre-commit checks failed, preventing changes from merging.

## Actions to take
- Add a unit test asserting all OBJ files end with a newline.
- Document OBJ formatting requirements in contributing guide.
