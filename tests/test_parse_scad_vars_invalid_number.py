from pathlib import Path

import pytest

from flywheel.fit import parse_scad_vars


def test_parse_scad_vars_errors_on_invalid_number(tmp_path: Path) -> None:
    scad = tmp_path / "bad.scad"
    scad.write_text("x = 1abc;")
    with pytest.raises(ValueError):
        parse_scad_vars(scad)
