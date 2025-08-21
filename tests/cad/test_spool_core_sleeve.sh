#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Render a known-good preset and check echo'd wall thickness
PRESET="sunlu55_to62_len60"
bash "${REPO_ROOT}/scripts/openscad_render_spool_core_sleeve.sh" || true
PRESET="${PRESET}" bash "${REPO_ROOT}/scripts/openscad_render_spool_core_sleeve.sh"

LOG="${REPO_ROOT}/stl/spool_core_sleeve/${PRESET}.log"
STL="${REPO_ROOT}/stl/spool_core_sleeve/${PRESET}.stl"

[[ -s "${STL}" ]] || { echo "FAIL: STL missing"; exit 1; }

# Expect wall thickness = (62-55)/2 = 3.5 mm (allow simple string match)
grep -E 'Radial wall thickness: +3\.5(.0+)? +mm' "${LOG}" >/dev/null \
    || { echo "FAIL: unexpected wall thickness (see ${LOG})"; exit 1; }

echo "All checks passed."
