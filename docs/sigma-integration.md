# Integrating with Sigma

[Sigma](https://github.com/futuroptimist/sigma) is an open-source ESP32 "AI pin" that lets you interact with language models using push‑to‑talk voice commands. It combines speech recognition, text-to-speech and a 3D‑printed enclosure.

## Why Sigma Matters

- Highlights how Flywheel's tooling can power hardware projects.
- Demonstrates LLM integration on constrained devices using the same docs and agent patterns.
- Provides a testbed for voice-driven prompts that may feed back into Flywheel.

## Quick start

Build the firmware and explore the helper scripts:

```bash
git clone https://github.com/futuroptimist/sigma
cd sigma
pio run
```

Future commits may sync the `llms.txt` configuration and AGENT docs between both projects to keep the experience consistent.
