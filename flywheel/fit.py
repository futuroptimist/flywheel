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
    shaft_diameter = shaft["shaft_diameter"]
    adapter_diameter = adapter["shaft_diameter"]
    if shaft_diameter != adapter_diameter:
        delta = adapter_diameter - shaft_diameter
        raise AssertionError(
            (
                "adapter shaft_diameter {adapter:.3f} mm does not match "
                "shaft {shaft:.3f} mm (Δ {delta:+.3f} mm)"
            ).format(
                adapter=adapter_diameter,
                shaft=shaft_diameter,
                delta=delta,
            )
        )
    wheel_shaft = wheel["shaft_diameter"]
    if wheel_shaft < shaft_diameter:
        delta = wheel_shaft - shaft_diameter
        raise AssertionError(
            (
                "flywheel shaft_diameter {wheel:.3f} mm is smaller than "
                "shaft {shaft:.3f} mm (Δ {delta:+.3f} mm)"
            ).format(
                wheel=wheel_shaft,
                shaft=shaft_diameter,
                delta=delta,
            )
        )
    bearing_outer = stand["bearing_outer_d"]
    if bearing_outer <= shaft_diameter:
        delta = bearing_outer - shaft_diameter
        raise AssertionError(
            (
                "stand bearing_outer_d {outer:.3f} mm must exceed "
                "shaft {shaft:.3f} mm (Δ {delta:+.3f} mm)"
            ).format(
                outer=bearing_outer,
                shaft=shaft_diameter,
                delta=delta,
            )
        )

    loose_tol = tol * LOOSE_TOL_MULTIPLIER

    shaft_dims = _dims(stl_dir / "shaft.stl")
    shaft_length = shaft["shaft_length"]
    shaft_len_delta = shaft_dims[2] - shaft_length
    if abs(shaft_len_delta) >= tol:
        raise AssertionError(
            (
                "shaft.stl length off by {delta:.3f} mm "
                "(expected {exp:.3f}, got {got:.3f}, tol {tol:.3f})"
            ).format(
                delta=shaft_len_delta,
                exp=shaft_length,
                got=shaft_dims[2],
                tol=tol,
            )
        )
    shaft_delta = max(abs(dim - shaft_diameter) for dim in shaft_dims[:2])
    if shaft_delta >= tol:
        raise AssertionError(
            (
                "shaft.stl diameter mismatch {delta:.3f} mm exceeds tol "
                "{tol:.3f} (target {target:.3f})"
            ).format(delta=shaft_delta, tol=tol, target=shaft_diameter)
        )

    wheel_dims = _dims(stl_dir / "flywheel.stl")
    wheel_diameter = wheel["diameter"]
    wheel_delta = max(abs(dim - wheel_diameter) for dim in wheel_dims[:2])
    if wheel_delta >= loose_tol:
        raise AssertionError(
            (
                "flywheel.stl diameter mismatch {delta:.3f} mm exceeds tol "
                "{tol:.3f} (target {target:.3f})"
            ).format(delta=wheel_delta, tol=loose_tol, target=wheel_diameter)
        )
    wheel_height = wheel["height"]
    wheel_height_delta = wheel_dims[2] - wheel_height
    if abs(wheel_height_delta) >= tol:
        raise AssertionError(
            (
                "flywheel.stl height off by {delta:.3f} mm "
                "(expected {exp:.3f}, got {got:.3f}, tol {tol:.3f})"
            ).format(
                delta=wheel_height_delta,
                exp=wheel_height,
                got=wheel_dims[2],
                tol=tol,
            )
        )

    adapter_dims = _dims(stl_dir / "adapter.stl")
    adapter_outer = adapter["outer_diameter"]
    adapter_delta = max(abs(dim - adapter_outer) for dim in adapter_dims[:2])
    if adapter_delta >= loose_tol:
        raise AssertionError(
            (
                "adapter.stl outer diameter mismatch {delta:.3f} mm "
                "exceeds tol {tol:.3f} (target {target:.3f})"
            ).format(delta=adapter_delta, tol=loose_tol, target=adapter_outer)
        )
    adapter_length = adapter["length"]
    adapter_len_delta = adapter_dims[2] - adapter_length
    if abs(adapter_len_delta) >= tol:
        raise AssertionError(
            (
                "adapter.stl length off by {delta:.3f} mm "
                "(expected {exp:.3f}, got {got:.3f}, tol {tol:.3f})"
            ).format(
                delta=adapter_len_delta,
                exp=adapter_length,
                got=adapter_dims[2],
                tol=tol,
            )
        )

    stand_dims = _dims(stl_dir / "stand.stl")
    expected_z = (
        stand["post_height"]
        + stand["base_thickness"]
        + stand["bearing_outer_d"] / 2  # noqa: E501
    )
    base_length = stand["base_length"]
    base_len_delta = stand_dims[0] - base_length
    if abs(base_len_delta) >= tol:
        raise AssertionError(
            (
                "stand.stl base length off by {delta:.3f} mm "
                "(expected {exp:.3f}, got {got:.3f}, tol {tol:.3f})"
            ).format(
                delta=base_len_delta,
                exp=base_length,
                got=stand_dims[0],
                tol=tol,
            )
        )
    base_width = stand["base_width"]
    base_width_delta = stand_dims[1] - base_width
    if abs(base_width_delta) >= tol:
        raise AssertionError(
            (
                "stand.stl base width off by {delta:.3f} mm "
                "(expected {exp:.3f}, got {got:.3f}, tol {tol:.3f})"
            ).format(
                delta=base_width_delta,
                exp=base_width,
                got=stand_dims[1],
                tol=tol,
            )
        )
    stand_height_delta = stand_dims[2] - expected_z
    if abs(stand_height_delta) >= loose_tol:
        raise AssertionError(
            (
                "stand.stl height off by {delta:.3f} mm "
                "(expected {exp:.3f}, got {got:.3f}, tol {tol:.3f})"
            ).format(
                delta=stand_height_delta,
                exp=expected_z,
                got=stand_dims[2],
                tol=loose_tol,
            )
        )

    return True


if __name__ == "__main__":
    verify_fit()
    print("All parts fit together.")
