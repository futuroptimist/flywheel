import runpy
import types
from pathlib import Path

import pytest

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


def test_parse_scad_vars_numeric_underscores(tmp_path):
    scad = tmp_path / "part.scad"
    scad.write_text("radius = 1_000.5;")
    vars = ff.parse_scad_vars(scad)
    assert vars == {"radius": 1000.5}


def test_parse_scad_vars_multiple_per_line(tmp_path):
    scad = tmp_path / "part.scad"
    scad.write_text("radius=5;height=2;")
    vars = ff.parse_scad_vars(scad)
    assert vars == {"radius": 5.0, "height": 2.0}


def test_parse_scad_vars_accepts_str_path(tmp_path):
    scad = tmp_path / "part.scad"
    scad.write_text("radius = 5;")
    vars = ff.parse_scad_vars(str(scad))
    assert vars == {"radius": 5.0}


def test_parse_scad_vars_handles_bom(tmp_path):
    scad = tmp_path / "part.scad"
    scad.write_text("radius = 5;\n", encoding="utf-8-sig")
    vars = ff.parse_scad_vars(scad)
    assert vars == {"radius": 5.0}


def test_verify_fit(tmp_path, monkeypatch):
    assert ff.verify_fit(CAD_DIR, STL_DIR)


def test_verify_fit_custom_tol(monkeypatch):
    original = ff._dims

    def bumped(path):
        x, y, z = original(path)
        return x + 0.01, y, z

    monkeypatch.setattr(ff, "_dims", bumped)
    with pytest.raises(AssertionError):
        ff.verify_fit(CAD_DIR, STL_DIR, tol=0.001)


def test_verify_fit_strict_tol_real_models():
    with pytest.raises(AssertionError):
        ff.verify_fit(CAD_DIR, STL_DIR, tol=0.05)


def test_verify_fit_reports_mismatch_details(monkeypatch):
    original = ff._dims

    def skew_shaft(path):
        dims = original(path)
        if path.name == "shaft.stl":
            return dims[0] + 0.2, dims[1], dims[2]
        return dims

    monkeypatch.setattr(ff, "_dims", skew_shaft)
    with pytest.raises(AssertionError) as exc:
        ff.verify_fit(CAD_DIR, STL_DIR, tol=0.05)
    msg = str(exc.value)
    assert "shaft.stl diameter mismatch" in msg
    assert "Δ +0.200 mm" in msg


def test_verify_fit_reports_shaft_length_delta(monkeypatch):
    original = ff._dims

    def stretch_shaft(path):
        dims = original(path)
        if path.name == "shaft.stl":
            return dims[0], dims[1], dims[2] + 0.2
        return dims

    monkeypatch.setattr(ff, "_dims", stretch_shaft)

    with pytest.raises(AssertionError) as exc:
        ff.verify_fit(CAD_DIR, STL_DIR)

    msg = str(exc.value)
    assert "shaft.stl length mismatch" in msg
    assert "Δ +0.200 mm" in msg


def test_verify_fit_reports_wheel_height_delta(monkeypatch):
    original = ff._dims

    def bump_wheel_height(path):
        dims = original(path)
        if path.name == "flywheel.stl":
            return dims[0], dims[1], dims[2] - 0.2
        return dims

    monkeypatch.setattr(ff, "_dims", bump_wheel_height)

    with pytest.raises(AssertionError) as exc:
        ff.verify_fit(CAD_DIR, STL_DIR)

    msg = str(exc.value)
    assert "flywheel.stl height mismatch" in msg
    assert "Δ -0.200 mm" in msg


def test_verify_fit_reports_adapter_outer_delta(monkeypatch):
    original = ff._dims

    def expand_adapter_outer(path):
        dims = original(path)
        if path.name == "adapter.stl":
            return dims[0] + 0.7, dims[1], dims[2]
        return dims

    monkeypatch.setattr(ff, "_dims", expand_adapter_outer)

    with pytest.raises(AssertionError) as exc:
        ff.verify_fit(CAD_DIR, STL_DIR)

    msg = str(exc.value)
    assert "adapter.stl outer diameter mismatch" in msg
    assert "Δ +0.700 mm" in msg


