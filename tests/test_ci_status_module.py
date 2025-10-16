import src.ci_status as cs
import src.table_builder as tb


def test_ci_state_graphql(monkeypatch):
    monkeypatch.setattr(cs, "_query_graphql", lambda o, r, s: "SUCCESS")
    assert cs.ci_state("o", "r", "sha") == "green"


def test_ci_state_graphql_pending(monkeypatch):
    monkeypatch.setattr(cs, "_query_graphql", lambda o, r, s: "PENDING")
    assert cs.ci_state("o", "r", "sha") == "unknown"


def test_ci_state_rest_fallback(monkeypatch):
    monkeypatch.setattr(cs, "_query_graphql", lambda o, r, s: None)
    monkeypatch.setattr(cs, "_query_rest", lambda o, r, s: "FAILURE")
    assert cs.ci_state("o", "r", "sha") == "red"


def test_ci_state_api_errors_treated_as_failure(monkeypatch):
    monkeypatch.setattr(cs, "_query_graphql", lambda o, r, s: None)
    monkeypatch.setattr(cs, "_query_rest", lambda o, r, s: None)
    assert cs.ci_state("o", "r", "sha") == "red"


def test_ci_state_rest_no_ci(monkeypatch):
    monkeypatch.setattr(cs, "_query_graphql", lambda o, r, s: None)
    monkeypatch.setattr(cs, "_query_rest", lambda o, r, s: "NO_CI")
    assert cs.ci_state("o", "r", "sha") == "unknown"


def test_trunk_cell(monkeypatch):
    monkeypatch.setattr(tb, "ci_state", lambda o, r, s: "green")
    assert tb.trunk_cell("o", "r", "sha") == "✅"
    assert tb.trunk_cell("o", "r", "") == "n/a"


def test_trunk_cell_unknown(monkeypatch):
    monkeypatch.setattr(tb, "ci_state", lambda o, r, s: "unknown")
    assert tb.trunk_cell("o", "r", "sha") == "n/a"
