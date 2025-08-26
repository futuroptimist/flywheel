from pathlib import Path

import pytest

from flywheel.fit import parse_scad_vars


def test_parse_scad_vars_errors_on_overflow(tmp_path: Path) -> None:
    scad = tmp_path / "overflow.scad"
    scad.write_text("x = 1e309;")
    with pytest.raises(ValueError):
        parse_scad_vars(scad)
