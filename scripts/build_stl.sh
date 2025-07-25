#!/usr/bin/env bash
set -euo pipefail

SCAD_DIR="${SCAD_DIR:-hardware/cad}"
STL_DIR="${STL_DIR:-hardware/stl}"

mkdir -p "$STL_DIR"

while IFS= read -r -d '' scad; do
  rel="${scad#$SCAD_DIR/}"
  stl="$STL_DIR/${rel%.scad}.stl"
  mkdir -p "$(dirname "$stl")"
  if [ -f "$stl" ] && [ "$stl" -nt "$scad" ]; then
    echo "[INFO] Skipping $scad; STL up to date"
    continue
  fi
  echo "[INFO] Exporting $scad -> $stl"
  openscad -o "$stl" "$scad"
done < <(find "$SCAD_DIR" -name '*.scad' -print0)
