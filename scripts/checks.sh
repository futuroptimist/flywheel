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
if command -v bandit >/dev/null 2>&1; then
  bandit -r flywheel -x tests,stl --severity-level medium
else
  echo "bandit not installed, skipping bandit scan"
fi
if command -v safety >/dev/null 2>&1; then
  safety check -r requirements.txt --full-report --continue-on-error
else
  echo "safety not installed, skipping dependency scan"
fi

# docs checks
if command -v pyspelling >/dev/null 2>&1 && [ -f .spellcheck.yaml ]; then
  pyspelling -c .spellcheck.yaml || true
fi
linkchecker README.md docs/ || true
