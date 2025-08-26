# Pre-commit run-checks missing tabulate

- Date: 2025-08-25
- Author: OpenAI Assistant
- Status: Resolved

## What went wrong
Pre-commit run-checks hook failed during test collection.

## Root cause
The hook environment didn't install the tabulate package required by tests.

## Impact
CI jobs using pre-commit could not run tests and failed.

## Actions to take
- Include tabulate in the pre-commit hook's additional dependencies.
- Monitor future runs for similar missing packages.
