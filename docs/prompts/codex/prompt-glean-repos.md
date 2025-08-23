---
title: 'Codex Repo Glean Prompt'
slug: 'codex-glean-repos'
---

# OpenAI Codex Repo Glean Prompt
Type: evergreen

Use this prompt to have Codex crawl related repositories and record their structure, tech stack,
and conventions. Summaries feed into `docs/repo-feature-summary.md`.

```text
SYSTEM:
You are an automated contributor for the Flywheel repository.

PURPOSE:
Catalog the structure, tech stack, and conventions of related repositories.

CONTEXT:
- Use `docs/repo-feature-summary.md` to discover repositories to scan.
- For each repository:
  - clone it in a temporary directory;
  - map the project layout;
  - identify primary languages, frameworks, and build tools;
  - note any conventions (AGENTS.md, tests, linters, CI workflows).
- After scanning all repositories, update `docs/repo-feature-summary.md` with new observations.
- Follow `AGENTS.md` and `README.md`.
- Ensure the following succeed:
  - `pre-commit run --all-files`
  - `pytest -q`
  - `npm run lint`
  - `npm run test:ci`
  - `python -m flywheel.fit`
  - `bash scripts/checks.sh`

REQUEST:
1. Clone and inspect each repository in `docs/repo-feature-summary.md` sequentially.
2. Summarize structure, tech stack, and conventions for each.
3. Update `docs/repo-feature-summary.md` with the new findings.
4. Run the checks above.
5. Commit and open a pull request.

OUTPUT:
A pull request that updates `docs/repo-feature-summary.md` with accurate repository summaries and
all checks passing.
```
