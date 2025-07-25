#!/usr/bin/env python3
"""Export OBJ models from the SCAD sources used by the webapp."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # noqa: E402

from webapp.app import ensure_obj_models  # noqa: E402

if __name__ == "__main__":
    ensure_obj_models()
