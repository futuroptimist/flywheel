## 2025-10-16
- feat: add CLI `--help` examples to align with the release checklist.

## 2025-10-15
- feat: attach validation commands to `flywheel spin --dry-run` suggestions so
  operators can run follow-up checks after applying fixes.

## 2025-10-14
- feat: flag missing lint tooling in `flywheel spin --dry-run` with a new
  `add-linting` suggestion and analyzer toggle.
- feat: add analyzer toggles to `flywheel spin --dry-run` so operators can scope
  heuristic checks.

## 2025-10-13
- feat: prompt for telemetry opt-in on first CLI run to match telemetry design
  guidance.
- feat: add `flywheel config telemetry` to persist opt-in preferences under
  `~/.config/flywheel/`.
- feat: add `--no-save-dev` support to `flywheel init` to match CLI docs.
- feat: sort `flywheel spin --dry-run` suggestions by category and impact to
  match prompt doc guidance.
- feat: add heuristic `confidence` scores to `flywheel spin --dry-run`
  suggestions so the output matches the prompt schema.
## 2025-10-12
- feat: add table and markdown formats to `flywheel spin --dry-run` output for
  human-readable reviews.
- fix: tag lockfile suggestions in `flywheel spin --dry-run` with a `chore`
  category to match README guidance.
- feat: expand `language_mix` detection in `flywheel spin --dry-run` to cover
  Go, Rust, Java, shell scripts, and other common stacks.
## 2025-10-11
- feat: flag missing dependency lockfiles in `flywheel spin --dry-run` output and
  include lockfile metadata in the stats payload.
- feat: expose repository `language_mix` stats in `flywheel spin --dry-run` to
  honor the prompt doc requirement for language mix metrics.
- feat: align `flywheel spin --dry-run` CI detection with the repo summary
  keyword heuristic so deploy-only workflows no longer mask missing CI.
## 2025-10-10
- feat: flag missing `docs/` directories in `flywheel spin --dry-run` output.
- feat: add `flywheel spin --dry-run` to surface heuristic suggestions before
  LLM-backed workflows land.
- feat: include signed Δ values in `verify_fit` mesh dimension errors to match
  README guidance on highlighting oversize vs undersize parts.
- feat: prompt before injecting dev tooling in `flywheel update` and document
  the `--yes` flag.
- feat: auto-sort the prompt docs TODO table by type and repository to match
  triage guidance.
- feat: include repo snapshots in `flywheel prompt` output for richer context.
- feat: run ESLint and Prettier via `npm run lint` and `npm run format:check`
  to align with documented linting workflows.
- fix: scaffold `eslint.config.mjs` for new projects so the CLI matches the
  repository tooling update.
- fix: treat CI status API errors as failures when computing repo summary trunk
  status.
- fix: dedupe repo crawl specs so branch overrides do not trigger duplicate
  entries.
- fix: ensure `flywheel crawl` honors the latest branch override when the same
  repo appears multiple times.
## 2025-10-09
- fix: mark repo summary trunk status as n/a when CI is pending or missing.
- fix: allow the repo feature summary CLI to run directly by ensuring the flywheel package is on
  `sys.path`.

## 2025-10-08
- fix: mask short secrets when reporting scan-secrets findings.
- feat: add drag-to-rotate and scroll-to-zoom controls to the OBJ viewer with
  automated tests.
- feat: add `docs-lint` table consistency script and tests.

## 2025-10-07
- feat: scale `verify_fit` tolerances with the custom `tol` parameter and
  document stricter checks.

## 2025-10-06
- feat: detect mixed uv/pip installers and label workflows without installers as none.
- test: enforce parity between `docs/repo_list.txt` and `dict/prompt-doc-repos.txt` for prompt propagation.

## 2025-10-03
- feat: add CLI entry point for README related-project status updates

## 2025-10-01
- feat: add `flywheel runbook` CLI command and document the YAML checklist helper.

## 2025-09-05
- docs: start changelog to track project evolution.
