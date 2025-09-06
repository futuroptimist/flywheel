//
// Spool Core Sleeve (AMS Lite compatible) — anti–z‑fighting edition
// SPDX-License-Identifier: MIT
// Units: mm
//
// Public interface (back‑compat with CI):
//   -D ID=... -D OD=... -D LEN=... -D TOL=...
// Optional: -D TOL_ID=..., -D TOL_OD=..., -D mode="ring" -D RING_H=10, -D SEGMENTS=160
//

// -------------------- User Parameters (override with -D) --------------------
ID      = 55.5;   // Inner diameter to fit AMS Lite spindle (53–58 mm window)
OD      = 63.0;   // Outer diameter to match YOUR spool hub hole
LEN     = 58.0;   // Overall length (57–60 mm typical for 1 kg spools)

TOL     = 0.00;   // Global radial tol: + on ID (looser on spindle), - on OD (looser in hub)
TOL_ID  = is_undef(TOL_ID) ? TOL : TOL_ID;
TOL_OD  = is_undef(TOL_OD) ? TOL : TOL_OD;

OUTER_CH = 0.8;   // Outer 45° chamfer height (and radial)
INNER_CH = 0.6;   // Inner 45° chamfer height (and radial)

MIN_WALL = 2.4;   // Warn if wall gets thinner than this

// Optional features
split_sleeve = false;  // Add a narrow axial slit for a light press fit
SLIT_GAP     = 0.60;   // Slit width if enabled
slot_count   = 0;      // Lightening slots (0 = off)

// Resolution
$fn = is_undef(SEGMENTS) ? 160 : SEGMENTS;

// Quick iteration
mode   = is_undef(mode) ? "full" : mode; // "full" or "ring"
RING_H = is_undef(RING_H) ? 10 : RING_H;

// -------------------- Preview-only epsilons --------------------
// Eliminate OpenCSG z-fighting in Preview by ensuring overlaps.
// In final Render (F6/CGAL), these collapse to zero and do not change geometry.
EPS_R = $preview ? 0.05 : 0.0;   // radial epsilon
EPS_Z = $preview ? 0.10 : 0.0;   // axial epsilon

// -------------------- Derived values --------------------
ID_EFF = ID + TOL_ID;
OD_EFF = OD - TOL_OD;

function clamp(x, a, b) = x < a ? a : (x > b ? b : x);
function ch_outer(h) = clamp(OUTER_CH, 0, h/2 - 0.01);
function ch_inner(h) = clamp(INNER_CH, 0, h/2 - 0.01);

// Sanity echoes
echo("---- Spool Core Sleeve ----");
echo(str("ID (effective): ", ID_EFF, " mm"));
echo(str("OD (effective): ", OD_EFF, " mm"));
echo(str("LEN: ", LEN, " mm"));
echo(str("Nominal wall: ", (OD_EFF - ID_EFF)/2, " mm"));
if ( (OD_EFF - ID_EFF)/2 < MIN_WALL )
    echo("WARNING: Wall thinner than MIN_WALL; consider increasing OD or decreasing ID.");

// -------------------- Geometry helpers --------------------
module outer_profile(od, h, oc) {
    r = od/2;
    oc_ = ch_outer(h);
    union() {
        translate([0,0,oc_]) cylinder(h = h - 2*oc_, r = r);
        if (oc_ > 0) cylinder(h = oc_, r1 = r - oc_, r2 = r);
        if (oc_ > 0) translate([0,0,h-oc_]) cylinder(h = oc_, r1 = r, r2 = r - oc_);
    }
}

module inner_profile(id, h, ic) {
    // Subtractive core with preview-only oversizing to avoid coplanar faces.
    r = id/2;
    ic_ = ch_inner(h);
    union() {
        // Center tube: stretch by ±EPS_Z axially, enlarge by EPS_R radially
        translate([0,0,max(ic_ - EPS_Z, 0)])
            cylinder(h = (h - 2*ic_) + 2*EPS_Z, r = r + EPS_R);
        // Bottom chamfer: extend slightly below zero during preview
        if (ic_ > 0)
            translate([0,0,-EPS_Z])
                cylinder(h = ic_ + EPS_Z, r1 = r + EPS_R, r2 = r + ic_ + EPS_R);
        // Top chamfer: extend slightly beyond h during preview
        if (ic_ > 0)
            translate([0,0,h - ic_])
                cylinder(h = ic_ + EPS_Z, r1 = r + ic_ + EPS_R, r2 = r + EPS_R);
    }
}

module axial_slit(od, h, gap, extra=0.6) {
    // Remove a narrow axial slot to allow slight compression
    translate([0,0,h/2])
        cube([od + 2*extra, gap, h + 2*extra], center = true);
}

module weight_slots(od, id, h, count=6, slot_w=8, keep_margin=1.2) {
    if (count > 0) {
        r_mid = (od + id)/4;
        radial_len = (od - id)/2 - keep_margin;
        for (i = [0:count-1]) {
            rotate([0,0, i*360/count])
                translate([r_mid, 0, h/2])
                    cube([slot_w, radial_len, h*0.6], center = true);
        }
    }
}

module sleeve(od, id, h) {
    difference() {
        outer_profile(od, h, OUTER_CH);
        inner_profile(id, h, INNER_CH); // subtractor overlaps by EPS_* in preview
        if (split_sleeve) axial_slit(od, h, SLIT_GAP);
        if (slot_count > 0) weight_slots(od, id, h, count=slot_count);
    }
}

// -------------------- Render --------------------
final_h = (mode == "ring") ? RING_H : LEN;
sleeve(OD_EFF, ID_EFF, final_h);
