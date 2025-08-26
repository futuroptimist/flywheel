#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Render known presets and check echo'd wall thicknesses
for PRESET in sunlu55_to63_len60 sunlu55_to63cyl_len60 \
               sunlu55_to73_len60 sunlu55_to73cyl_len60; do
    bash "${REPO_ROOT}/scripts/openscad_render_spool_core_sleeve.sh" || true
    PRESET="${PRESET}" bash "${REPO_ROOT}/scripts/openscad_render_spool_core_sleeve.sh"

    LOG="${REPO_ROOT}/stl/spool_core_sleeve/${PRESET}.log"
    STL="${REPO_ROOT}/stl/spool_core_sleeve/${PRESET}.stl"

    [[ -s "${STL}" ]] || { echo "FAIL: STL missing for ${PRESET}"; exit 1; }

    case "${PRESET}" in
        sunlu55_to63_len60)
            EXPECT='Radial wall thickness: +4(\.0+)? +mm -> +4\.5(\.0+)? +mm'
            ;;
        sunlu55_to63cyl_len60)
            EXPECT='Radial wall thickness: +4(\.0+)? +mm -> +4(\.0+)? +mm'
            ;;
        sunlu55_to73_len60)
            EXPECT='Radial wall thickness: +9(\.0+)? +mm -> +9\.5(\.0+)? +mm'
            ;;
        sunlu55_to73cyl_len60)
            EXPECT='Radial wall thickness: +9(\.0+)? +mm -> +9(\.0+)? +mm'
            ;;
    esac

    grep -E "${EXPECT}" "${LOG}" >/dev/null \
        || { echo "FAIL: unexpected wall thickness (see ${LOG})"; exit 1; }
done

echo "All checks passed."
