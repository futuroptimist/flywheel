# Web UI Playwright Tests

The SCAD preview exposes simple camera controls implemented with Three.js `OrbitControls`.
These tests verify the core interactions in Chromium using Playwright.

## Scenarios

1. **Rotate**: drag with the left mouse button or touch to orbit the camera.
2. **Zoom**: scroll the mouse wheel or pinch to zoom the view in and out.
3. **Reset**: double-click to return the model to its initial orientation and distance.

Playwright scripts exercise these scenarios in `tests/playwright/`.
