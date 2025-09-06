# Spool Core Sleeves

These OpenSCAD presets adapt common filament spools to the Bambu Lab AMS and AMS Lite.
They wrap the AMS hub (55 mm or 55.5 mm) and expand to the measured spool diameter.

## Naming convention

`<brand><ID>_to<OD>[cyl]_len<length>.scad`

- `<brand>` – spool brand (e.g., `sunlu`, `bambu`)
- `<ID>` – inner bore diameter; `55p5` denotes 55.5 mm for AMS Lite
- `<OD>` – starting outer diameter of the sleeve
- `cyl` – optional straight cylinder used to push out a tapered sleeve
- `len<length>` – axial length of the part in millimeters

## Available presets

| File | Description |
|------|-------------|
| `sunlu55_to63_len60.scad` | 63→64 mm tapered adapter |
| `sunlu55_to63cyl_len60.scad` | straight 63 mm removal cylinder |
| `sunlu55_to73_len60.scad` | 73→74 mm tapered adapter |
| `sunlu55_to73cyl_len60.scad` | straight 73 mm removal cylinder |
| `bambu55p5_to63_len58.scad` | 63 mm sleeve for AMS Lite |
| `bambu55p5_to73_len59.scad` | 73 mm sleeve for AMS Lite |
