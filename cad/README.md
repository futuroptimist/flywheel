# CAD Models

Source OpenSCAD files for the flywheel project.

## Prerequisites

Install the OpenSCAD command-line tools before exporting meshes, for example:

```bash
sudo apt-get install openscad
```

## Available models

- `stand.scad` – stand for a flywheel shaft using 608 bearings; post thickness
  derives from the bearing width and the base is 6 mm thick by default to save material
- `shaft.scad` – straight shaft sized for 608 bearings (exposes `shaft()` module for easy
  customization; override `$fs` via the `resolution_fs` variable for finer meshes)
- `adapter.scad` – clamp adapter that attaches the flywheel to the shaft with configurable
  bore clearance
- `flywheel.scad` – cylindrical flywheel with center bore and optional shaft clearance
  (override `$fs` via the `resolution_fs` variable for finer meshes)
- `utils/spool_core_sleeve.scad` – parametric spool core sleeve library
  (see `examples/spool_core_sleeve_example.scad`; a pre-generated
  `sunlu55_to62_len60` sleeve lives in `stl/spool_core_sleeve/`)
- `examples/spool_core_sleeve_example.scad` – demo spool core sleeve; the
  corresponding OBJ lives in `webapp/static/models/examples/` and the
  pre-generated sleeve's OBJ is at
  `webapp/static/models/spool_core_sleeve/sunlu55_to62_len60.obj`

## Regenerating meshes

Rebuild STL outputs and OBJ viewer models whenever a SCAD file changes. Library
modules in `cad/utils/` are skipped because they don't render standalone parts:

```bash
scripts/build_stl.sh
python - <<'PY'
from webapp.app import ensure_obj_models
ensure_obj_models()
PY
python -m flywheel.fit
```

Use `scripts/openscad_render_spool_core_sleeve.sh` with a `PRESET` to export
parametric spool core sleeves, for example:

```bash
PRESET=sunlu55_to62_len60 scripts/openscad_render_spool_core_sleeve.sh
```

## Validation

Run `python -m flywheel.fit` after regenerating meshes to verify that all parts
still fit together.
