# Core‑Sleeve Spool Adapter (OpenSCAD utility module)

A tiny, reusable OpenSCAD module for adapting filament spools: it slides into the
spool’s bore (`inner_id`) and expands the wall to desired outer diameters
(`target_od` → `target_od_end`) over the full spool width (`length`). It echoes
computed wall thickness so CI can
sanity‑check builds.

## Quick start

```scad
use "../utils/spool_core_sleeve.scad";

// direct parameters
spool_core_sleeve(inner_id=55, target_od=63, target_od_end=64,
                  length=60, clearance=0.20);

// or via named preset
spool_core_sleeve_preset("sunlu55_to63_len60");

// straight 63 mm cylinder (works as a wedge removal tool)
spool_core_sleeve_preset("sunlu55_to63cyl_len60");
```

### Parameters

| Name        | Type | Default | Notes                               |
|-------------|------|---------|-------------------------------------|
| `inner_id`      | mm   | 55      | Measured bore (ID) of the spool     |
| `target_od`     | mm   | 63      | Sleeve OD at z=0                    |
| `target_od_end` | mm   | 63      | Sleeve OD at z=length               |
| `length`        | mm   | 60      | Axial length (match spool width)    |
| `clearance`     | mm   | 0.20    | Added to diameter of bore (total)   |
| `$fn_outer` | —    | 200     | Facets for outer cylinder           |
| `$fn_inner` | —    | 150     | Facets for inner bore               |

Tip: If a print is too tight or loose, re‑export with a slightly different
clearance (e.g., 0.15–0.30).

## Rendering from the command line

Example (Linux/macOS):

```bash
openscad -o stl/spool_core_sleeve/sunlu55_to63_len60.stl \
  -D INNER_ID=55 -D TARGET_OD=63 -D TARGET_OD_END=64 \
  -D LENGTH=60 -D CLEARANCE=0.20 \
  cad/examples/spool_core_sleeve_example.scad
```

Or with the preset shortcut:

```bash
openscad -o stl/spool_core_sleeve/sunlu55_to63_len60.stl \
  -D PRESET="sunlu55_to63_len60" \
  cad/examples/spool_core_sleeve_example.scad
```

## Ready-to-print files

Two preset SCAD files live in `cad/spool_core_sleeve/` with matching STLs in
`stl/spool_core_sleeve/`. The tapered adapter (`sunlu55_to63_len60`) expands from
63 mm to 64 mm, while the straight cylinder (`sunlu55_to63cyl_len60`) serves as a
wedge-removal tool so the adapter can be reused across many spools.


## Printing notes

Print on its side (axis horizontal) for stronger hoop strength; or vertical for
best circularity—choose per application.

0.2–0.28 mm layer height is typical; 3+ perimeters; PETG or tough PLA works well.

Test fit first; adjust clearance as needed and re‑export.

License: CC0‑1.0 (public domain).
