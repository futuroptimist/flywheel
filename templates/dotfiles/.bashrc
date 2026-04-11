rmtag() {
  local tag="$1"
  if [[ -z "$tag" ]]; then
    echo "usage: rmtag <tag-name>"
    return 1
  fi

  git tag -d "$tag" &&
  git push origin --delete "$tag"
}

retag() {
  local tag="$1"
  if [[ -z "$tag" ]]; then
    echo "usage: retag <tag-name>"
    return 1
  fi

  rmtag "$tag" &&
  git tag "$tag" &&
  git push origin "$tag"
}
