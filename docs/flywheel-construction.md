# IRL Flywheel Construction

This document explains how to build a physical flywheel using the
`cad/flywheel.scad` design or any similar heavy cylinder. The provided
OpenSCAD file produces a simple hub with a center bore for a shaft.

## Materials

- **PLA or PETG** – 3D print the part at 100% infill for maximum weight.
- **Wood** – cut a circular disk and drill a centered hole.
- **Metal** – machine or repurpose a steel or aluminum cylinder.

Any material works as long as the flywheel remains balanced and securely
mounted to the shaft.

## Printing / Machining

1. Adjust `radius`, `height`, and `shaft_diameter` in the SCAD file as needed.
2. Export to STL and slice with your preferred software.
3. If using wood or metal, replicate the dimensions and center bore.

## Assembly

- Use a shaft that matches `shaft_diameter`.
- Ensure the wheel is firmly fixed to avoid wobble.
- Consider adding washers or bearings for smooth rotation.

This general approach lets you experiment with different materials while
keeping the overall design consistent.

For a refresher on the math, see [Flywheel Physics](flywheel-physics.md).
For a printable stand and shaft that use skateboard bearings, see
[Flywheel Stand](flywheel-stand.md).

For a removable clamp to attach the wheel, see [Flywheel Clamp Adapter](flywheel-adapter.md).
