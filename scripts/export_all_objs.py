#!/usr/bin/env python
"""Export all SCAD files in ``cad/`` to OBJ."""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from flywheel.export_obj import export_obj  # noqa: E402


def main() -> None:
    cad_dir = Path("cad")
    for scad_path in cad_dir.glob("*.scad"):
        obj_path = cad_dir / f"{scad_path.stem}.obj"
        export_obj(scad_path, obj_path)


if __name__ == "__main__":
    main()
