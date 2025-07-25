#!/usr/bin/env python3
"""Export OBJ models from the SCAD sources used by the webapp."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from webapp.app import ensure_obj_models  # noqa: E402

if __name__ == "__main__":
    ensure_obj_models()
