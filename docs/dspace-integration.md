# Integrating with DSPACE

[DSPACE](https://github.com/democratizedspace/dspace) is an offline-first idle simulation that blends aquarium management with maker quests. The project serves as a playground for Flywheel's quest generator and showcases how an open source game can reuse this repository's automation loops.

## Why DSPACE Matters

- Demonstrates offline-friendly patterns for storing quest data.
- Provides a concrete target for Flywheel's generalized quest tooling.
- Shares the same CI and documentation style as Flywheel for frictionless contributions.
- Maintains a structured outage catalog under `/outages` so fixes propagate across repositories.

## Quick start

Clone both repositories side by side to share prompts, automation patterns, and
testing utilities. DSPACE maintains its own quest scaffolding scripts, so refer
to that repository when you need to author new quests.

Future iterations will focus on reusable quest infrastructure inside Flywheel
rather than shipping DSPACE-specific generators here.

## Repository boundary

The quest JSON paths referenced by DSPACE hardening prompts (for example,
`frontend/src/pages/quests/json/*` and `docs/qa/v3.md`) do not exist in this
repository. If a task requires editing those files, perform the work in a
checked-out clone of `democratizedspace/dspace` instead of Flywheel.

## Codex Automation

DSPACE keeps its own automation prompt at
`frontend/src/pages/docs/md/prompts-codex.md`. The prompt instructs Codex to pick
an unchecked item from the September 1, 2025 changelog and fully implement it.
Each run should tackle a different backlog task and then run
`npm run test:pr` to verify code style and all tests. Reviewing this prompt helps
align Flywheel's agents with DSPACE workflows when building shared features.
Flywheel now provides complementary prompts like `prompts/codex/cad.md` and
`prompts/codex/physics.md` for CAD updates and physics docs.
