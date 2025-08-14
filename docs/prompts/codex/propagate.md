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
Ensure each repository has a canonical `docs/prompts/codex/automation.md` file so future agents have guidance.

CONTEXT:
- For each repo in the list, check for existing `docs/prompts/codex/*.md` files.
- If none exist, create `docs/prompts/codex/automation.md` based on the version in `futuroptimist/flywheel`.
- Follow the repository's `AGENTS.md`, style guides, and commit conventions.
- Run `npm run lint` (or equivalent) and the primary test suite before committing.

REQUEST:
1. Clone the repository and add the prompt doc.
2. Include a short README update linking to the new doc.
3. Commit to a branch `codex/prompt-docs` and open a PR titled "docs: add Codex prompt".
4. Return the pull request URL.

OUTPUT:
A list of pull request links, one per repository.
```

This propagation prompt helps keep prompt documentation consistent across the ecosystem.
