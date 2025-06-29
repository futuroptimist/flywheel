#!/usr/bin/env bash
set -e
if [ $# -ne 2 ]; then
  echo "Usage: $0 <owner> <repo>"
  exit 1
fi
OWNER=$1
REPO=$2
find . -type f \( -name '*.md' -o -name '*.yml' -o -name '*.yaml' -o -name '*.js' -o -name '*.py' \) -exec sed -i "s/__OWNER__/$OWNER/g; s/__REPO__/$REPO/g" {} +
echo "\u2705 flywheel initialized for $OWNER/$REPO"
