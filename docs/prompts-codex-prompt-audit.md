---
title: 'Codex Prompt Audit Prompt'
slug: 'prompts-codex-prompt-audit'
---

# OpenAI Codex Prompt Audit Prompt

Use this prompt in any repository to audit whether standard Codex prompts or obvious TODOs are missing.
It checks the central Prompt Docs Summary for common patterns and scans the repo for gaps.

**Human set-up steps**
1. Paste the target repository URL on the first line of your ChatGPT message.
2. Press <kbd>Enter</kbd> twice to insert two blank lines.
3. Copy the entire block below and paste it after the blank lines.
4. Send the message.

```text
SYSTEM:
You are an automated contributor for the target repository.

PURPOSE:
Identify missing prompt files or unchecked roadmap items and propose next steps.

CONTEXT:
- Consult https://github.com/futuroptimist/flywheel/blob/main/docs/prompt-docs-summary.md to see existing prompt templates across projects.
- Look for absent common prompts (CI fix, spellcheck, upgrade guides, etc.).
- Review README, docs, and roadmaps for unchecked boxes or TODO comments.
- Follow repository conventions and commit rules.

REQUEST:
1. List any missing prompt types or obvious tasks.
2. Suggest minimal pull requests that would add the missing material.
3. If everything is covered, respond that no action is needed.

OUTPUT:
A concise summary of findings and recommended actions.
```

Copy this block whenever you want Codex to audit a repository's prompt coverage and roadmap.
