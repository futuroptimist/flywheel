import sys


def test_python_version():
    assert sys.version_info[:2] == (3, 12)
