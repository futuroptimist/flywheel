from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Dict, Tuple

import trimesh

LOOSE_TOL_MULTIPLIER = 6.0

_DEF_RE = re.compile(
    r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*"
    r"([-+]?(?:\d(?:_?\d)*(?:\.(?:\d(?:_?\d)*)?)?|\.\d(?:_?\d)*)"
    r"(?:[eE][-+]?\d(?:_?\d)*)?)\s*"
    r";(?:\s*//.*)?$"
)


def parse_scad_vars(path: str | Path) -> Dict[str, float]:
    """Return variable assignments parsed from a SCAD file.

    Args:
        path: String or :class:`~pathlib.Path` pointing to the SCAD file.

    Block comments ``/* ... */`` and inline ``//`` comments after the
    semicolon are ignored. The parser strips an initial UTF-8 BOM and
    supports negative values, decimals without a leading zero, trailing
    decimal points, scientific notation, underscore digit separators, and
    multiple assignments on the same line. Raises :class:`ValueError` when a
    variable assignment lacks a numeric value, has an empty right-hand side,
    or omits a terminating semicolon, or exceeds floating-point range.
    """
    path = Path(path)
    text = path.read_text()
    text = text.lstrip("\ufeff")  # Handle UTF-8 BOM
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    vars: Dict[str, float] = {}
    for raw_line in text.splitlines():
        line = raw_line.split("//", 1)[0]
        stripped = line.strip()
        if (
            stripped
            and re.match(r"[a-zA-Z_][a-zA-Z0-9_]*\s*=", stripped)
            and not stripped.endswith(";")
        ):
            raise ValueError(f"missing semicolon: {stripped}")
        for part in line.split(";"):
            part = part.strip()
            if not part:
                continue
            m = _DEF_RE.match(part + ";")
            if m:
                num = m.group(2).replace("_", "")
                value = float(num)
                if not math.isfinite(value):
                    raise ValueError(f"invalid number for {m.group(1)}: {num}")
                vars[m.group(1)] = value
            elif re.match(
                r"[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*" r"[a-zA-Z_][a-zA-Z0-9_]*\s*$",
                part,
            ):
                raise ValueError(f"invalid assignment: {part}")
            elif re.match(r"[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*$", part):
                name = part.split("=", 1)[0].strip()
                raise ValueError(f"missing value for {name}")
            elif re.match(
                r"[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[-+]?(?:\d|\.)",
                part,
            ):
                raise ValueError(f"invalid assignment: {part}")
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
    tol: float = 0.1,
) -> bool:
    """Check that CAD parameters align across parts and match exported STLs.

    Args:
        scad_dir: Directory containing the source ``.scad`` files.
        stl_dir: Directory containing the exported ``.stl`` meshes.
        tol: Maximum allowed deviation when comparing dimensions in
            millimeters. Defaults to ``0.1``. Larger diameters and heights use
            ``tol`` scaled by ``LOOSE_TOL_MULTIPLIER`` to account for mesh
            tessellation while still shrinking or expanding with the supplied
            tolerance.
    """
    adapter = parse_scad_vars(scad_dir / "adapter.scad")
    shaft = parse_scad_vars(scad_dir / "shaft.scad")
    wheel = parse_scad_vars(scad_dir / "flywheel.scad")
    stand = parse_scad_vars(scad_dir / "stand.scad")

    # Basic parameter relationships
    assert shaft["shaft_diameter"] == adapter["shaft_diameter"]
    assert wheel["shaft_diameter"] >= shaft["shaft_diameter"]
    assert stand["bearing_outer_d"] > shaft["shaft_diameter"]

    loose_tol = tol * LOOSE_TOL_MULTIPLIER

    shaft_dims = _dims(stl_dir / "shaft.stl")
    assert abs(shaft_dims[2] - shaft["shaft_length"]) < tol
    shaft_diameter = shaft["shaft_diameter"]
    shaft_delta = max(abs(dim - shaft_diameter) for dim in shaft_dims[:2])
    assert shaft_delta < tol

    wheel_dims = _dims(stl_dir / "flywheel.stl")
    wheel_diameter = wheel["diameter"]
    wheel_delta = max(abs(dim - wheel_diameter) for dim in wheel_dims[:2])
    assert wheel_delta < loose_tol
    assert abs(wheel_dims[2] - wheel["height"]) < tol

    adapter_dims = _dims(stl_dir / "adapter.stl")
    adapter_outer = adapter["outer_diameter"]
    adapter_delta = max(abs(dim - adapter_outer) for dim in adapter_dims[:2])
    assert adapter_delta < loose_tol
    assert abs(adapter_dims[2] - adapter["length"]) < tol

    stand_dims = _dims(stl_dir / "stand.stl")
    expected_z = (
        stand["post_height"]
        + stand["base_thickness"]
        + stand["bearing_outer_d"] / 2  # noqa: E501
    )
    assert abs(stand_dims[0] - stand["base_length"]) < tol
    assert abs(stand_dims[1] - stand["base_width"]) < tol
    assert abs(stand_dims[2] - expected_z) < loose_tol

    return True


if __name__ == "__main__":
    verify_fit()
    print("All parts fit together.")
