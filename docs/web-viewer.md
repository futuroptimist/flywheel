# Web-based CAD Viewer

This repo includes a tiny Flask application that renders OBJ models generated from the SCAD files in `cad/`.

A GitHub Actions workflow converts the SCAD files to OBJ using `openscad` and
commits the results to `webapp/static/models/` when it runs on the `main`
branch. Another scheduled workflow generates nightly STL exports and commits
them to `stl/`. GitHub renders `.stl` files with a built‑in 3D viewer so you can
inspect the geometry right in the browser.

To regenerate the OBJ assets locally, export fresh STLs with `openscad` and
convert them using the [`assimp`](https://github.com/assimp/assimp) command-line
utility. This will emit `.obj` files along with matching `.mtl` material files:

```bash
openscad -o stl/stand.stl cad/stand.scad
assimp export stl/stand.stl webapp/static/models/stand.obj
```

Flywheel's conversion helper also writes a neutral material definition to the
`.mtl` file and updates the `.obj` header with `mtllib`/`usemtl` directives so
the Three.js loader renders models with consistent shading.

## Running Locally

Ensure Node.js 20 or newer is installed. Then run:

```bash
uv pip install -r requirements.txt
npm ci
npm run playwright:install
python webapp/app.py
```

The development server listens on port 5000 by default, matching Flask's
standard quickstart URL. Set ``FLYWHEEL_WEBAPP_PORT`` to override it, for
example ``FLYWHEEL_WEBAPP_PORT=8123 python webapp/app.py``. Visit
[http://localhost:5000](http://localhost:5000) (or your chosen port) and select
a model. Drag the mouse to rotate and scroll to zoom.

## Three.js Demo

Open `viewer/threejs.html` directly in your browser to spin the STL-based flywheel. The script uses the Three.js `STLLoader` and adds simple animated spheres as ball bearings.

## User Journeys

- **Rotate:** left-click and drag on the canvas. The viewer captures the pointer while
  the button is held so rotations stay smooth even if the cursor leaves the canvas.
- **Zoom:** scroll your mouse wheel to move the camera in and out with gentle limits to
  avoid clipping through the model.
- **Switch models:** use the dropdown above the viewer to load a different OBJ file.
