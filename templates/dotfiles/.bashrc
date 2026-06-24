# Reusable Git helpers.
# Copy this file into your local shell config or source it from your shell rc file:
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
    echo "retag: local tag '$tag' created but push failed; run: git push $remote $tag"
    return 1
  }
}

pokeci() {
  local branch="$1"
  local remote="${2:-origin}"

  if [[ -z "$branch" ]]; then
    echo "usage: pokeci <branch-name> [remote]"
    return 1
  fi

  if ! git check-ref-format --branch "$branch" >/dev/null 2>&1; then
    echo "pokeci: invalid branch name: $branch"
    return 1
  fi

  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "pokeci: not inside a git repository"
    return 1
  fi

  local repo_root tmpdir exit_code poke_commit
  repo_root="$(git rev-parse --show-toplevel)" || return 1

  if ! git -C "$repo_root" ls-remote --exit-code --heads "$remote" "${branch}" >/dev/null; then
    echo "pokeci: remote branch '$branch' not found on '$remote'"
    return 1
  fi

  tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/pokeci.XXXXXX")" || return 1

  git -C "$repo_root" fetch "$remote" "+refs/heads/${branch}:refs/remotes/${remote}/${branch}" &&
  git -C "$repo_root" worktree add --detach "$tmpdir" "refs/remotes/${remote}/${branch}" &&
  git -C "$tmpdir" commit --allow-empty -m "poke CI" &&
  poke_commit="$(git -C "$tmpdir" rev-parse HEAD)" &&
  git -C "$repo_root" push "$remote" "${poke_commit}:refs/heads/${branch}"

  exit_code=$?

  git -C "$repo_root" worktree remove --force "$tmpdir" >/dev/null 2>&1 || rm -rf "$tmpdir"

  return "$exit_code"
}
