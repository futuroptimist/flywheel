import importlib

import pytest

from webapp import app as webapp_module


@pytest.fixture(autouse=True)
def _reset_webapp_module():
    """Reload the webapp module between tests to avoid cached state."""
    yield
    importlib.reload(webapp_module)


def test_resolve_port_defaults_to_documented_value(monkeypatch):
    monkeypatch.delenv("FLYWHEEL_WEBAPP_PORT", raising=False)
    assert webapp_module.resolve_port() == 5000


def test_resolve_port_supports_env_override(monkeypatch):
    monkeypatch.setenv("FLYWHEEL_WEBAPP_PORT", "8123")
    assert webapp_module.resolve_port() == 8123


def test_resolve_port_falls_back_on_invalid_input(monkeypatch):
    monkeypatch.setenv("FLYWHEEL_WEBAPP_PORT", "not-a-number")
    assert webapp_module.resolve_port() == 5000
