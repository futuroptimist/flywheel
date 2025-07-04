# Codex Assistant Rules

This file expands on [`AGENTS.md`](AGENTS.md), [`llms.txt`](llms.txt) and
[`CLAUDE.md`](CLAUDE.md). Any LLM can refine these standards to keep the
flywheel turning smoothly.

## 1. Project Discovery
1. **Bootstrapping**
   - On cloning/opening a repo, immediately locate and parse:
     - `AGENTS.md`
     - `README.md`
     - Any project-specific docs (e.g. `QUESTS/`, `docs/`).
   - Infer the repo’s **primary goal**, architecture, language(s), and key modules before any changes.

2. **Clarify Missing Docs**
   - If **no** `AGENTS.md` exists, ask:
     > "What agent-oriented workflows or LLM-driven interactions would you like documented here?"
   - If the **README** is sparse, prompt for:
     - Installation steps
     - Usage examples
     - Contribution guidelines

## 2. Documentation Ownership
1. **AGENTS.md**
   - Keep it in sync with the code:
     - Update descriptions when new agents or prompt templates appear.
     - Add usage examples or CLI flags.
     - Fix typos and broken links.
2. **README.md**
   - Ensure it has:
     - Project badges (CI, coverage, PyPI/npm, license).
     - A clear "Getting Started" section.
     - Links to AGENTS.md and any "How to Contribute" guides.

3. **In-Code Prompts**
   - Search for LLM prompts in code (e.g. `PROMPT = """…"""`).
   - Standardize formatting:
     - A short **purpose** header
     - A **context** section with relevant code snippets
     - A **request** section at the bottom
   - Where appropriate, wrap prompts in helper functions to DRY-up repetition.

## 3. Code Quality & Quick Wins
1. **Low-hanging Fruit**
   - Run linters/formatters (e.g. `black`, `eslint`) and apply safe fixes.
   - Remove unused imports, dead code, or console/debug statements.
   - Fix any broken examples in docs or source comments.
2. **Basic Tests**
   - If no tests exist for a core module, generate a minimal test stub.
   - Where coverage is >0% but <50%, highlight modules lacking tests.

## 4. Cross-Project Synergies
1. **Shared Utilities**
   - Spot duplicate logic (e.g. config loading, authentication) across repos:
     - Propose extraction into a common package (e.g. `@futuroptimist/common`).
2. **Consistent Templates**
   - Use the same PR, issue, and commit message templates in all projects.
   - Harmonize code style and tooling (e.g. the same ESLint/Prettier or Flake8/black config).

## 5. Quest & Flywheel Enhancement (dspace-specific)
1. **Tech-Tree Gaps**
   - Parse existing quests and their prerequisites.
   - Suggest 1–2 new quests that naturally follow each completed branch.
2. **Automated Quest Scaffolding**
   - Add or improve an "`npm run generate-quest`" (or equivalent) to scaffold:
     - Metadata (title, description, requirements)
     - Placeholder code/tests
3. **Prompt-Driven Quest Creation**
   - Enhance any in-repo prompts so Codex can, on command, "Create a new quest called X that requires Y and teaches Z."

## 6. Continuous Feedback Loop
- **On every push**:
  1. Re-scan for new or changed prompts/docs.
  2. Check for new low-hanging documentation or lint fixes.
  3. Propose a small "doc/code hygiene" PR alongside any feature work.
- **Always err on the side of small, incremental improvements** rather than big rewrites or new deps.

---

> \U0001F527 **Tip:** If you ever feel stuck, revisit the project’s README goals and the “flywheel” concept—every little doc or prompt tweak should help the next contributor onboard faster and push the wheel a bit further.
