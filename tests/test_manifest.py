import json
from pathlib import Path

from flywheel.agent import sdk


def test_manifest_generation(tmp_path):
    @sdk.agent_tool(preferred=True)
    def tool_a():
        pass

    @sdk.agent_tool()
    def tool_b():
        pass

    manifest = sdk.generate_manifest()
    data = json.loads(manifest.read_text())
    assert data[0]["name"] == "tool_a"
    assert data[0]["preferred"] is True
    assert any(item["name"] == "tool_b" for item in data)


def test_build_env_triggers_manifest(monkeypatch, tmp_path):
    path = Path(sdk.__file__).resolve().parents[1] / "agent_manifest.json"
    if path.exists():
        path.unlink()
    monkeypatch.setenv("FLYWHEEL_BUILD", "1")
    import importlib

    importlib.reload(sdk)
    assert path.exists()
    path.unlink()
