from pathlib import Path


def test_obj_files_have_trailing_newline():
    """All OBJ model files should end with a newline for git hygiene."""
    obj_dir = Path("webapp/static/models")
    for path in obj_dir.rglob("*.obj"):
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"{path} missing trailing newline"
