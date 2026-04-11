# token.place Feature Overview

This document summarizes key capabilities of [token.place](https://token.place) as observed from the upstream repository.

## Core Capabilities

- **End-to-end encryption** using a hybrid RSA/AES scheme ensures prompts and responses remain private.
- **Relay architecture** hides the IP addresses of LLM servers and clients.
- **OpenAI-compatible API** for easy integration with existing tools.
- **Local or remote inference**: run models on your own hardware or interact with remote servers.
- **Cross-platform support** with Docker containerization and platform-specific launch scripts.
- **Minimal logging in production** with environment-aware logging helpers.
- **Security recommendations** in the docs include rate limiting and abuse detection to mitigate DoS attacks.

For implementation details, see the [token.place repository](https://github.com/futuroptimist/token.place).
