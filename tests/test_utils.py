"""Tests for utils module."""

import json
import tempfile
from pathlib import Path

from big_red_button.utils import safe_run, write_json, write_text


def test_safe_run_success():
    """Test safe_run with successful command."""
    result = safe_run(["echo", "hello"])

    assert result["returncode"] == 0
    assert "hello" in result["stdout"]
    assert result["stderr"] == ""


def test_safe_run_failure():
    """Test safe_run with failing command."""
    result = safe_run(["false"])

    assert result["returncode"] != 0


def test_safe_run_nonexistent_command():
    """Test safe_run with nonexistent command."""
    result = safe_run(["nonexistent_command_xyz"])

    assert result["returncode"] is None
    assert "ERROR" in result["stderr"]


def test_write_json():
    """Test writing JSON to file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
        path = Path(f.name)

    try:
        data = {"key": "value", "number": 42}
        write_json(path, data)

        with open(path) as f:
            loaded = json.load(f)

        assert loaded == data
    finally:
        path.unlink()


def test_write_text():
    """Test writing text to file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        path = Path(f.name)

    try:
        content = "Hello, World!"
        write_text(path, content)

        assert path.read_text() == content
    finally:
        path.unlink()
