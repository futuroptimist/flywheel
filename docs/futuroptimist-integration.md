# Futuroptimist Synergy

[futuroptimist/futuroptimist](https://github.com/futuroptimist/futuroptimist) hosts video scripts, helper utilities and a complete test suite for a solarpunk YouTube channel. The repository uses `llms.txt` and `AGENTS.md` to keep AI assistants aligned with its workflow. It also includes a 3‑D heat‑map generator that visualizes lines of code changed per day.

This document collects lessons Flywheel can borrow and suggests improvements for Futuroptimist.

## Lessons for Flywheel

- **Orientation file** – Maintaining a short `llms.txt` alongside `AGENTS.md` helps LLMs understand tone and context. Flywheel adopters should consider adding a similar file after running `./scripts/setup.sh`.
- **Structured metadata** – Each video script lives in a dated folder with a `metadata.json` file validated by JSON Schema.
- **Automation helpers** – The Makefile creates virtualenvs, fetches subtitles and scaffolds new script folders with one command.
- **Cross-platform** – Make targets run on both Unix and Windows.
- **Complete tests** – Futuroptimist's test suite covers helper scripts and schema validation, reaching 100% coverage. New Flywheel templates should encourage high coverage from the start.
- **Runbook & instructions** – A separate `RUNBOOK.md` captures the production checklist, while `INSTRUCTIONS.md` documents setup details. Keeping these distinct avoids cluttering the README.

## Recommendation for Futuroptimist

Futuroptimist already automates several tasks via the Makefile and nightly workflows. A dedicated Python CLI could unify these helpers under a single command and pave the way for additional tooling:

```bash
futuroptimist init               # scaffold scripts from video_ids.txt
futuroptimist heatmap            # rebuild the 3-D contribution chart
futuroptimist subtitles VIDEO_ID # fetch subtitles into ./subtitles
```

Packaging the CLI would make cross‑platform usage easier (mirroring `flywheel`'s own CLI) and allow other repos to reuse pieces like the heat‑map generator. The existing scripts could be refactored into a module (e.g. `futuroptimist.cli`) and tested alongside the current utilities.

Beyond the core commands, a small wrapper around Flywheel's `flywheel prompt` could produce context-aware onboarding tips:

```bash
python -m futuroptimist.prompt  # surfaces # Purpose, # Context and # Request sections
```

Another idea is to convert the Markdown runbook to `runbook.yml`. A `flywheel runbook` subcommand could then parse the YAML and output the same checklist, letting Axel or other tools reason over the steps automatically.
