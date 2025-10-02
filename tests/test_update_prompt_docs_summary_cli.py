import importlib


def test_update_prompt_docs_summary_default_repo_list(monkeypatch, tmp_path):
    module = importlib.import_module("scripts.update_prompt_docs_summary")

    repo_file = tmp_path / "repos.txt"
    repo_file.write_text("futuroptimist/flywheel\n")
    monkeypatch.setattr(module, "DEFAULT_REPO_LIST", repo_file)

    created_specs: list[list[str]] = []

    class DummyCrawler:
        def __init__(self, repos, token=None):
            created_specs.append(list(repos))

    monkeypatch.setattr(module, "RepoCrawler", DummyCrawler)

    out_path = tmp_path / "summary.md"

    module.main(["--out", str(out_path)])

    assert created_specs == [["futuroptimist/flywheel"]]
    assert out_path.exists()
