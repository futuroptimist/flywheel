# Futuroptimist Synergy

[futuroptimist/futuroptimist](https://github.com/futuroptimist/futuroptimist) hosts video scripts, helper utilities and a complete test suite for a solarpunk YouTube channel. The project documents its automation in `AGENTS.md` and `llms.txt` and provides a 3‑D heat‑map generator to visualise activity over time.

This guide summarises key lessons Flywheel can borrow and outlines a potential improvement for the Futuroptimist repo itself.

## Lessons for Flywheel

- **Structured metadata** – Every video script lives in a dated folder with a `metadata.json` file validated by JSON Schema. This keeps the project searchable and enables automated checks.
- **Orientation files** – `AGENTS.md` and a short `llms.txt` describe tone and layout so LLMs stay consistent. Flywheel adopters could generate a similar pair after running `./scripts/setup.sh`.
- **Automation helpers** – The Makefile sets up virtualenvs, fetches subtitles and scaffolds script folders. Tests enforce cross‑platform behaviour with 100% coverage.
- **High coverage mindset** – The test suite validates helper scripts and schema with 100% coverage, ensuring new utilities remain reliable.
- **Runbook & instructions** – A dedicated `RUNBOOK.md` walks through ideation, filming, editing and publishing. `INSTRUCTIONS.md` handles local setup. Keeping these distinct avoids cluttering the README.

## Recommendation for Futuroptimist

Futuroptimist already automates several tasks via the Makefile and nightly workflows. A dedicated Python CLI could unify these helpers under a single command:

```bash
futuroptimist init               # scaffold scripts from video_ids.txt
futuroptimist heatmap            # rebuild the 3-D contribution chart
futuroptimist subtitles VIDEO_ID # fetch subtitles into ./subtitles
```

Packaging the CLI would make cross‑platform usage easier (mirroring `flywheel`'s own CLI) and allow other repos to reuse pieces like the heat‑map generator. The existing scripts could be refactored into a module (e.g. `futuroptimist.cli`) and tested alongside the current utilities.

To keep orientation tasks consistent, Futuroptimist could also expose a small wrapper around `flywheel prompt`. This would read the local `README` and `AGENTS` guides and return tips tailored to video script contributions. Finally, converting `RUNBOOK.md` to a machine‑readable `runbook.yml` would let both repositories share automated checklists.
