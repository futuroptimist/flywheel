#!/usr/bin/env bash
# Helper functions for interactive AI shells

command_not_found_handle() {
  printf "Command '%s' not found in %s.\n" "$1" "$PWD"
  local suggestion
  if type compgen >/dev/null 2>&1; then
    suggestion=$(compgen -c "$1" | head -n 1)
  elif type whence >/dev/null 2>&1; then
    suggestion=$(whence -p "$1" 2>/dev/null | head -n 1)
  fi
  if [ -n "$suggestion" ]; then
    echo "Did you mean '$suggestion'?"
  fi
  return 127
}

command_not_found_handler() {
  command_not_found_handle "$@"
}

flw_pwd_hint() {
  local p="$PWD"
  if [ ${#p} -le 60 ]; then
    echo "$p"
  else
    echo "...${p: -57}"
  fi
}
