#!/usr/bin/env bash
set -euo pipefail

# Render a spool sleeve STL from parameters.
# Usage: scripts/openscad_render_spool_core_sleeve.sh ID OD LEN TOL
# Outputs to stl/spool_core_sleeve/<name>.stl and logs echo to a .log file.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

OUT_DIR="${REPO_ROOT}/stl/spool_core_sleeve"
mkdir -p "${OUT_DIR}"

SCAD="${REPO_ROOT}/cad/utils/spool_core_sleeve.scad"

if [[ $# -ne 4 ]]; then
    echo "Usage: $0 ID OD LEN TOL"
    exit 2
fi

ID="$1"
OD="$2"
LEN="$3"
TOL="$4"

NAME="id${ID}_od${OD}_len${LEN}_tol${TOL}"
DEFINE=(-D "ID=${ID}" -D "OD=${OD}" -D "LEN=${LEN}" -D "TOL=${TOL}")

OUT_STL="${OUT_DIR}/${NAME}.stl"
OUT_LOG="${OUT_DIR}/${NAME}.log"

echo "[openscad] rendering ${OUT_STL}"

# Use xvfb-run in CI; locally plain openscad is fine if GUI is installed.
if command -v xvfb-run >/dev/null 2>&1; then
    xvfb-run -a openscad -o "${OUT_STL}" "${DEFINE[@]}" "${SCAD}" 2>&1 | tee "${OUT_LOG}"
else
    openscad -o "${OUT_STL}" "${DEFINE[@]}" "${SCAD}" 2>&1 | tee "${OUT_LOG}"
fi

# Basic sanity: file exists & nontrivial
[[ -s "${OUT_STL}" ]] || { echo "ERROR: STL not created"; exit 1; }
echo "[ok] wrote $(du -h "${OUT_STL}" | awk '{print $1}')"
