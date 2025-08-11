import runpy
import types
from pathlib import Path

import flywheel.fit as ff

REPO = Path(__file__).resolve().parents[1]
CAD_DIR = REPO / "cad"
STL_DIR = REPO / "stl"


def test_parse_scad_vars(tmp_path):
    scad = tmp_path / "part.scad"
    scad.write_text("radius = 5;\nheight = 2;")
    vars = ff.parse_scad_vars(scad)
    assert vars == {"radius": 5.0, "height": 2.0}


def test_parse_scad_vars_with_comments_and_negatives(tmp_path):
    scad = tmp_path / "part.scad"
    scad.write_text("radius = 5; // mm\nheight = -2; // depth\n")
    vars = ff.parse_scad_vars(scad)
    assert vars == {"radius": 5.0, "height": -2.0}


def test_parse_scad_vars_ignores_block_comments(tmp_path):
    scad = tmp_path / "part.scad"
    scad.write_text("/*\n radius = 5;\n*/\nheight = 2;")
    vars = ff.parse_scad_vars(scad)
    assert vars == {"height": 2.0}


def test_parse_scad_vars_without_leading_zero(tmp_path):
    scad = tmp_path / "part.scad"
    scad.write_text("radius = .5;")
    vars = ff.parse_scad_vars(scad)
    assert vars == {"radius": 0.5}


def test_parse_scad_vars_scientific_notation(tmp_path):
    scad = tmp_path / "part.scad"
    scad.write_text("radius = 1e-3;")
    vars = ff.parse_scad_vars(scad)
    assert vars == {"radius": 0.001}


def test_parse_scad_vars_trailing_decimal(tmp_path):
    scad = tmp_path / "part.scad"
    scad.write_text("radius = 5.;")
    vars = ff.parse_scad_vars(scad)
    assert vars == {"radius": 5.0}


def test_parse_scad_vars_multiple_per_line(tmp_path):
    scad = tmp_path / "part.scad"
    scad.write_text("radius=5;height=2;")
    vars = ff.parse_scad_vars(scad)
    assert vars == {"radius": 5.0, "height": 2.0}


def test_verify_fit(tmp_path, monkeypatch):
    assert ff.verify_fit(CAD_DIR, STL_DIR)


def test_ensure_obj_models_mock(monkeypatch, tmp_path):
    import shutil
    import subprocess
    import sys

    import webapp.app as webapp_module

    models = tmp_path / "models"
    models.mkdir()
    webapp_module.MODEL_DIR = models
    webapp_module.SCAD_DIR = CAD_DIR

    class DummyMesh:
        def export(self, path, file_type="obj"):
            Path(path).write_text("ok")

    def fake_load(path, file_type=None):
        return DummyMesh()

    def fake_run(cmd, check):
        Path(cmd[2]).write_text("stl")

    monkeypatch.setitem(
        sys.modules,
        "trimesh",
        types.SimpleNamespace(load_mesh=fake_load),
    )
    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setattr(shutil, "which", lambda x: "/usr/bin/openscad")

    webapp_module.ensure_obj_models()
    scad_names = [p.stem for p in CAD_DIR.glob("*.scad")]
    obj_names = [p.stem for p in models.glob("*.obj")]
    assert set(scad_names) <= set(obj_names)


def test_ensure_obj_models_no_openscad(monkeypatch, tmp_path):
    import shutil

    import webapp.app as webapp_module

    webapp_module.MODEL_DIR = tmp_path / "models"
    webapp_module.SCAD_DIR = CAD_DIR
    monkeypatch.setattr(shutil, "which", lambda x: None)
    webapp_module.ensure_obj_models()
    assert list(webapp_module.MODEL_DIR.glob("*.obj")) == []


def test_ensure_obj_models_exception(monkeypatch, tmp_path):
    import shutil
    import subprocess

    import webapp.app as webapp_module

    webapp_module.MODEL_DIR = tmp_path / "models"
    webapp_module.SCAD_DIR = CAD_DIR
    monkeypatch.setattr(shutil, "which", lambda x: "/usr/bin/openscad")

    def fail_run(cmd, check):
        raise RuntimeError("boom")

    monkeypatch.setattr(subprocess, "run", fail_run)
    webapp_module.ensure_obj_models()
    assert list(webapp_module.MODEL_DIR.glob("*.obj")) == []


def test_models_route(tmp_path):
    from webapp import app as webapp_module

    webapp_module.MODEL_DIR = tmp_path
    f = tmp_path / "dummy.obj"
    f.write_text("ok")
    client = webapp_module.app.test_client()
    resp = client.get(f"/models/{f.name}")
    assert resp.status_code == 200


def test_main_entry(monkeypatch):
    called = {}

    def fake_run(self, debug, port):
        called["port"] = port

    monkeypatch.setattr("flask.app.Flask.run", fake_run)
    runpy.run_module("webapp.app", run_name="__main__")
    assert called.get("port") == 42165


def test_fit_module_main(monkeypatch):
    import sys
    from io import StringIO

    buf = StringIO()
    monkeypatch.setattr(sys, "stdout", buf)
    runpy.run_module("flywheel.fit", run_name="__main__")
    assert "All parts fit together." in buf.getvalue()
