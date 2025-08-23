import tomllib
from pathlib import Path


def test_typos_allows_physics_terms():
    cfg = tomllib.loads(Path(".typos.toml").read_text())
    words = cfg["default"]["extend-words"]
    assert "precess" in words
    assert "circ" in words
