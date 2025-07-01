# Patch Plan

This patch extends the flywheel template with a Python CLI and agent hook.

## Code
- new `flywheel` package exposing a `flywheel` command with subcommands
  `init`, `update`, `audit`, and `prompt`.
- `--save-dev` option copies ESLint/Prettier configs, CI workflows,
  DEPENDABOT settings and release scripts into a target repository.
- added minimal `.eslintrc.json` and `.prettierrc` used as templates.

## Tests
- end-to-end tests verify template generation and idempotency by running the CLI twice against a temporary directory.

## Documentation
- README updated with CLI usage examples.
- AGENTS.md mentions the new prompt agent.
- this patch plan tracks planned additions for future reference.
