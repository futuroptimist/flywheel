from pathlib import Path

import pytest

from flywheel.fit import parse_scad_vars


def test_parse_scad_vars_errors_on_non_finite(tmp_path: Path) -> None:
    scad = tmp_path / "big.scad"
    scad.write_text("radius = 1e5000;")
    with pytest.raises(ValueError):
        parse_scad_vars(scad)
