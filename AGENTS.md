# \U0001F916 AGENTS

This project uses several lightweight LLM assistants to keep the flywheel spinning.

## Code Linter Agent
- **When:** every PR
- **Does:** run ESLint/Flake8 and suggest patches

## Docs Agent
- **When:** docs or README change
- **Does:** spell-check and link-check, suggest style tweaks

## Quest Generator Agent
- **When:** you request a new quest
- **Does:** scaffold metadata, code stubs, and tests

## Synergy Bot
- **When:** multiple repos evolve
- **Does:** detect duplicate utilities and propose extraction into a shared package

---

For personalization, run `./scripts/setup.sh YOURNAME YOURREPO` after cloning.
