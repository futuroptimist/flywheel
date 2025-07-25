# Flywheel Clamp Adapter

This part locks the flywheel to the shaft using a split-collar design so you can remove or swap the wheel without tools that damage the shaft.

## Materials
- **PETG or nylon** – strong and slightly flexible for the adapter body.
- **M4 bolts and nuts** – two for clamping and two or more to attach the wheel.

The geometry lives in `hardware/cad/adapter.scad` and can be tweaked for different shaft sizes or bolt diameters.

## Printing
1. Adjust the SCAD parameters if needed, then export to STL.
2. Print at least 50% infill for durability.

## Assembly
1. Insert the clamp bolts through the side holes.
2. Slide the adapter onto the shaft.
3. Fasten the flywheel to the radial holes or directly through the adapter.
4. Tighten the clamp bolts until the wheel no longer slips.

The clamp can be loosened and retightened many times, making experimentation easy.

For a breakdown of the forces acting on this part and how to size materials, see [Flywheel Physics](flywheel-physics.md).
