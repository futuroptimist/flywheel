# Integrating with f2clipboard

[f2clipboard](https://github.com/futuroptimist/f2clipboard) is a minimal Python utility for copying groups of files into a Markdown snippet. It began as a quick way to collect code for LLM conversations and has grown into a sandbox for building larger automation flows.

## Why f2clipboard Matters

- Demonstrates how small, single-purpose CLIs can evolve using Flywheel's patterns.
- Explores macro-based workflows that may inform future Flywheel agents.
- Shares style guides and CI configuration with this repository.

## Quick start

Clone the tool and run it alongside Flywheel:

```bash
git clone https://github.com/futuroptimist/f2clipboard
cd f2clipboard
pip install -e .
python -m f2clipboard --dir ../flywheel --pattern "*.md"
```

The roadmap for f2clipboard includes integrating Flywheel's agent prompts so that copied snippets come with context-aware instructions.
