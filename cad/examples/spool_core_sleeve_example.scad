/*
// This example file lets you render the sleeve from the CLI:
//
//   openscad -o out.stl \
//     -D INNER_ID=55 -D TARGET_OD=62 -D LENGTH=60 -D CLEARANCE=0.20 \
//     cad/examples/spool_core_sleeve_example.scad
//
// or to use a named preset:
//
//   openscad -o out.stl -D PRESET="sunlu55_to62_len60" \
//     cad/examples/spool_core_sleeve_example.scad
*/

use <../utils/spool_core_sleeve.scad>;

// Defaults (overridable via -D)
INNER_ID  = is_undef(INNER_ID)  ? 55   : INNER_ID;
TARGET_OD = is_undef(TARGET_OD) ? 62   : TARGET_OD;
LENGTH    = is_undef(LENGTH)    ? 60   : LENGTH;
CLEARANCE = is_undef(CLEARANCE) ? 0.20 : CLEARANCE;

// If PRESET is provided, it takes precedence
if (!is_undef(PRESET)) {
    spool_core_sleeve_preset(PRESET);
} else {
    spool_core_sleeve(
        inner_id = INNER_ID,
        target_od = TARGET_OD,
        length = LENGTH,
        clearance = CLEARANCE
    );
}
