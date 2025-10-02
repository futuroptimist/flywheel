#!/usr/bin/env bash
set -e
if [ $# -ne 2 ]; then
  echo "Usage: $0 <owner> <repo>"
  exit 1
fi
OWNER=$1
REPO=$2
find . -type f \( -name '*.md' -o -name '*.yml' -o -name '*.yaml' -o -name '*.js' -o -name '*.py' \) -exec sed -i "s/__OWNER__/$OWNER/g; s/__REPO__/$REPO/g" {} +

LOCAL_DIR=".local"
mkdir -p "$LOCAL_DIR"

README_TEMPLATE="$LOCAL_DIR/README.md"
if [ ! -f "$README_TEMPLATE" ]; then
  cat <<'EOF' > "$README_TEMPLATE"
# Local overrides

This directory stores personal development settings such as API tokens,
editor preferences, and experimental configuration files. Copy
`settings.env.example` to `settings.env`, update the values, and keep the
custom file out of version control.

Values placed here are ignored by git so you can iterate safely without
sharing secrets.
EOF
fi

ENV_TEMPLATE="$LOCAL_DIR/settings.env.example"
if [ ! -f "$ENV_TEMPLATE" ]; then
  cat <<'EOF' > "$ENV_TEMPLATE"
# Example environment variables for local development.
# Copy this file to `.local/settings.env` and customize the values.

# export OPENAI_API_KEY=""
# export ANTHROPIC_API_KEY=""
EOF
fi

if [ -f ".gitignore" ]; then
  if ! grep -qxF ".local/" .gitignore; then
    printf "\n.local/\n" >> .gitignore
  fi
else
  printf ".local/\n" > .gitignore
fi

echo "\u2705 flywheel initialized for $OWNER/$REPO"
