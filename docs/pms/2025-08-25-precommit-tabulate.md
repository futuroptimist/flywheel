# 2025-08-25: Pre-commit tabulate import

- **Date:** 2025-08-25
- **Author:** codex-bot
- **Status:** fixed

## What went wrong
Pre-commit checks failed because `scripts/update_prompt_docs_summary.py` imported `tabulate` at module load and the hook environment lacked the dependency.

## Root cause
Module-level import of `tabulate` caused `ModuleNotFoundError` during test collection when `tabulate` wasn't installed.

## Impact
CI failed on `run project checks`, blocking merges.

## Actions to take
- move `tabulate` import inside `main` so only the CLI requires it
- consider adding optional dependency check in script
