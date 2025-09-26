# JavaScript tests slowed by Python dependency build

- **Date**: 2025-09-26
- **Author**: Codex
- **Status**: resolved

## What went wrong
The `test (javascript)` GitHub Actions job began running for more than ten minutes, far above the
normal ~3 minute completion time.

## Root cause
Commit 2132cb8 (2025-07-19) expanded `requirements.txt` with 3-D tooling such as `assimp_py`. The
JavaScript workflow installs everything in that file before running Playwright. Because `assimp_py`
ships source-only wheels, pip rebuilt it from C++ each run, extending the job runtime by several
minutes.

## Impact
JavaScript CI checks (e.g. [run 18029996098](https://github.com/futuroptimist/flywheel/actions/runs/18029996098/job/51304258464))
spent ~10 minutes compiling native dependencies, delaying feedback and burning GitHub Actions
minutes.

## Actions to take
- Install only the webapp dependencies needed for Playwright (`Flask`, `trimesh`).
- Add a regression test that asserts the workflow references the lightweight requirement file.
- Keep heavy modeling libraries (e.g. `assimp_py`) scoped to build jobs that need them.
