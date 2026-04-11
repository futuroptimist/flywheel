# templates/dotfiles/.bashrc — Reusable Git tag helpers.
# Source this file from your ~/.bashrc:
#   source /path/to/flywheel/templates/dotfiles/.bashrc

rmtag() {
  local tag="$1"
  local remote="${2:-origin}"
  if [[ -z "$tag" ]]; then
    echo "usage: rmtag <tag-name> [remote]"
    return 1
  fi

  if git rev-parse -q --verify "refs/tags/$tag" >/dev/null; then
    git tag -d "$tag" || return 1
  fi

  if git ls-remote --exit-code --tags "$remote" "refs/tags/$tag" >/dev/null 2>&1; then
    git push "$remote" --delete "$tag" || return 1
  fi
}

retag() {
  local tag="$1"
  local remote="${2:-origin}"
  if [[ -z "$tag" ]]; then
    echo "usage: retag <tag-name> [remote]"
    return 1
  fi

  rmtag "$tag" "$remote" || return 1
  git tag "$tag" || return 1
  git push "$remote" "$tag" || {
    echo "retag: local tag '$tag' created but push failed — run: git push $remote $tag"
    return 1
  }
}
