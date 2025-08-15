# Changelog

## [2025-08-15] - Ignore localhost links in docs checks
- skip localhost URLs during link checking to avoid CI failure
## [2025-08-15] - Skip Codecov upload without token
- guard coverage uploads so forks without secrets keep CI green

## [2025-08-15] - Safely handle symbolic link destinations
- avoid deleting linked directories when cloning repos

## [2025-08-14] - Pin Python version in CI
- lock workflows to Python 3.12 to avoid uv install failures

## [2025-08-13] - Stabilize viewer model tests
- ensure model dropdown options are loaded before evaluation
