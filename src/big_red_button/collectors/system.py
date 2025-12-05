"""System information collector."""

import getpass
import platform
import time
from datetime import datetime, timezone
from typing import Any, Dict

import psutil


def collect_system_info() -> Dict[str, Any]:
    """Collect basic system and platform information.

    Returns:
        Dict containing system details.
    """
    boot_time = psutil.boot_time()

    try:
        user = getpass.getuser()
    except Exception:
        user = None

    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
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
        "user": user,
    }
