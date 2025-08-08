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

## Running Locally

```bash
uv pip install -r requirements.txt
npm install
npx playwright install
python webapp/app.py
```

Visit [http://localhost:5000](http://localhost:5000) and select a model. Drag the mouse to rotate and scroll to zoom.

## Three.js Demo

Open `viewer/threejs.html` directly in your browser to spin the STL-based flywheel. The script uses the Three.js `STLLoader` and adds simple animated spheres as ball bearings.

## User Journeys

- **Rotate:** left-click and drag on the canvas.
- **Zoom:** scroll your mouse wheel.
- **Switch models:** use the dropdown above the viewer to load a different OBJ file.
