// Simple shaft for the flywheel stand
// Sized to fit standard 608 skateboard bearings

shaft_diameter = 8;   // mm
shaft_length = 150;   // mm

module shaft(shaft_d, shaft_len) {
    cylinder(r = shaft_d / 2, h = shaft_len, $fs = 0.5);
}

shaft(shaft_diameter, shaft_length);
