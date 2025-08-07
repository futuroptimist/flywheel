// Simple cylindrical flywheel
// Parameters: diameter, height, and shaft diameter
// Customize $fs for resolution

diameter = 100;    // mm
height = 20;       // mm
shaft_diameter = 10;  // mm

module flywheel(d, h, shaft_d) {
    difference() {
        cylinder(d=d, h=h, $fs=0.5);
        translate([0, 0, -1])
            cylinder(d=shaft_d, h=h+2, $fs=0.5);
    }
}

flywheel(diameter, height, shaft_diameter);
