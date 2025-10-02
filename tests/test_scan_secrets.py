import sys
from importlib import util
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
SCRIPT_PATH = SCRIPTS_DIR / "scan-secrets.py"
spec = util.spec_from_file_location("scan_secrets", SCRIPT_PATH)
scan_secrets = util.module_from_spec(spec)
sys.modules["scan_secrets"] = scan_secrets
spec.loader.exec_module(scan_secrets)


def run_scan(diff: str):
    return scan_secrets.scan_diff(diff)


def test_detects_github_token():
    token = "ghp_" + "a" * 36
    diff = f"""diff --git a/demo.txt b/demo.txt
--- a/demo.txt
+++ b/demo.txt
@@ -0,0 +1,2 @@
+notes
+token = \"{token}\"
"""
    findings = run_scan(diff)
    assert findings, "Expected GitHub token to be flagged"
    finding = findings[0]
    assert finding.path == "demo.txt"
    assert finding.line == 2
    assert "GitHub" in finding.description
    assert finding.masked.startswith("ghp_")
    assert finding.masked.endswith("aaaa")
    assert "…" in finding.masked


def test_ignores_removed_lines():
    removal = "ghp_" + "abcd" * 9
    diff = (
        "diff --git a/demo.txt b/demo.txt\n"
        "--- a/demo.txt\n"
        "+++ b/demo.txt\n"
        "@@ -1,2 +1,1 @@\n"
        f'-token = "{removal}"\n'
        '+token = "safe"\n'
    )
    findings = run_scan(diff)
    assert findings == []


def test_detects_private_key_block():
    begin = "-----BEGIN " + "RSA PRIVATE KEY-----"
    end = "-----END " + "RSA PRIVATE KEY-----"
    diff = (
        "diff --git a/key.pem b/key.pem\n"
        "--- /dev/null\n"
        "+++ b/key.pem\n"
        "@@ -0,0 +1,4 @@\n"
        f"+{begin}\n"
        "+abc\n"
        "+def\n"
        f"+{end}\n"
    )
    findings = run_scan(diff)
    assert len(findings) == 1
    finding = findings[0]
    assert finding.path == "key.pem"
    assert finding.line == 1
    assert "Private key" in finding.description


def test_no_findings_for_safe_diff():
    diff = """diff --git a/demo.txt b/demo.txt
--- a/demo.txt
+++ b/demo.txt
@@ -1,2 +1,2 @@
-line one
+line one updated
"""
    assert run_scan(diff) == []


@pytest.mark.parametrize(
    "pattern, text",
    [
        (r"AKIA[0-9A-Z]{16}", "AKIA" + "A" * 16),
        (r"ASIA[0-9A-Z]{16}", "ASIA" + "B" * 16),
        (r"sk_(?:live|test)_[A-Za-z0-9]{24,}", "sk_live_" + "a" * 24),
        (r"xox[baprs]-[A-Za-z0-9-]{10,}", "xoxb-" + "abcdEF1234"),
        (
            r"(?i)aws_secret_access_key\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{40}",
            "aws_secret_access_key=" + "C" * 40,
        ),
    ],
)
def test_patterns_cover_expected_strings(pattern, text):
    regex = None
    for compiled, _ in scan_secrets.PATTERNS:
        if compiled.pattern == pattern:
            regex = compiled
            break
    assert regex is not None, f"Pattern {pattern} missing"
    assert regex.search(text)
