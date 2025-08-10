from src.ci_status import ci_state


def test_ci_state_expected(monkeypatch):
    monkeypatch.setattr(
        "src.ci_status._query_graphql",
        lambda o, r, s: "EXPECTED",
    )
    assert ci_state("o", "r", "s") == "green"
