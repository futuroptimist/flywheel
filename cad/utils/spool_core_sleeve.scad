/*
//--------------------------------------------------------------
//  Core‑Sleeve Spool Adapter  ✧  v1.1  (CC0‑1.0 / public domain)
//  Library module for parametric spool-core sleeves.
//  Example usage:
//      use <../utils/spool_core_sleeve.scad>;
//      spool_core_sleeve(inner_id=55, target_od=63, target_od_end=64,
//                        length=60, clearance=0.20);
//
//  Parameters:
//    inner_id   — measured bore ID (mm), e.g. 55 (≈AMS axle)
//    target_od      — outer diameter at z=0 (mm), e.g. 63 (Sunlu spool)
//    target_od_end  — outer diameter at z=length (mm); defaults to target_od
//    length         — axial length (mm), e.g. 60
//    clearance  — extra diameter added to bore (total), default 0.20
//    $fn_outer  — circle resolution for outer cylinder
//    $fn_inner  — circle resolution for inner bore
//
//  Notes:
//  • "clearance" is applied to the *diameter* of the bore (2× radial).
//  • Echoes computed wall thickness so test scripts can sanity-check values.
//--------------------------------------------------------------
*/

module spool_core_sleeve(
    inner_id      = 55,
    target_od     = 63,
    target_od_end = undef,
    length        = 60,
    clearance     = 0.20,
    $fn_outer     = 200,
    $fn_inner     = 150
) {
    target_od_end = is_undef(target_od_end) ? target_od : target_od_end;

    // Basic parameter validation
    assert(
        min(target_od, target_od_end) > inner_id + 2 * clearance,
        str("invalid dims: outer diameters (", target_od, ", ", target_od_end,
            ") must exceed inner_id + 2*clearance (",
            inner_id + 2 * clearance, ")")
    );

    wall_start = (target_od - inner_id) / 2;
    wall_end   = (target_od_end - inner_id) / 2;
    echo(str("Radial wall thickness: ", wall_start, " mm -> ",
             wall_end, " mm"));

    difference() {
        // OUTER – linearly interpolate between diameters
        cylinder(d1 = target_od, d2 = target_od_end, h = length, $fn = $fn_outer);
        // BORE — extended ±1mm to avoid z-fusing
        translate([0, 0, -1])
            cylinder(
                d = inner_id + 2 * clearance, h = length + 2, $fn = $fn_inner
            );
    }
}

// Optional named presets (extend as you collect measurements)
function _spool_core_sleeve_preset(preset) =
    (preset == "sunlu55_to63_len60") ? [55, 63, 64, 60, 0.20] :
    (preset == "sunlu55_to63cyl_len60") ? [55, 63, 63, 60, 0.20] :
    undef;

module spool_core_sleeve_preset(
    preset = "sunlu55_to63_len60", $fn_outer = 200, $fn_inner = 150
) {
    p = _spool_core_sleeve_preset(preset);
    assert(p != undef, str("unknown preset: ", preset));
    spool_core_sleeve(
        inner_id      = p[0],
        target_od     = p[1],
        target_od_end = p[2],
        length        = p[3],
        clearance     = p[4],
        $fn_outer     = $fn_outer,
        $fn_inner     = $fn_inner
    );
}

// End of library
