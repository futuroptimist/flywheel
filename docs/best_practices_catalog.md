# Best Practices Catalog

This document explains the key conventions bundled with **flywheel** and how you can reuse them in your own projects.

Each section covers three points:

1. **Why it exists** and how the idea transfers to another repository.
2. **How it works** in simple terms.
3. **Maintenance tips** for both humans and LLM agents.

## Pre-commit Hooks

**Why:** Running `pre-commit` before every push keeps formatting and tests consistent.
It helps avoid CI failures and encourages small, clean commits.

**How it works:** The `.pre-commit-config.yaml` file lists hooks for `flake8`, `isort`,
`black`, `pytest`, and link checking. When you run `pre-commit run --all-files`, the
hooks format code, lint for errors, and run tests locally.

**Maintenance:** Add new lint or test tools to `.pre-commit-config.yaml` and update
`scripts/checks.sh`. LLM agents should check hook output and suggest fixes.

## Style Guides

**Why:** Standardized code style reduces friction during reviews. It also allows automated tools to reformat code.

**How it works:** Python projects use `flake8`, `isort`, and `black`. JavaScript relies on `eslint` and `prettier`. The relevant config lives in `docs/styleguides` and package files.

**Maintenance:** When introducing a new language or rule, document it under `docs/styleguides` and link to it here.

## uv for Python Installs

**Why:** [uv](https://github.com/astral-sh/uv) speeds up dependency installation compared to `pip`. Fast installs reduce wait time in CI and for new contributors.

**How it works:** `uv venv` creates a virtual environment and installs packages from `requirements.txt` using a compiled resolver.

**Maintenance:** Keep `requirements.txt` up to date. Mention `uv` commands in setup docs and check CI workflows for consistency.

### Running Python scripts with dependencies

**Why:** `uv` can execute a standalone script and automatically install any required packages on-the-fly. This keeps one-off utilities lightweight.

**How it works:** There are two ways to declare dependencies:

1. Pass them at runtime with `--with`:

   ```bash
   uv run --with rich example.py
   ```

2. Embed them using [PEP 723](https://peps.python.org/pep-0723/) metadata:

   ```bash
   uv add --script example.py 'requests<3' rich
   ```

   This inserts a block at the top of the file:

   ```python
   # /// script
   # dependencies = [
   #   "requests<3",
   #   "rich",
   # ]
   # ///
   ```

   Once present, run the script normally and `uv` handles installation automatically:

   ```bash
   uv run example.py
   ```

**Maintenance:** Encourage contributors to use inline metadata when sharing scripts. Document updates to the recommended flags here if the `uv` syntax evolves.

## Local Environments

**Why:** The `.local` folder lets each contributor store private configuration without committing it to the repository.

**How it works:** `./scripts/setup.sh YOURNAME YOURREPO` scaffolds `.local/README.md` and `.local/settings.env.example`, then ensures `.local/` appears in `.gitignore`. Git ignores everything inside so secrets remain private.

**Maintenance:** Remind contributors to rerun the setup script when new templates are added. LLMs should never log contents of `.local`.

## Conventional Commits

**Why:** Following the `feat:`, `fix:`, and `docs:` prefixes makes changelogs and release notes easier to generate.

**How it works:** Commit messages start with a type followed by a short summary. GitHub actions and release tools parse these prefixes to categorize changes.

**Maintenance:** Reject commits that do not follow the pattern. Update `.github/PULL_REQUEST_TEMPLATE.md` if new types are introduced.

## Continuous Integration

**Why:** Automated checks catch issues early and document the health of the project.

**How it works:** Workflows under `.github/workflows` run linting, tests, documentation checks, and security scans. Results appear on each pull request.

**Maintenance:** Add new jobs or matrix entries as tooling evolves. Keep the "Quality Targets" table in `docs/codex-custom-instructions.md` aligned with the workflows.

## Release Drafter

**Why:** Automatically compiling release notes saves time and ensures all contributions are recognized.

**How it works:** When commits land on `main`, a workflow updates the draft release notes using the commit history and PR titles.

**Maintenance:** Keep the workflow file and `CHANGELOG` format in sync. LLM agents should summarize notable changes in PR bodies.

## Runbook

**Why:** `runbook.yml` provides a checklist for bootstrapping and maintaining the repo.

**How it works:** Each stage lists tasks such as cloning the template, installing hooks, and merging releases. Humans or agents can follow it step by step.

**Maintenance:** Update the runbook whenever setup commands change. Link new documentation or scripts to the appropriate stage.

## Positive-Sum Values

**Why:** A welcoming community improves collaboration and code quality.

**How it works:** The [Code of Conduct](CODE_OF_CONDUCT.md) sets expectations for behavior. CONTRIBUTING.md reinforces respectful communication.

**Maintenance:** Review these documents periodically. Agents should flag outdated links or wording.

## Respecting Users

**Why:** Avoid manipulative design choices that erode trust.

**How it works:** The [dark-patterns guide](dark-patterns.md) outlines common traps and the "bright" alternatives we encourage. A companion [bright-patterns guide](bright-patterns.md) lists pro-user design elements. The repo crawler scans each repository for suspicious dark patterns and for positive bright patterns, recording the counts in `docs/repo-feature-summary.md`.

**Maintenance:** Update the pattern list and scanning heuristics as new anti-patterns emerge. Keep this catalog and the guide in sync.

## Maintaining This Catalog

- Add a new section whenever a best practice is added to the repository.
- Keep links to other docs (README, AGENTS, style guides) current.
- LLM agents should scan for config changes on each push and propose updates here.
- Humans can open small PRs to clarify steps or fix typos.
