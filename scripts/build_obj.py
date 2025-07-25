#!/usr/bin/env python3
"""Export OBJ models from the SCAD sources used by the webapp."""
from webapp.app import ensure_obj_models

if __name__ == "__main__":
    ensure_obj_models()
