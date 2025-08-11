// Clamp adapter to attach the flywheel to a shaft
// Uses a split collar design with two clamp bolts

shaft_diameter = 8; // mm
outer_diameter = 24; // mm
length = 20; // mm
bolt_diameter = 4; // mm
slit_width = 1; // mm
shaft_clearance = 0.2; // mm added to shaft bore

module clamp_adapter(shaft_d, outer_d, len, bolt_d, slit_w, clearance=0) {
    difference() {
        cylinder(d=outer_d, h=len, $fs=0.5);
        cylinder(d=shaft_d + clearance, h=len+0.1, $fs=0.5);
        // clearance for clamp bolt
        translate([outer_d/2 - bolt_d/2, 0, len/2])
            rotate([90,0,0])
                cylinder(d=bolt_d, h=outer_d+2, $fs=0.5);
        // slot for clamping
        translate([outer_d/2, 0, 0])
            cube([slit_w, outer_d, len], center=true);
    }
}

clamp_adapter(
    shaft_diameter,
    outer_diameter,
    length,
    bolt_diameter,
    slit_width,
    shaft_clearance
);
