#!/usr/bin/env bash
set -e

# security scan helper
run_security_checks() {
  if command -v bandit >/dev/null 2>&1; then
    bandit -r flywheel -x tests,stl --severity-level medium
  else
    echo "bandit not installed; skipping security scan"
  fi
  if command -v safety >/dev/null 2>&1; then
    safety check -r requirements.txt --full-report --continue-on-error
  else
    echo "safety not installed; skipping dependency scan"
  fi
}

if [ "${RUN_SECURITY_ONLY}" = "1" ]; then
  run_security_checks
  exit 0
fi

# python checks
flake8 . --exclude=.venv,node_modules
isort --check-only . --skip .venv --skip node_modules
black --check . --exclude ".venv/|node_modules/"

# js checks
if [ -f package.json ]; then
  npm ci
  if [ -z "$SKIP_E2E" ]; then
    npm run playwright:install
    npm run lint
    npm run format:check
    npm run test:ci
  else
    echo "SKIP_E2E set; skipping Playwright installation and e2e tests" >&2
    npm run lint
    npm run format:check
    npm run jest -- --coverage
  fi
fi

# run tests
pytest -q

# security scans
run_security_checks

# docs checks
if [ -f package.json ]; then
  npm run docs-lint
fi
if command -v codespell >/dev/null 2>&1; then
  codespell \
    --ignore-words dict/allow.txt \
    --skip ".git,.venv,node_modules,dist,build,docs-site,coverage,*.lock,*.min.js,*.stl,*.obj,*.glb,*.gltf,*.png,*.jpg" \
    --quiet-level 2
else
  echo "codespell not installed; skipping spell check"
fi

if command -v pyspelling >/dev/null 2>&1 && [ -f .spellcheck.yaml ]; then
  pyspelling -c .spellcheck.yaml || true
fi
linkchecker --no-warnings README.md docs/ || true
