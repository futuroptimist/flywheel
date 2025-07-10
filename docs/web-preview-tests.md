# Web Preview Tests

This document records typical interactions with the OBJ viewer and how they are
exercised in automated tests.

## User experiences

- **Rotate** – drag with the left mouse button or touch to orbit around the model.
- **Zoom** – scroll the mouse wheel or pinch on touch devices.
- **Reset** – press `r` or double-click to restore the default view.

## Automated checks

The `tests/test_playwright_ui.py` suite uses Playwright with the Chromium
browser to mimic these actions. The GitHub Actions test workflow installs the
browser and runs these tests alongside the rest of the Python suite.
