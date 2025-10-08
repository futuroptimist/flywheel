# Integrating with sugarkube

[sugarkube](https://github.com/futuroptimist/sugarkube) is an accessible k3s platform targeting Raspberry Pi and similar devices. It bundles off-grid solar and cellular connectivity for outage-resistant web hosting.

## Why sugarkube Matters

- Showcases Flywheel's tooling on infrastructure projects.
- Provides a platform to test LLM agents in remote or offline environments.
- Shares CI configuration and docs with this repository.

## Quick start

Clone the repository and explore the setup scripts:

```bash
git clone https://github.com/futuroptimist/sugarkube
cd sugarkube
# follow the README to provision the cluster
```

## Syncing automation prompts

Keep sugarkube's automation instructions aligned with Flywheel by copying the
canonical prompt doc into the repository:

```bash
flywheel sync-prompts /path/to/sugarkube
```

The command writes `docs/prompts/codex/automation.md` into the target repo and
skips files that are already identical. Run it after updating the automation
prompt so both projects share the same baseline instructions.
