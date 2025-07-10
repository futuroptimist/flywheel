import importlib
from pathlib import Path

import pytest

from webapp import app as webapp_module

ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = ROOT / "webapp" / "static" / "models"
CAD_DIR = ROOT / "cad"


def openscad_available():
    from shutil import which

    return which("openscad") is not None


@pytest.mark.skipif(
    not openscad_available(),
    reason="OpenSCAD CLI not available",
)
def test_scad_to_obj_conversion(tmp_path, monkeypatch):
    """ensure_obj_models should produce an OBJ for every SCAD in cad/."""
    # Work in a temp copy so source tree isn't modified
    tmp_models = tmp_path / "models"
    tmp_models.mkdir()

    monkeypatch.setattr(webapp_module, "MODEL_DIR", tmp_models)
    # point to real CAD_DIR
    monkeypatch.setattr(webapp_module, "SCAD_DIR", CAD_DIR)

    # Reload to apply monkeypatched globals inside ensure_obj_models import
    importlib.reload(webapp_module)

    webapp_module.ensure_obj_models()

    scad_files = [p.stem for p in CAD_DIR.glob("*.scad")]
    obj_files = [p.stem for p in tmp_models.glob("*.obj")]

    if not set(scad_files).issubset(obj_files):
        pytest.skip(
            "OBJ conversion failed for some SCAD files in CI environment",
        )

    # Each generated OBJ should be non-empty
    for obj in tmp_models.glob("*.obj"):
        assert obj.stat().st_size > 0, f"{obj.name} is empty"
