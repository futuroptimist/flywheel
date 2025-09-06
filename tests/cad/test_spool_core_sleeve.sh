#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

cases=(
  "55.5 63.0 58 0.20 3.55"
  "55.5 73.0 59 0.20 8.55"
)

for c in "${cases[@]}"; do
  read -r ID OD LEN TOL EXPECT <<<"$c"
  bash "${REPO_ROOT}/scripts/openscad_render_spool_core_sleeve.sh" "$ID" "$OD" "$LEN" "$TOL"
  NAME="id${ID}_od${OD}_len${LEN}_tol${TOL}"
  LOG="${REPO_ROOT}/stl/spool_core_sleeve/${NAME}.log"
  STL="${REPO_ROOT}/stl/spool_core_sleeve/${NAME}.stl"
  [[ -s "${STL}" ]] || { echo "FAIL: STL missing for ${NAME}"; exit 1; }
  grep -E "Nominal wall: ${EXPECT}" "${LOG}" >/dev/null \
    || { echo "FAIL: unexpected wall thickness (see ${LOG})"; exit 1; }
done

echo "All checks passed."
