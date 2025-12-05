"""Foreground application detector."""

import platform
from typing import Any, Dict

import psutil

from ..utils import safe_run


def collect_foreground_app() -> Dict[str, Any]:
    """Detect the foreground application.

    Returns:
        Dict containing foreground app information.
    """
    system = platform.system()

    if system == "Darwin":
        # macOS: AppleScript via osascript
        result = safe_run(
            [
                "osascript",
                "-e",
                'tell application "System Events" to get name of first '
                "application process whose frontmost is true",
            ]
        )
        if result["returncode"] == 0:
            return {
                "method": "osascript",
                "app_name": result["stdout"].strip(),
            }
        return {"method": "osascript", "error": result["stderr"]}

    elif system == "Windows":
        # Windows: try using pywin32
        try:
            import win32gui
            import win32process

            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            window_text = win32gui.GetWindowText(hwnd)

            try:
                process = psutil.Process(pid)
                process_name = process.name()
            except Exception:
                process_name = None

            return {
                "method": "win32gui",
                "window_title": window_text,
                "process_name": process_name,
                "pid": pid,
            }
        except Exception as e:
            return {
                "method": "win32gui",
                "error": str(e),
                "note": "Install pywin32 for foreground app detection",
            }

    return {"method": "unsupported_platform"}
