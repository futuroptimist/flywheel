#!/usr/bin/env bash
set -e

# python checks
if command -v flake8 >/dev/null 2>&1; then
  flake8 .
fi
if command -v isort >/dev/null 2>&1; then
  isort --check-only .
fi
if command -v black >/dev/null 2>&1; then
  black --check .
fi

# js checks
if [ -f package.json ]; then
  npm run lint
  npm run format:check
fi

# run tests if pytest available
if command -v pytest >/dev/null 2>&1; then
  pytest -q
fi

# docs link check if linkchecker installed
if command -v linkchecker >/dev/null 2>&1; then
  linkchecker README.md docs/ || true
fi
