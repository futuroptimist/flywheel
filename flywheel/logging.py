"""Environment-aware logging helpers for Flywheel."""

from __future__ import annotations

import logging
import os
from typing import Optional

_DEF_FORMAT = "%(levelname)s: %(message)s"


def _resolve_level(level_name: Optional[str]) -> int:
    """Return a logging level integer from a name, defaulting to INFO."""
    if not level_name:
        return logging.INFO
    return getattr(logging, level_name.upper(), logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """Return a logger configured based on environment variables.

    The log level can be set via ``FLYWHEEL_LOG_LEVEL``. When unset, the
    ``FLYWHEEL_ENV`` variable controls defaults: ``production`` maps to
    WARNING and any other value maps to INFO.
    """

    level_name = os.getenv("FLYWHEEL_LOG_LEVEL")
    if level_name is None:
        env = os.getenv("FLYWHEEL_ENV")
        level_name = "WARNING" if env == "production" else "INFO"
    level = _resolve_level(level_name)

    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_DEF_FORMAT))
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
