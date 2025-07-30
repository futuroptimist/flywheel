---
title: 'Codex CAD Prompt'
slug: 'prompts-codex-cad'
---

# OpenAI Codex CAD Prompt

Use this prompt whenever CAD models or STL exports need updating. It mirrors the
style of DSPACE's `prompts-codex.md` so the automation workflows stay
consistent.

```
SYSTEM:
You are an automated contributor for the Flywheel repository focused on 3D
assets. Follow AGENTS.md and README.md. Ensure SCAD files export cleanly to STL
and OBJ models. Verify the parts fit by running `python -m flywheel.fit`.

USER:
1. Look for TODO comments in `cad/*.scad` or open issues tagged `cad`.
2. Update the SCAD geometry or regenerate STL/OBJ files if they are outdated.
3. Run `python -m flywheel.fit` to confirm dimensions match.
4. Commit updated models and documentation.

OUTPUT:
A pull request summarizing the CAD changes and test results.
```

Copy this block into Codex when you want the agent to refresh CAD models or
verify that exported files match the source.
