from pathlib import Path


def test_template_dirs_have_lockfiles():
    """Ensure each template with package.json has a lock file."""
    missing = []
    for pkg in Path("templates").rglob("package.json"):
        lock = pkg.with_name("package-lock.json")
        if not lock.exists():
            missing.append(str(lock))
    assert not missing, f"missing package-lock.json: {missing}"
