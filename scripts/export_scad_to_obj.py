#!/usr/bin/env python
"""Export all SCAD models under ./cad/ to OBJ files."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import meshio

CAD_DIR = Path("cad")
OUT_DIR = Path("web/static/models")


def convert(scad: Path) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".stl") as tmp:
        subprocess.run(
            [
                "openscad",
                "-o",
                tmp.name,
                str(scad),
            ],
            check=True,
        )
        mesh = meshio.read(tmp.name)
        obj_path = OUT_DIR / f"{scad.stem}.obj"
        meshio.write(obj_path, mesh, file_format="obj")
        print(f"exported {obj_path}")


def main() -> None:
    for scad in CAD_DIR.glob("*.scad"):
        convert(scad)


if __name__ == "__main__":
    main()
