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

Use the prompt sync report to compare Flywheel's prompts with sugarkube's copy and
identify anything to port over:

```bash
python -m flywheel.promptsync --target-repo futuroptimist/sugarkube
```

The command reads `docs/prompt-docs-summary.md` and prints the prompts missing from
either repository so you can open a PR downstream.
