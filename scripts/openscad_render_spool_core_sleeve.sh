#!/usr/bin/env bash
set -euo pipefail

# Render a spool sleeve STL from parameters or a named PRESET.
# Usage examples:
#   scripts/openscad_render_spool_core_sleeve.sh 55 63 64 60 0.20
#   scripts/openscad_render_spool_core_sleeve.sh 55 63 60 0.20  # end defaults to 63
#   PRESET=sunlu55_to63_len60 scripts/openscad_render_spool_core_sleeve.sh
#   PRESET=sunlu55_to73_len60 scripts/openscad_render_spool_core_sleeve.sh
# Outputs to stl/spool_core_sleeve/<name>.stl and logs echo to a .log file.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

OUT_DIR="${REPO_ROOT}/stl/spool_core_sleeve"
mkdir -p "${OUT_DIR}"

EX_SCAD="${REPO_ROOT}/cad/examples/spool_core_sleeve_example.scad"

if [[ "${PRESET:-}" != "" ]]; then
    NAME="${PRESET}"
    DEFINE=(-D "PRESET=\"${PRESET}\"")
else
    if [[ $# -lt 4 ]]; then
        echo "Usage: $0 INNER_ID TARGET_OD [TARGET_OD_END] LENGTH CLEARANCE"
        echo " or: PRESET=name $0"
        exit 2
    fi
    INNER_ID="$1"
    TARGET_OD="$2"
    if [[ $# -ge 5 ]]; then
        TARGET_OD_END="$3"
        LENGTH="$4"
        CLEARANCE="$5"
    else
        TARGET_OD_END="$2"
        LENGTH="$3"
        CLEARANCE="$4"
    fi
    NAME="id${INNER_ID}_od${TARGET_OD}to${TARGET_OD_END}_len${LENGTH}_clr${CLEARANCE}"
    DEFINE=(-D "INNER_ID=${INNER_ID}" -D "TARGET_OD=${TARGET_OD}" \
        -D "TARGET_OD_END=${TARGET_OD_END}" -D "LENGTH=${LENGTH}" \
        -D "CLEARANCE=${CLEARANCE}")
fi

OUT_STL="${OUT_DIR}/${NAME}.stl"
OUT_LOG="${OUT_DIR}/${NAME}.log"

echo "[openscad] rendering ${OUT_STL}"

# Use xvfb-run in CI; locally plain openscad is fine if GUI is installed.
if command -v xvfb-run >/dev/null 2>&1; then
    xvfb-run -a openscad -o "${OUT_STL}" "${DEFINE[@]}" "${EX_SCAD}" 2>&1 | tee "${OUT_LOG}"
else
    openscad -o "${OUT_STL}" "${DEFINE[@]}" "${EX_SCAD}" 2>&1 | tee "${OUT_LOG}"
fi

# Basic sanity: file exists & nontrivial
[[ -s "${OUT_STL}" ]] || { echo "ERROR: STL not created"; exit 1; }
echo "[ok] wrote $(du -h "${OUT_STL}" | awk '{print $1}')"
