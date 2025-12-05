"""Installed creative applications detector."""

import os
import platform
from typing import Any, Dict

from ..utils import safe_run


def detect_installed_apps() -> Dict[str, Any]:
    """Detect installed creative applications and their versions.

    Returns:
        Dict containing detected applications.
    """
    apps = {}
    system = platform.system()

    if system == "Darwin":
        # macOS: Check common application paths
        app_paths = {
            "Pro Tools": "/Applications/Pro Tools.app",
            "DaVinci Resolve": "/Applications/DaVinci Resolve/"
            "DaVinci Resolve.app",
            "Nuke": "/Applications/Nuke*/Nuke*.app",
            "Houdini": "/Applications/Houdini/Houdini*.app",
            "Maya": "/Applications/Autodesk/maya*/Maya.app",
        }

        for app_name, path_pattern in app_paths.items():
            result = safe_run(
                [
                    "bash",
                    "-c",
                    f"ls -d {path_pattern} " f"2>/dev/null | head -1",
                ]
            )
            if result["returncode"] == 0 and result["stdout"].strip():
                app_path = result["stdout"].strip()
                # Try to get version
                version_result = safe_run(
                    ["mdls", "-name", "kMDItemVersion", app_path]
                )
                version = (
                    version_result["stdout"].strip()
                    if version_result["returncode"] == 0
                    else "unknown"
                )
                apps[app_name] = {
                    "path": app_path,
                    "version": version,
                }

    elif system == "Windows":
        # Windows: Check registry or common paths
        common_paths = {
            "Pro Tools": r"C:\Program Files\Avid\Pro Tools",
            "DaVinci Resolve": (
                r"C:\Program Files\Blackmagic Design" r"\DaVinci Resolve"
            ),
            "Nuke": r"C:\Program Files\Nuke",
            "Houdini": r"C:\Program Files\Side Effects Software",
            "Maya": r"C:\Program Files\Autodesk\Maya",
        }

        for app_name, path in common_paths.items():
            if os.path.exists(path):
                apps[app_name] = {"path": path, "version": "detected"}

    return apps
