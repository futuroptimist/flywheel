"""Helpers to convert OpenSCAD files to OBJ format."""

from __future__ import annotations

import subprocess
from pathlib import Path


def export_obj(scad_path: Path, obj_path: Path) -> None:
    """Run OpenSCAD to export ``scad_path`` to ``obj_path``."""
    cmd = ["openscad", "-o", str(obj_path), str(scad_path)]
    subprocess.run(cmd, check=True)
