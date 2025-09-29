---
title: 'Codex Implement.md Prompt'
slug: 'codex-implement-md'
conversational: true
---

# Codex Implement.md Prompt
Type: evergreen

Use this prompt to draft or refresh an `implement.md` for the target repository using existing exemplars.

```text
Study these implement.md playbooks before you start:
- [democratizedspace/dspace](https://github.com/democratizedspace/dspace/blob/v3/docs/prompts/codex/implement.md)
- [futuroptimist/token.place](https://github.com/futuroptimist/token.place/blob/main/docs/prompts/codex/implement.md)
- [futuroptimist/sugarkube](https://github.com/futuroptimist/sugarkube/blob/main/docs/prompts/codex/implement.md)
- [futuroptimist/jobbot3000](https://github.com/futuroptimist/jobbot3000/blob/main/docs/prompts/codex/implement.md)
- [futuroptimist/danielsmith.io](https://github.com/futuroptimist/danielsmith.io/blob/main/docs/prompts/codex/implement.md)

Task: create or update the target repository's `implement.md` so it reflects current engineering practices.

Checklist:
1. Confirm the repo's coding conventions, primary languages, and package managers.
2. Describe the expected workflow (branch naming, commit strategy, PR review) in actionable steps.
3. Enumerate mandatory tests, linters, and local verification commands before opening a PR.
4. Highlight repo-specific gotchas (monorepo layout, required environment variables, generated assets).
5. Provide a short upgrade section explaining how to keep the document current.

When finished, output the complete `implement.md` in a single fenced code block, ready to copy into the repo.
```

## Upgrade Prompt
Type: evergreen

Use this prompt to keep the Implement.md prompt aligned with the broader ecosystem.

```text
Scan every repository linked from https://github.com/futuroptimist#related-projects.

1. Open each repo's existing `docs/prompts/codex/implement.md` (or equivalent).
   Confirm it appears in the reference list above.
2. If any repository lacks an `implement.md`, file an issue or add a TODO note describing the gap.
3. Update the reference list in the primary prompt's first code block.
   Ensure it includes every available `implement.md` across the related-projects repos.
4. Summarize your changes and note any repos that still need an `implement.md` playbook.

After editing, run these checks:
- `pre-commit run --all-files`
- `pyspelling -c .spellcheck.yaml`
- `linkchecker --no-warnings README.md docs/`
- `git diff --cached | ./scripts/scan-secrets.py`

If all commands succeed, reply with `All lightweight checks passed. Ready for CI.` Otherwise, explain what failed.
```
