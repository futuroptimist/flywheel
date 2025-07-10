# Web-based CAD Viewer

This repo includes a tiny Flask application that renders OBJ models generated from the SCAD files in `cad/`.

A GitHub Actions workflow automatically converts the SCAD files to OBJ using `openscad` and commits them to `webapp/static/models/`.
Another workflow runs nightly to export the same SCAD sources to `stl/`. GitHub
renders `.stl` files with a built‑in 3D viewer so you can quickly inspect the
geometry right in the browser.

## Running Locally

```bash
uv pip install -r requirements.txt
npm install
npx playwright install
python webapp/app.py
```

Visit [http://localhost:5000](http://localhost:5000) and select a model. Drag the mouse to rotate and scroll to zoom.

## User Journeys

- **Rotate:** left-click and drag on the canvas.
- **Zoom:** scroll your mouse wheel.
- **Switch models:** use the dropdown above the viewer to load a different OBJ file.
