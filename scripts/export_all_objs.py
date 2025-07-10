#!/usr/bin/env python
"""Export all SCAD files in ``cad/`` to OBJ."""
from pathlib import Path

from flywheel.export_obj import export_obj


def main() -> None:
    cad_dir = Path("cad")
    for scad_path in cad_dir.glob("*.scad"):
        obj_path = cad_dir / f"{scad_path.stem}.obj"
        export_obj(scad_path, obj_path)


if __name__ == "__main__":
    main()
