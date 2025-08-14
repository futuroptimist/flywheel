# Contributing

Thank you for helping improve **flywheel**!

## Setup

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv pip install pre-commit
pre-commit install
```

Run all checks before committing:

```bash
pre-commit run --all-files
```

## Pull Requests

- Add tests for new functionality when possible.
- Update documentation in `README.md` or `docs/` as needed.
- Ensure `.obj` model files end with a newline so pre-commit passes.
- By submitting a PR you agree to license your work under the MIT license.
- Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).
