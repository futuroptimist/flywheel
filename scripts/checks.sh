#!/usr/bin/env bash
set -e

# python checks
flake8 .
isort --check-only .
black --check .

# js checks
if [ -f package.json ]; then
  npm ci
  npm run lint
  npm run format:check
  npm test -- --coverage
fi

# run tests
pytest -q

# docs checks
if command -v pyspelling >/dev/null 2>&1 && [ -f spellcheck.yaml ]; then
  pyspelling -c spellcheck.yaml || true
fi
linkchecker README.md docs/ || true
