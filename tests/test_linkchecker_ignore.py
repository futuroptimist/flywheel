import pathlib


def test_checks_script_ignores_localhost():
    content = pathlib.Path("scripts/checks.sh").read_text()
    assert "--ignore-url '^http://(localhost|127\\.0\\.0\\.1)'" in content


def test_docs_workflow_ignores_localhost():
    content = pathlib.Path(".github/workflows/03-docs.yml").read_text()
    assert "--ignore-url '^http://(localhost|127\\.0\\.0\\.1)'" in content
