# 🎡 flywheel

[![Lint & Format](https://img.shields.io/github/actions/workflow/status/__OWNER__/__REPO__/.github/workflows/01-lint-format.yml)]()
[![Tests](https://img.shields.io/github/actions/workflow/status/__OWNER__/__REPO__/.github/workflows/02-tests.yml)]()
[![Docs](https://img.shields.io/github/actions/workflow/status/__OWNER__/__REPO__/.github/workflows/03-docs.yml)]()
[![License](https://img.shields.io/github/license/__OWNER__/__REPO__)]()

**flywheel** is a GitHub template for rapid project bootstrapping. It bundles linting, testing, documentation checks, and LLM-powered agents to keep your repo healthy.

## Usage

1. **Use as a template** on GitHub.
2. Clone your new repo and run `./scripts/setup.sh YOURNAME NEWREPO` to personalize placeholders.
3. Commit and push to start the flywheel.

## Contents

- CI workflows for linting, tests, and docs
- Style guides for Python and JavaScript
- Example code and templates
- [AGENTS.md](AGENTS.md) detailing included LLM assistants

## Getting Started

```bash
# Clone your fork
git clone git@github.com:YOURNAME/NEWREPO.git
cd NEWREPO

# Personalize badge URLs and docs
./scripts/setup.sh YOURNAME NEWREPO

# Commit
git add .
git commit -m "chore: initialize flywheel"

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run checks before committing
pre-commit run --all-files
```
