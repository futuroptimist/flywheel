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

See [web-preview-tests.md](web-preview-tests.md) for expected user interactions
and how they are automated with Playwright.
