# Local Environment Configuration

Flywheel can scaffold a `.local` directory that stores personal settings such as API keys or editor preferences. Anything in this folder is git‑ignored so each contributor can keep private customisations while sharing the rest of the repo.

To generate it, run:

```bash
./scripts/setup.sh YOURNAME YOURREPO
```

The script creates a `.local` folder and adds typical config templates. You can extend these files for other projects without affecting version control.

This keeps personal energy flowing into your workflow without leaking private information.