def test_verify_fit_reports_adapter_length_delta(monkeypatch):
    original = ff._dims

    def stretch_adapter(path):
        dims = original(path)
        if path.name == "adapter.stl":
            return dims[0], dims[1], dims[2] + 0.2
        return dims

    monkeypatch.setattr(ff, "_dims", stretch_adapter)

    with pytest.raises(AssertionError) as exc:
        ff.verify_fit(CAD_DIR, STL_DIR)

    msg = str(exc.value)
    assert "adapter.stl length mismatch" in msg
    assert "Δ +0.200 mm" in msg


def test_verify_fit_reports_stand_base_length_delta(monkeypatch):
    original = ff._dims

    def stretch_stand_length(path):
        dims = original(path)
        if path.name == "stand.stl":
            return dims[0] + 0.2, dims[1], dims[2]
        return dims

    monkeypatch.setattr(ff, "_dims", stretch_stand_length)

    with pytest.raises(AssertionError) as exc:
        ff.verify_fit(CAD_DIR, STL_DIR)

    msg = str(exc.value)
    assert "stand.stl base length mismatch" in msg
    assert "Δ +0.200 mm" in msg


def test_verify_fit_reports_stand_base_width_delta(monkeypatch):
    original = ff._dims

    def stretch_stand_width(path):
        dims = original(path)
        if path.name == "stand.stl":
            return dims[0], dims[1] - 0.2, dims[2]
        return dims

    monkeypatch.setattr(ff, "_dims", stretch_stand_width)

    with pytest.raises(AssertionError) as exc:
        ff.verify_fit(CAD_DIR, STL_DIR)

    msg = str(exc.value)
    assert "stand.stl base width mismatch" in msg
    assert "Δ -0.200 mm" in msg


def test_verify_fit_reports_stand_height_delta(monkeypatch):
    original = ff._dims

    def raise_stand_height(path):
        dims = original(path)
        if path.name == "stand.stl":
            return dims[0], dims[1], dims[2] + 1.0
        return dims

    monkeypatch.setattr(ff, "_dims", raise_stand_height)

    with pytest.raises(AssertionError) as exc:
        ff.verify_fit(CAD_DIR, STL_DIR)

    msg = str(exc.value)
    assert "stand.stl height mismatch" in msg
    assert "Δ +1.000 mm" in msg


def test_verify_fit_reports_adapter_shaft_delta(monkeypatch):
    def fake_parse(path):
        name = Path(path).name
        if name == "shaft.scad":
            return {"shaft_diameter": 8.0, "shaft_length": 50.0}
        if name == "adapter.scad":
            return {
                "shaft_diameter": 7.8,
                "outer_diameter": 20.0,
                "length": 10.0,
            }
        if name == "flywheel.scad":
            return {
                "shaft_diameter": 8.0,
                "diameter": 40.0,
                "height": 12.0,
            }
        if name == "stand.scad":
            return {
                "bearing_outer_d": 16.0,
                "post_height": 5.0,
                "base_thickness": 3.0,
                "base_length": 30.0,
                "base_width": 30.0,
            }
        raise AssertionError(f"unexpected path {path}")

    monkeypatch.setattr(ff, "parse_scad_vars", fake_parse)
    monkeypatch.setattr(ff, "_dims", lambda path: (0.0, 0.0, 0.0))

    with pytest.raises(AssertionError) as exc:
        ff.verify_fit(Path("cad"), Path("stl"))

    msg = str(exc.value)
    assert "adapter shaft_diameter" in msg
    assert "Δ" in msg
    assert "0.200" in msg  # shows exact deviation


