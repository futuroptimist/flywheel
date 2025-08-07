from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Tuple

import trimesh

_DEF_RE = re.compile(
    r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+))"
    r"\s*;(?:\s*//.*)?$"
)


def parse_scad_vars(path: Path) -> Dict[str, float]:
    """Return variable assignments parsed from a SCAD file.

    Inline ``//`` comments after the semicolon are ignored. The parser supports
    negative values, decimals without a leading zero, and numbers ending with a
    trailing decimal point.
    """
    vars: Dict[str, float] = {}
    for line in Path(path).read_text().splitlines():
        m = _DEF_RE.match(line.strip())
        if m:
            vars[m.group(1)] = float(m.group(2))
    return vars


def _dims(stl_path: Path) -> Tuple[float, float, float]:
    """Return (x, y, z) dimensions of the STL mesh."""
    mesh = trimesh.load_mesh(stl_path)
    bounds = mesh.bounds
    diff = bounds[1] - bounds[0]
    return float(diff[0]), float(diff[1]), float(diff[2])


def verify_fit(
    scad_dir: Path = Path("cad"),
    stl_dir: Path = Path("stl"),
) -> bool:
    """Check that CAD parameters align across parts and match exported STLs."""
    adapter = parse_scad_vars(scad_dir / "adapter.scad")
    shaft = parse_scad_vars(scad_dir / "shaft.scad")
    wheel = parse_scad_vars(scad_dir / "flywheel.scad")
    stand = parse_scad_vars(scad_dir / "stand.scad")

    # Basic parameter relationships
    assert shaft["shaft_diameter"] == adapter["shaft_diameter"]
    assert wheel["shaft_diameter"] >= shaft["shaft_diameter"]
    assert stand["bearing_outer_d"] > shaft["shaft_diameter"]

    tol = 0.1

    shaft_dims = _dims(stl_dir / "shaft.stl")
    assert abs(shaft_dims[2] - shaft["shaft_length"]) < tol
    assert any(abs(d - shaft["shaft_diameter"]) < tol for d in shaft_dims[:2])

    wheel_dims = _dims(stl_dir / "flywheel.stl")
    assert abs(wheel_dims[0] - 2 * wheel["radius"]) < 1.0
    assert abs(wheel_dims[2] - wheel["height"]) < tol

    adapter_dims = _dims(stl_dir / "adapter.stl")
    assert abs(adapter_dims[0] - adapter["outer_diameter"]) < 1.0
    assert abs(adapter_dims[2] - adapter["length"]) < tol

    stand_dims = _dims(stl_dir / "stand.stl")
    expected_z = (
        stand["post_height"]
        + stand["base_thickness"]
        + stand["bearing_outer_d"] / 2  # noqa: E501
    )
    assert abs(stand_dims[0] - stand["base_length"]) < tol
    assert abs(stand_dims[1] - stand["base_width"]) < tol
    assert abs(stand_dims[2] - expected_z) < 1.0

    return True


if __name__ == "__main__":
    verify_fit()
    print("All parts fit together.")
