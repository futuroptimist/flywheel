// Stand for a flywheel shaft using skateboard bearings
// Parameters can be tweaked for different sizes

bearing_outer_d = 22; // mm (608 bearing)
bearing_thickness = 7; // mm
base_length = 100; // mm
base_width = 40;  // mm
base_thickness = 8; // mm
post_thickness = 10; // mm
post_height = 40; // mm (distance from base to bearing center)

module bearing_post(thk, width, height, base_thk, bore_d) {
    difference() {
        cube([thk, width, height + bore_d/2 + base_thk], center=false);
        translate([thk/2, width/2, height + base_thk])
            rotate([90,0,0])
                cylinder(r=bore_d/2, h=thk+2, $fs=0.5);
    }
}

module stand(base_len, base_w, base_thk, post_thk, post_h, bore_d) {
    // base platform
    cube([base_len, base_w, base_thk], center=false);
    // left post
    translate([0,0,0])
        bearing_post(post_thk, base_w, post_h, base_thk, bore_d);
    // right post
    translate([base_len - post_thk, 0, 0])
        bearing_post(post_thk, base_w, post_h, base_thk, bore_d);
}

stand(base_length, base_width, base_thickness, post_thickness, post_height, bearing_outer_d);
