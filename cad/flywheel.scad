// Simple cylindrical flywheel
// Parameters: diameter, height, shaft diameter, and clearance
// Customize $fs for resolution

diameter = 100;        // mm
height = 20;           // mm
shaft_diameter = 10;   // mm
shaft_clearance = 0.2; // mm added to shaft bore

module flywheel(d, h, shaft_d, clearance=0) {
    difference() {
        cylinder(d=d, h=h, $fs=0.5);
        translate([0, 0, -1])
            cylinder(d=shaft_d + clearance, h=h+2, $fs=0.5);
    }
}

flywheel(diameter, height, shaft_diameter, shaft_clearance);
