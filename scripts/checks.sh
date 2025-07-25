#!/usr/bin/env bash
set -e

# python checks
flake8 . --exclude=.venv
isort --check-only . --skip .venv
black --check . --exclude ".venv/"

# js checks
if [ -f package.json ]; then
  npm ci
  npx playwright install --with-deps
  npm run lint
  npm run format:check
  npm test -- --coverage
fi

# run tests
pytest -q

# security scans
bandit -r flywheel -x tests,hardware/stl,hardware/parts --severity-level medium
safety check -r requirements.txt --full-report --continue-on-error

# docs checks
if command -v pyspelling >/dev/null 2>&1 && [ -f .spellcheck.yaml ]; then
  pyspelling -c .spellcheck.yaml || true
fi
linkchecker README.md docs/ || true
