import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from example_module import hello  # noqa: E402


def test_hello():
    assert hello("world") == "Hello, world!"
