// Simple shaft for the flywheel stand
// Sized to fit standard 608 skateboard bearings

shaft_diameter = 8;   // mm
shaft_length = 150;   // mm
resolution_fs = 0.5;  // mm, surface resolution

// Allow callers to override `$fs` for finer or coarser meshes
module shaft(shaft_d, shaft_len, $fs = resolution_fs) {
    cylinder(r = shaft_d / 2, h = shaft_len);
}

shaft(shaft_diameter, shaft_length);
