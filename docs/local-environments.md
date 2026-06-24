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

## Reusing Git shell helpers

Flywheel keeps reusable, repo-versioned shell snippets in
`templates/dotfiles/.bashrc`. This template is the canonical place for common
Git shell helpers that can be copied into a local shell config or sourced from
a checkout of the repository:

```bash
source /path/to/flywheel/templates/dotfiles/.bashrc
```

The helpers accept an optional remote name and default to `origin`:

```bash
rmtag <tag> [remote]
retag <tag> [remote]
pokeci <branch-name> [remote]
```

Use `rmtag` to remove a tag locally and remotely when it exists, and `retag` to
replace a tag at the current `HEAD` before pushing it. Use `pokeci` to create an
empty `poke CI` commit on a remote branch. `pokeci` fetches the selected remote
branch into a temporary detached worktree, commits there, pushes back to the
same remote branch, and removes the temporary worktree afterward, so it does not
switch your current checkout or disturb local changes.
