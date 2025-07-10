# Web Preview

This repo includes a small Flask app that loads OBJ files in a Three.js scene.
OBJ models are generated from the SCAD sources in `cad/` via the
`export_obj` GitHub Actions workflow.

Run the demo locally:

```bash
uv pip install flask
python web/app.py
```

Then open <http://localhost:5000> to view the sample model.

## Interactions

The viewer supports basic camera controls powered by Three.js `OrbitControls`:

1. **Rotate** – drag with the left mouse button or a single finger on touch devices.
2. **Zoom** – use the mouse wheel or pinch gesture to zoom in and out.
3. **Reset** – double‑click anywhere in the viewer to return to the initial view.

Playwright tests in `tests/playwright/` exercise these actions using the Chromium browser.
