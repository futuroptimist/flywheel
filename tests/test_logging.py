import logging

from flywheel.logging import get_logger


def test_default_log_level_info(monkeypatch):
    monkeypatch.delenv("FLYWHEEL_ENV", raising=False)
    monkeypatch.delenv("FLYWHEEL_LOG_LEVEL", raising=False)
    logger = get_logger("default")
    assert logger.level == logging.INFO


def test_production_env_sets_warning(monkeypatch):
    monkeypatch.setenv("FLYWHEEL_ENV", "production")
    monkeypatch.delenv("FLYWHEEL_LOG_LEVEL", raising=False)
    logger = get_logger("prod")
    assert logger.level == logging.WARNING


def test_explicit_level_overrides_env(monkeypatch):
    monkeypatch.setenv("FLYWHEEL_ENV", "production")
    monkeypatch.setenv("FLYWHEEL_LOG_LEVEL", "debug")
    logger = get_logger("override")
    assert logger.level == logging.DEBUG
