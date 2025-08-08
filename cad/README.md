# CAD Models

Source OpenSCAD files for the flywheel project.

## Available models

- `stand.scad` – stand for a flywheel shaft using 608 bearings
- `shaft.scad` – straight shaft sized for 608 bearings
- `adapter.scad` – clamp adapter that attaches the flywheel to the shaft
- `flywheel.scad` – simple cylindrical flywheel with center bore

## Regenerating meshes

Rebuild STL outputs and OBJ viewer models whenever a SCAD file changes:

```bash
scripts/build_stl.sh
python - <<'PY'
from webapp.app import ensure_obj_models
ensure_obj_models()
PY
python -m flywheel.fit
```
