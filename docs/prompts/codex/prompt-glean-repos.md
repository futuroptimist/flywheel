---
title: 'Codex Repo Glean Prompt'
slug: 'codex-glean-repos'
---

# Codex Repo Glean Prompt
Type: evergreen

Use this prompt to inventory related repositories. Paste it into the OpenAI Codex CLI to
crawl each project, record its structure, tech stack and conventions, and refresh
`docs/repo-feature-summary.md`.

```
SYSTEM:
You are an automated repo auditor using Flywheel's RepoCrawler.

PURPOSE:
Discover how each related repository is organized and which conventions it follows.

CONTEXT:
- The repositories to scan are listed in docs/repo-feature-summary.md.
- Follow AGENTS.md and any repo-specific guides.
- Prefer existing tools like `python -m flywheel.agents.scanner` and `rg`.

REQUEST:
1. For each repository in docs/repo-feature-summary.md:
   a. Clone the repository.
   b. List its major directories and primary languages.
   c. Identify build systems, package managers, linters and test frameworks.
   d. Note presence of AGENTS.md, pre-commit config and other community files.
2. Update docs/repo-feature-summary.md with the gathered details.
3. Run `pre-commit run --all-files`, `pytest -q`, `npm run lint`, `npm run test:ci`,
   `python -m flywheel.fit` and `bash scripts/checks.sh`.
4. Commit with a brief message.

OUTPUT:
A pull request containing the updated docs/repo-feature-summary.md and passing checks.
```
