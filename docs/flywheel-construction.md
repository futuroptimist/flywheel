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

1. Adjust `diameter`, `height`, and `shaft_diameter` in the SCAD file as needed.
   Inline `//` or block `/* ... */` comments are ignored by the CAD parser.
2. Export to STL and slice with your preferred software.
3. If using wood or metal, replicate the dimensions and center bore.

## Assembly

- Use a shaft that matches `shaft_diameter`.
- Ensure the wheel is firmly fixed to avoid wobble.
- Consider adding washers or bearings for smooth rotation.

## Mass, inertia, and energy

Let `diameter`, `shaft_diameter`, and `height` be the parameters in
[`cad/flywheel.scad`](../cad/flywheel.scad). The outer and inner radii are
$r_o = \tfrac{\text{diameter}}{2}$ and $r_i = \tfrac{\text{shaft\_diameter}}{2}$.
For material density $\rho$ the wheel's mass and moment of inertia are

$$m = \rho \pi (r_o^2 - r_i^2) h$$
$$I = \tfrac{1}{2} m (r_o^2 + r_i^2)$$

Spinning at angular speed $\omega$ stores

$$E = \tfrac{1}{2} I \omega^2$$

Using the default dimensions (`diameter = 100`, `shaft_diameter = 10`,
`height = 20`) and PLA ($\rho \approx 1.25\,\text{g/cm}^3$) yields
$m \approx 0.19\,\text{kg}$ and $I \approx 2.5\times10^{-4}\,\text{kg·m}^2$.
At 3000\,rpm ($\omega \approx 314\,\text{rad/s}$) the wheel holds about
12\,J of kinetic energy. See [Flywheel Physics](flywheel-physics.md)
for derivations.

This general approach lets you experiment with different materials while
keeping the overall design consistent.

For a refresher on the math, see [Flywheel Physics](flywheel-physics.md).
For a printable stand and shaft that use skateboard bearings, see
[Flywheel Stand](flywheel-stand.md).

For a removable clamp to attach the wheel, see [Flywheel Clamp Adapter](flywheel-adapter.md).
