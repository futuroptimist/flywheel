import json

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
