from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_basic_example_script_outputs_prompt(tmp_path):
    script = Path(__file__).resolve().parents[1] / "examples" / "basic.py"
    assert script.exists(), "examples/basic.py is required by llms.txt"

    result = subprocess.run(
        [sys.executable, str(script)],
        check=True,
        capture_output=True,
        text=True,
    )

    output = result.stdout
    assert "# Purpose" in output
    assert "# Context" in output
    assert "# Request" in output
    assert output.strip(), "Script should emit non-empty prompt text"
