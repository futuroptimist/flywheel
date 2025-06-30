# Patch Plan

This update introduces a small CLI for applying flywheel templates and new tests.

## Code
- `flywheel.py` implements `init`, `update`, `audit`, and `prompt` subcommands with a `--save-dev` flag.
- Dev tooling templates live in `templates/dev` and include ESLint, Prettier, CI, Dependabot, and release scripts.

## Tests
- Added `tests/test_cli.py` to verify template generation and idempotency.

## Documentation
- README updated with instructions for embedding flywheel.
- AGENTS file updated with new Prompt Hook agent.
