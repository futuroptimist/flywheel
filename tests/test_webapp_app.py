"""Ensure the Flask server starts in production mode during tests."""

from webapp import app as app_module


def test_main_runs_without_debug(monkeypatch):
    called = {}

    def fake_run(**kwargs):
        called.update(kwargs)

    monkeypatch.setattr(app_module.app, "run", fake_run)
    app_module.main()
    assert called.get("debug") is False
    assert called.get("use_reloader") is False
