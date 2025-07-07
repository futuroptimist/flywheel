import subprocess
import sys


def _run(args):
    return subprocess.run(
        [sys.executable, "-m", "flywheel", *args],
        capture_output=True,
        text=True,
        check=True,
    )


def test_help_has_all_subcommands():
    out = _run(["--help"]).stdout
    for cmd in ["init", "update", "audit", "prompt", "crawl"]:
        assert cmd in out
