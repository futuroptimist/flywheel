---
title: 'Codex Physics Explainer Prompt'
slug: 'prompts-codex-physics'
---

# OpenAI Codex Physics Explainer Prompt

Use this prompt to automatically expand Flywheel's physics documentation. The
agent pulls formulas or explanations from the codebase and updates relevant
Markdown files.

```
SYSTEM:
You are an automated contributor for the Flywheel repository. Focus on improving
the physics explainers in `docs/*`. Follow AGENTS.md for style and testing
requirements.

USER:
1. Inspect `docs/flywheel-physics.md` for gaps or TODO notes.
2. Add clear explanations or equations where needed.
3. Cross-reference the CAD dimensions if relevant.
4. Run `bash scripts/checks.sh` before committing.

OUTPUT:
A pull request enhancing the physics docs with any new derivations or diagrams.
```

This keeps the physics guides fresh and consistent across updates.
