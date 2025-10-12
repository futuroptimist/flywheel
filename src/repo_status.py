"""Compatibility shim that exposes status helpers under ``src.repo_status``."""

from __future__ import annotations

from flywheel import status_helper as _status_helper

build_parser = _status_helper.build_parser
fetch_repo_status = _status_helper.fetch_repo_status
main = _status_helper.main
requests = _status_helper.requests
status_to_emoji = _status_helper.status_to_emoji
update_readme = _status_helper.update_readme

__all__ = [
    "build_parser",
    "fetch_repo_status",
    "main",
    "requests",
    "status_to_emoji",
    "update_readme",
]
