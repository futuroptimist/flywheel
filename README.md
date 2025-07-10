# 🎡 flywheel

[![Lint & Format](https://img.shields.io/github/actions/workflow/status/futuroptimist/flywheel/.github/workflows/01-lint-format.yml?label=lint%20%26%20format)](https://github.com/futuroptimist/flywheel/actions/workflows/01-lint-format.yml)
[![Tests](https://img.shields.io/github/actions/workflow/status/futuroptimist/flywheel/.github/workflows/02-tests.yml?label=tests)](https://github.com/futuroptimist/flywheel/actions/workflows/02-tests.yml)
[![Coverage](https://codecov.io/gh/futuroptimist/flywheel/branch/main/graph/badge.svg)](https://codecov.io/gh/futuroptimist/flywheel)
[![Docs](https://img.shields.io/github/actions/workflow/status/futuroptimist/flywheel/.github/workflows/03-docs.yml?label=docs)](https://github.com/futuroptimist/flywheel/actions/workflows/03-docs.yml)
[![License](https://img.shields.io/github/license/futuroptimist/flywheel)](LICENSE)

**flywheel** is a GitHub template for rapid project bootstrapping. It bundles linting, testing, documentation checks, and LLM-powered agents to keep your repo healthy.

## Usage

1. **Use as a template** on GitHub.
2. Clone your new repo and run `./scripts/setup.sh YOURNAME NEWREPO` to personalize placeholders.
3. Commit and push to start the flywheel.

## Contents

- CI workflows for linting, tests, and docs
- DEPENDABOT for automated dependency updates
- CodeQL workflow for security scanning
- Style guides for Python and JavaScript
- Fast Python installs powered by [uv](https://github.com/astral-sh/uv)
- Example code and templates
- Python CLI with subcommands `init`, `update`, `audit`, `prompt`, and `crawl` that prompts interactively unless `--yes` is used
- [AGENTS.md](AGENTS.md) detailing included LLM assistants
- [llms.txt](llms.txt) with quick context for AI helpers
- [CLAUDE.md](CLAUDE.md) summarizing Anthropic guidance
- [CUSTOM_INSTRUCTIONS.md](CUSTOM_INSTRUCTIONS.md) for Codex rules
  and a [runbook.yml](runbook.yml) checklist for repo setup
- Axel integration guide in `docs/axel-integration.md`
- DSPACE synergy doc in `docs/dspace-integration.md`
- token.place roadmap in `docs/tokenplace-roadmap.md`
- local environment guide in `docs/local-environments.md`
- token.place features in `docs/tokenplace-features.md`
- token.place PRD in `docs/tokenplace-PRD.md`
- f2clipboard integration in `docs/f2clipboard-integration.md`
- Futuroptimist integration in `docs/futuroptimist-integration.md`
- Gabriel integration in `docs/gabriel-integration.md`
- Sigma integration in `docs/sigma-integration.md`
- Web viewer instructions in `docs/web-viewer.md`
- Flywheel construction guide in `docs/flywheel-construction.md` with CAD files in `cad/`
  including `stand.scad`, `shaft.scad`, and `adapter.scad`. Assembly details live in `docs/flywheel-stand.md`, clamp instructions in `docs/flywheel-adapter.md`, and physics in `docs/flywheel-physics.md`

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

# Install uv and pre-commit hooks
curl -Ls https://astral.sh/uv/install.sh | sh
uv venv
uv pip install pre-commit
pre-commit install

# Run checks before committing
pre-commit run --all-files
```

### Embedding in an existing project

Install the CLI and inject dev tooling. Without `--yes`, the command prompts for language and whether to add dev tools:

```bash
pipx run flywheel init . --language python --save-dev --yes
```

### Generating Codex prompts

Invoke the prompt agent to get repo-aware suggestions:

```bash
flywheel prompt
```

### Generating repo feature summary

Create a Markdown table showing which flywheel files each repo uses:

```bash
flywheel crawl futuroptimist/flywheel futuroptimist/axel --output docs/repo-feature-summary.md
```
Append `@branch` to any repo to crawl a non-default branch, e.g. `owner/name@dev`.
Pass `--token YOURTOKEN` or set `GITHUB_TOKEN` to avoid API rate limits.
The table in `docs/repo-feature-summary.md` is automatically refreshed after each commit via GitHub Actions.
The summary now records the short SHA of the latest commit and the name of each repository's default branch.

## Values

We aim for a positive-sum, empathetic community. The flywheel embraces regenerative and open-source principles to keep energy cycling back into every project.

## Related Projects

- **[token.place](https://token.place)** – stateless faucet for LLM inference with zero auth friction ([repo](https://github.com/futuroptimist/token.place))
- **[DSPACE](https://democratized.space)** – offline-first idle-sim where aquariums meet maker quests ([repo](https://github.com/democratizedspace/dspace))
- **[flywheel](https://github.com/futuroptimist/flywheel)** – opinionated boilerplate for reproducible CI and releases
- **[gabriel](https://github.com/futuroptimist/gabriel)** – guardian-angel LLM that nudges safer digital hygiene
- **[f2clipboard](https://github.com/futuroptimist/f2clipboard)** – bulk-copy files from nested dirs straight to your clipboard
- **[axel](https://github.com/futuroptimist/axel)** – LLM-powered quest tracker for repos and next steps
- **[sigma](https://github.com/futuroptimist/sigma)** – open-source AI pin device
- **[gitshelves](https://github.com/futuroptimist/gitshelves)** – turn GitHub contributions into 3D-printable block models
- **[wove](https://github.com/futuroptimist/wove)** – open-source toolkit for knitting and robotic looms

A summary of flywheel features adopted across repos lives in [docs/repo-feature-summary.md](docs/repo-feature-summary.md).
