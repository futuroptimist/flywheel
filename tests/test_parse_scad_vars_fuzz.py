from __future__ import annotations

import random
import string
from pathlib import Path

import pytest

from flywheel.fit import parse_scad_vars


def _random_invalid_assignment() -> str:
    letters = string.ascii_letters
    value = "".join(random.choice(letters) for _ in range(5))
    return f"x = {value};"


def test_parse_scad_vars_rejects_invalid_assignments(tmp_path: Path) -> None:
    random.seed(0)
    scad = tmp_path / "bad.scad"
    for _ in range(10):
        scad.write_text(_random_invalid_assignment())
        with pytest.raises(ValueError):
            parse_scad_vars(scad)
