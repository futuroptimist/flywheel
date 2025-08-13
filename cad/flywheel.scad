// Simple cylindrical flywheel
// Parameters: diameter, height, shaft diameter, and clearance
// Customize $fs for mesh resolution

diameter = 100;        // mm
height = 20;           // mm
shaft_diameter = 10;   // mm
shaft_clearance = 0.2; // mm added to shaft bore
resolution_fs = 0.5;   // mm, surface resolution

// Allow callers to override `$fs` for finer or coarser meshes
module flywheel(d, h, shaft_d, clearance=0, $fs = resolution_fs) {
    difference() {
        cylinder(d=d, h=h);
        translate([0, 0, -1])
            cylinder(d=shaft_d + clearance, h=h + 2);
    }
}

flywheel(diameter, height, shaft_diameter, shaft_clearance);
