### Cursor Rules Quick Reference (2025-09-xx)

# Overview
- Cursor rules provide persistent, system-level instructions for the Agent and Inline Edit so models follow your workflows across sessions.
- Apply rules to capture project conventions, automate repetitive edits, and standardize how the AI collaborates with your team.

# Rule types
- **Project rules** – Stored as Markdown Context (`.mdc`) files in `.cursor/rules/`. Version-controlled alongside source and visible in the Agent sidebar.
- **User rules** – Managed from *Cursor Settings › Rules*. Global to your Cursor environment and automatically applied in every workspace.
- **Team rules** – Created in the Cursor dashboard for Team and Enterprise plans. Enforced across all members to guarantee shared standards.
- **AGENTS.md** – Markdown instructions co-located with code (root or nested folders) that augment project rules for specific paths.

# How rules work
- Large language models forget previous completions; rules inject consistent context at the top of each prompt.
- Active rules appear in both chat and Inline Edit transcripts. They do **not** affect Cursor Tab or other AI surfaces.
- Rule precedence: **Team rules → Project rules → User rules**. Higher-precedence content overrides conflicting guidance.

# Project rules
- Lives under `.cursor/rules/`; each file represents a single rule.
- Use project rules to:
  - Encode domain-specific knowledge about your codebase.
  - Automate project-specific workflows or templates.
  - Standardize style, architecture, or review expectations.
- Rules can be:
  - **Always** – permanently included in the model context (`alwaysApply: true`).
  - **Auto Attached** – activated when edited or referenced files match configured glob patterns.
  - **Manual** – inserted on demand via `@rule-name` in chat or Inline Edit prompts.

# Rule anatomy
- Rule files are Markdown with optional front matter describing activation metadata.

```md
---
description: RPC Service boilerplate
globs:
  - services/**/*.ts
alwaysApply: false
---

- Use our internal RPC pattern when defining services.
- Always use `snake_case` for service names.

@service-template.ts
```

- Key fields:
  - `description` – One-line summary shown in UI pickers.
  - `globs` – File patterns that trigger Auto Attached rules.
  - `alwaysApply` – Forces inclusion without matching files.
  - Inline `@filename` references pin supplemental files into the prompt.

# Nested rules
- Place additional `.cursor/rules/` folders inside subdirectories to scope guidance tightly.

```
project/
  .cursor/rules/        # Project-wide rules
  backend/
    server/
      .cursor/rules/    # Backend-specific rules
  frontend/
    .cursor/rules/      # Frontend-specific rules
```

# Creating rules
- In Cursor, open *Settings › Rules* and click **New Cursor Rule** to scaffold a `.mdc` file.
- Alternatively, add Markdown files manually under `.cursor/rules/`; they are picked up instantly and tracked by git.

# Generating rules with AI
- Use the `/Generate Cursor Rules` slash command in chat to draft new rules from existing context.
- Best practices when authoring or refining rules:
  - Keep each rule focused, actionable, and under ~500 lines.
  - Split large requirements into smaller, composable rules.
  - Provide concrete examples or linked files so the AI can ground its responses.
  - Avoid vague guidance—write them like internal runbooks.
  - Reuse rules when repeating prompts across chats.

# Team rules
- Managed in the Cursor dashboard with options to **Enable** immediately or **Enforce** so members cannot disable them.
- Use for compliance, secure defaults, and consistent team-wide workflows without per-developer setup.
- Team rules accept plain-text content with optional `globs` and `alwaysApply` metadata to target files or enforce blanket coverage.

# AGENTS.md integration
- Cursor reads `AGENTS.md` files from the project root and nested directories to provide localized guidance.
- Layer multiple `AGENTS.md` files to match repository structure:

```
project/
  AGENTS.md              # Global instructions
  frontend/
    AGENTS.md            # Frontend-specific instructions
    components/
      AGENTS.md          # Component guidance
  backend/
    AGENTS.md            # Backend-specific instructions
```

- Combine `AGENTS.md` with project rules to balance high-level standards and directory-specific notes.

# FAQ highlights
- Rules cannot reference other rules directly, but `@filename` annotations can pull companion files into context.
- Legacy Agent Applied rules can be migrated via the **Convert Legacy Agent Applied Rules** flow in settings.
- If a rule is not applied, confirm its `globs` match the edited files or call it manually with `@rule-name`.
- Rules influence the Agent and Inline Edit features only; other AI tools in Cursor ignore them.
