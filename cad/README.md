# CAD Models

Source OpenSCAD files for the flywheel project.

## Available models

- `stand.scad` – stand for a flywheel shaft using 608 bearings
- `shaft.scad` – straight shaft sized for 608 bearings (exposes `shaft()` module for easy
  customization)
- `adapter.scad` – clamp adapter that attaches the flywheel to the shaft
- `flywheel.scad` – simple cylindrical flywheel with center bore
- `utils/spool_core_sleeve.scad` – parametric spool core sleeve library
  (see `examples/spool_core_sleeve_example.scad`)

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
PRESET=sunlu55_to73_len60 scripts/openscad_render_spool_core_sleeve.sh
```
