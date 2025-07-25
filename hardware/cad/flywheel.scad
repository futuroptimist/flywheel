// Simple cylindrical flywheel
// Parameters: radius, height, and shaft diameter
// Customize $fs for resolution

radius = 50;    // mm
height = 20;    // mm
shaft_diameter = 10;  // mm

module flywheel(r, h, shaft_d) {
    difference() {
        cylinder(r=r, h=h, $fs=0.5);
        translate([0,0,-1])
            cylinder(r=shaft_d/2, h=h+2, $fs=0.5);
    }
}

flywheel(radius, height, shaft_diameter);
