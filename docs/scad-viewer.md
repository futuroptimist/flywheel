# Web-based SCAD Viewer

This demo exposes the CAD models in `cad/` as OBJ files rendered with Three.js.
A lightweight Flask server hosts the viewer.

## User journey

1. Run `./scripts/export_scad_to_obj.py` to generate OBJ files.
2. Start the server: `python web/app.py`.
3. Open `http://localhost:5000` and select a model.
4. Rotate the camera by dragging with the mouse.
5. Zoom using the scroll wheel.
6. Pick other models from the dropdown.

The same workflow will be mirrored in downstream repos such as DSPACE and Sigma.
