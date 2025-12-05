"""System information collector."""

import os
import platform
import time
from datetime import UTC, datetime
from typing import Any, Dict

import psutil


def collect_system_info() -> Dict[str, Any]:
    """Collect basic system and platform information.

    Returns:
        Dict containing system details.
    """
    boot_time = psutil.boot_time()
    return {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "timestamp_local": datetime.now().isoformat(),
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "hostname": platform.node(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "boot_time": datetime.fromtimestamp(boot_time).isoformat(),
        "uptime_seconds": time.time() - boot_time,
        "user": os.getlogin() if hasattr(os, "getlogin") else None,
    }
