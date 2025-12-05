"""Utility functions for the Big Red Button tool."""

import json
import subprocess  # nosec B404
from pathlib import Path
from typing import Any, Dict, List


def safe_run(cmd: List[str], timeout: int = 5) -> Dict[str, Any]:
    """Run a command and capture stdout/stderr without raising exceptions.

    Args:
        cmd: Command and arguments as a list.
        timeout: Maximum time in seconds to wait for command.

    Returns:
        Dict with keys: cmd, returncode, stdout, stderr.
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )  # nosec B603
        return {
            "cmd": cmd,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except Exception as e:
        return {
            "cmd": cmd,
            "returncode": None,
            "stdout": "",
            "stderr": f"ERROR running {cmd!r}: {e}",
        }


def write_json(path: Path, data: Any) -> None:
    """Write data to a JSON file.

    Args:
        path: Destination file path.
        data: Data to serialize to JSON.
    """
    path.write_text(
        json.dumps(data, indent=2, sort_keys=True, default=str),
        encoding="utf-8",
    )


def write_text(path: Path, data: str) -> None:
    """Write text data to a file.

    Args:
        path: Destination file path.
        data: Text content to write.
    """
    path.write_text(data, encoding="utf-8")
