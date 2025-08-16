import subprocess


def test_checks_sh_handles_missing_linkchecker():
    result = subprocess.run(
        ["bash", "-c", "source scripts/checks.sh && run_linkcheck"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "linkchecker not installed" in result.stdout
