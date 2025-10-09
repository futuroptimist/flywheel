# Changelog
## 2025-10-10
- feat: add `flywheel spin --dry-run` to surface heuristic suggestions before
  LLM-backed workflows land.
- feat: include signed Δ values in `verify_fit` mesh dimension errors to match
  README guidance on highlighting oversize vs undersize parts.
- feat: prompt before injecting dev tooling in `flywheel update` and document
  the `--yes` flag.
- feat: auto-sort the prompt docs TODO table by type and repository to match
  triage guidance.
- feat: include repo snapshots in `flywheel prompt` output for richer context.
- fix: treat CI status API errors as failures when computing repo summary trunk
  status.
- fix: dedupe repo crawl specs so branch overrides do not trigger duplicate
  entries.
- fix: ensure `flywheel crawl` keeps the latest branch override when the same
  repository appears multiple times.
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
