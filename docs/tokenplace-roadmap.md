# token.place Integration Roadmap

This document outlines a future vision for packaging **flywheel** as an npm module that leverages [token.place](https://token.place) for LLM inference. The goal is to provide a plug‑and‑play API that can be added to developer environments with minimal setup.

## Goals

- Distribute flywheel as an easily installable npm package
- Use token.place as the backend for LLM calls
- Provide optional Python bindings via a PyPI package

## Architecture Overview

```
+-------------+         +----------------+        +----------------+
| Developer   |  npm    | flywheel pkg   |  HTTPS | token.place    |
| environment +-------->+ (API layer)    +------->+ LLM backend    |
+-------------+         +----------------+        +----------------+
```

1. The developer installs the package via `npm install --save-dev @yourorg/flywheel`.
2. API calls from the package are routed to token.place for inference.

## Key Features

- **Cross-language support**: deliver the same functionality via a companion PyPI package using a small Node.js wrapper.

## Roadmap

1. **Prototype npm package**
   - Implement a basic wrapper that forwards prompts to token.place.
   - Include minimal configuration (e.g., custom endpoint, timeout).
2. **Publish alpha on npm**
   - Use scoped package name (e.g., `@yourorg/flywheel`).
   - Gather early feedback from internal users.
3. **Python compatibility**
   - Bundle the Node.js package with a Python wheel via `node-wasm` or a simple `subprocess` bridge.
   - Provide a `requirements-dev.txt` entry for painless setup.

## Acceptance Criteria

- The package installs with `npm install` without additional setup.
- Requests successfully hit token.place and return LLM responses.
- Documentation clearly explains usage in both JS and Python projects.

For details on misuse detection and DoS protections, see [token.place features](tokenplace-features.md).