def test_verify_fit_reports_wheel_shaft_delta(monkeypatch):
    def fake_parse(path):
        name = Path(path).name
        if name == "shaft.scad":
            return {"shaft_diameter": 8.0, "shaft_length": 50.0}
        if name == "adapter.scad":
            return {
                "shaft_diameter": 8.0,
                "outer_diameter": 20.0,
                "length": 10.0,
            }
        if name == "flywheel.scad":
            return {
                "shaft_diameter": 7.6,
                "diameter": 40.0,
                "height": 12.0,
            }
        if name == "stand.scad":
            return {
                "bearing_outer_d": 16.0,
                "post_height": 5.0,
                "base_thickness": 3.0,
                "base_length": 30.0,
                "base_width": 30.0,
            }
        raise AssertionError(f"unexpected path {path}")

    monkeypatch.setattr(ff, "parse_scad_vars", fake_parse)
    monkeypatch.setattr(ff, "_dims", lambda path: (0.0, 0.0, 0.0))

    with pytest.raises(AssertionError) as exc:
        ff.verify_fit(Path("cad"), Path("stl"))

    msg = str(exc.value)
    assert "flywheel shaft_diameter" in msg
    assert "Δ" in msg
    assert "-0.400" in msg


def test_verify_fit_reports_bearing_delta(monkeypatch):
    def fake_parse(path):
        name = Path(path).name
        if name == "shaft.scad":
            return {"shaft_diameter": 8.0, "shaft_length": 50.0}
        if name == "adapter.scad":
            return {
                "shaft_diameter": 8.0,
                "outer_diameter": 20.0,
                "length": 10.0,
            }
        if name == "flywheel.scad":
            return {
                "shaft_diameter": 8.2,
                "diameter": 40.0,
                "height": 12.0,
            }
        if name == "stand.scad":
            return {
                "bearing_outer_d": 7.6,
                "post_height": 5.0,
                "base_thickness": 3.0,
                "base_length": 30.0,
                "base_width": 30.0,
            }
        raise AssertionError(f"unexpected path {path}")

    monkeypatch.setattr(ff, "parse_scad_vars", fake_parse)
    monkeypatch.setattr(ff, "_dims", lambda path: (0.0, 0.0, 0.0))

    with pytest.raises(AssertionError) as exc:
        ff.verify_fit(Path("cad"), Path("stl"))

    msg = str(exc.value)
    assert "stand bearing_outer_d" in msg
    assert "Δ" in msg
    assert "-0.400" in msg


def test_verify_fit_relaxed_tol_real_models():
    assert ff.verify_fit(CAD_DIR, STL_DIR, tol=0.2)


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


def test_ensure_obj_models_appends_newline(monkeypatch, tmp_path):
    import shutil
    import subprocess
    import sys
    import types

    import webapp.app as webapp_module

    models = tmp_path / "models"
    models.mkdir()
    webapp_module.MODEL_DIR = models
    webapp_module.SCAD_DIR = CAD_DIR

    class DummyMesh:
        def export(self, path, file_type="obj"):
            Path(path).write_bytes(b"no-newline")

    def fake_load(path, file_type=None):
        return DummyMesh()

    def fake_run(cmd, check):
        Path(cmd[2]).write_text("stl")

    monkeypatch.setitem(
        sys.modules, "trimesh", types.SimpleNamespace(load_mesh=fake_load)
    )
    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setattr(shutil, "which", lambda x: "/usr/bin/openscad")

    webapp_module.ensure_obj_models()

    for obj in models.glob("*.obj"):
        assert obj.read_bytes().endswith(b"\n")


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
    assert called.get("port") == 5000


def test_fit_module_main(monkeypatch):
    import sys
    from io import StringIO

    buf = StringIO()
    monkeypatch.setattr(sys, "stdout", buf)
    runpy.run_module("flywheel.fit", run_name="__main__")
    assert "All parts fit together." in buf.getvalue()
