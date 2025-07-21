from __future__ import annotations

"""Utilities for defining LLM agent tools."""

import json
import os
from pathlib import Path
from typing import Callable, List

AGENT_TOOLS: List[Callable] = []


def agent_tool(preferred: bool = False) -> Callable:
    """LLM Guidance: Decorator to mark a function as an agent tool."""

    def decorator(func: Callable) -> Callable:
        func._agent_preferred = preferred
        AGENT_TOOLS.append(func)
        return func

    return decorator


def generate_manifest() -> Path:
    """LLM Guidance: Write ``agent_manifest.json`` with tool order."""

    tools = [
        {
            "name": f.__name__,
            "preferred": bool(getattr(f, "_agent_preferred", False)),
        }
        for f in AGENT_TOOLS
    ]
    tools.sort(key=lambda t: not t["preferred"])
    path = Path(__file__).resolve().parents[1] / "agent_manifest.json"
    path.write_text(json.dumps(tools, indent=2))
    return path


if os.environ.get("FLYWHEEL_BUILD"):
    generate_manifest()
