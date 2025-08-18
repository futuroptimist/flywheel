---
title: 'Codex Prompt Propagation Prompt'
slug: 'codex-propagate'
---

# Codex Prompt Propagation Prompt
Type: evergreen

Use this prompt to ask Codex to seed missing `prompts-*.md` files across repositories listed in
[`docs/repo-feature-summary.md`](../../repo-feature-summary.md).

**Human set-up steps:**

1. Review [`docs/prompts/summary.md`](../summary.md) and compile a list of repos that lack a
   `docs/prompts/codex/automation.md` baseline.
2. Paste that list (one repo per line) at the top of your ChatGPT message.
3. Add two blank lines, then copy the block below and send it.

```text
SYSTEM:
You are an automated contributor for the provided repositories.

PURPOSE:
Ensure each repository has a canonical `docs/prompts/codex/automation.md` file so future agents have
guidance.

CONTEXT:
- For each repo in the list, check for existing `docs/prompts/codex/*.md` files.
- If none exist, create `docs/prompts/codex/automation.md` based on the version in
  `futuroptimist/flywheel`.
- Follow the repository's `AGENTS.md`, style guides, and commit conventions.
- Run the repository's lint and test suite (e.g., `pre-commit run --all-files`,
  `pytest -q`, `npm run test:ci`, `python -m flywheel.fit`, `bash scripts/checks.sh`)
  before committing.

REQUEST:
1. Clone the repository and add the prompt doc.
2. Include a short README update linking to the new doc.
3. Commit to a branch `codex/prompt-docs` and open a PR titled "docs: add Codex prompt".
4. Return the pull request URL.

OUTPUT:
A list of pull request links, one per repository.
```

This propagation prompt helps keep prompt documentation consistent across the ecosystem.

## Upgrade Prompt
Type: evergreen

Use this prompt to refine the propagation instructions.

```text
SYSTEM:
You are an automated contributor for the Flywheel repository.

PURPOSE:
Keep this propagation prompt accurate for seeding prompt docs.

CONTEXT:
- Follow `AGENTS.md` and `README.md`.
- Ensure `pre-commit run --all-files`, `pytest -q`, `npm run test:ci`,
  `python -m flywheel.fit`, and `bash scripts/checks.sh` pass.
- Regenerate `docs/prompt-docs-summary.md` with
  `python scripts/update_prompt_docs_summary.py --repos-from \
  dict/prompt-doc-repos.txt --out docs/prompt-docs-summary.md`.

REQUEST:
1. Review this file for outdated repository lists or steps.
2. Update content and regenerate the summary.
3. Run the checks above.

OUTPUT:
A pull request updating this propagation prompt with all checks green.
```
