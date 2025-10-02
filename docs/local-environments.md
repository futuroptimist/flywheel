# Local Environment Configuration

Flywheel can scaffold a `.local` directory that stores personal settings such as API keys or editor preferences. Anything in this folder is git‑ignored so each contributor can keep private customizations while sharing the rest of the repo.

To generate it, run:

```bash
./scripts/setup.sh YOURNAME YOURREPO
```

The script creates a `.local` folder with two starter files:

- `.local/README.md` — explains how to use the directory for personal overrides.
- `.local/settings.env.example` — sample environment variables you can copy to `.local/settings.env` and customize.

If `.gitignore` is missing the entry, the script appends `.local/` so anything you add stays out of version control. You can extend these files for other projects without affecting the shared repository.

This keeps personal energy flowing into your workflow without leaking private information.
