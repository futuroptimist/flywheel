from flywheel.repocrawler import RepoCrawler


def test_weird_workflow_names():
    files = {"build-fast.yml", "QA.yml", "custom-docs.yml"}
    crawler = RepoCrawler([])
    assert crawler._has_ci(files) is True
