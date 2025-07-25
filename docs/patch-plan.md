# Patch Plan

This patch extends the flywheel template with a Python CLI and agent hook.

## Code
- new `flywheel` package exposing a `flywheel` command with subcommands
  `init`, `update`, `audit`, `prompt`, and `crawl`.
- `--save-dev` option copies ESLint/Prettier configs, CI workflows,
  DEPENDABOT settings and release scripts into a target repository.
- added minimal `.eslintrc.json` and `.prettierrc` used as templates.
- interactive prompts ask for language and dev tooling unless `--yes` is used.
- repo crawler uses the `requests` library to fetch files.
- root `requirements.txt` lists `requests` so CI installs dependencies.

## Tests
- end-to-end tests verify template generation and idempotency by running the CLI twice against a temporary directory.

## Documentation
- README updated with CLI usage examples.
- AGENTS.md mentions the new prompt agent.
- this patch plan tracks planned additions for future reference.
