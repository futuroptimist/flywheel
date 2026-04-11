# token.place Integration PRD

This document expands on the roadmap for distributing **flywheel** as a package that uses [token.place](https://token.place) for LLM inference. The goal is a frictionless developer experience with minimal configuration.

## Objectives

- Offer an npm package, `@yourorg/flywheel`, that forwards API calls to token.place.
- Avoid auth requirements by relying on token.place's open protocol and DoS mitigation.
- Provide Python bindings through a companion PyPI package.

## Proposed Architecture

```
+---------------+          npm            +----------------+         HTTPS         +-----------------+
| Developer environment | ---------------------> | flywheel pkg   | ---------------------> | token.place API |
| (JS or Python)| <--------------------- | (API wrapper)  | <--------------------- |  inference node |
+---------------+   LLM responses        +----------------+         results        +-----------------+
```

1. Developers install the package via `npm install --save-dev @yourorg/flywheel`.
2. The wrapper sends prompts to token.place using a configurable endpoint.
3. Python projects depend on a small Node.js shim published to PyPI.

## Key Features

- **Zero-key setup**: no API keys or secrets required.
- **Cross‑platform**: works on macOS, Linux, Windows, and via Docker.
- **Misuse detection**: monitoring and rate limiting built into token.place, see [tokenplace-features](tokenplace-features.md).

## Milestones

```
[M1 Prototype] -> [M2 Alpha npm release] -> [M3 Python bindings] -> [M4 Stable 1.0]
```

- **M1 Prototype**: basic npm wrapper, manual deployment.
- **M2 Alpha**: publish scoped package for feedback.
- **M3 Python**: ship `node-wasm` or `subprocess` bridge in PyPI package.
- **M4 Stable**: finalize docs and security guidelines.

## Acceptance Criteria

- `npm install @yourorg/flywheel` works without extra setup.
- Example scripts demonstrate LLM calls in JS and Python.
- Documentation references mitigation techniques for abuse.
