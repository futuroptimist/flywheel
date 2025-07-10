import subprocess
from pathlib import Path

import flywheel.export_obj as eo


def test_export_obj_invokes_openscad(monkeypatch):
    calls = []

    def fake_run(cmd, check):
        calls.append(cmd)

    monkeypatch.setattr(subprocess, "run", fake_run)
    scad = Path("foo.scad")
    obj = Path("foo.obj")
    eo.export_obj(scad, obj)
    assert calls == [["openscad", "-o", str(obj), str(scad)]]
