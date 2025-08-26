# Changelog

## [2025-08-27] - Scan root docs for prompt files
- include `docs/prompts-*.md` in prompt docs crawler

## [2025-08-25] - Defer tabulate import in prompt doc script
- allow tests to run without installing tabulate

## [2025-08-23] - Fix newline in prompt docs summary
- add missing newline to docs/prompt-docs-summary.md to satisfy pre-commit

## [2025-08-22] - Use typos for docs spellcheck
- replace flaky aspell-based spellchecker with crate-ci/typos

## [2025-08-16] - Skip run-checks in prompt docs workflow
- avoid failing scheduled doc summary by bypassing project checks

## [2025-08-15] - Skip Codecov upload without token
- guard coverage uploads so forks without secrets keep CI green

## [2025-08-15] - Safely handle symbolic link destinations
- avoid deleting linked directories when cloning repos

## [2025-08-15] - Fix spellcheck noise in prompt summary
- disable spellchecker on generated summary to keep docs workflow green

## [2025-08-16] - Skip run-checks in repo summary workflow
- prevent Update Repo Feature Summary job from running full project checks

## [2025-08-14] - Pin Python version in CI
- lock workflows to Python 3.12 to avoid uv install failures

## [2025-08-13] - Stabilize viewer model tests
- ensure model dropdown options are loaded before evaluation
