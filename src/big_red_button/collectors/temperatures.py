"""System temperature collector."""

import platform
from typing import Any, Dict

import psutil

from ..utils import safe_run


def collect_temperatures() -> Dict[str, Any]:
    """Collect system temperature information if available.

    Returns:
        Dict containing temperature readings.
    """
    temps: Dict[str, Any] = {}
    try:
        if hasattr(psutil, "sensors_temperatures"):
            sensors = psutil.sensors_temperatures()
            if sensors:
                temps["sensors"] = {
                    name: [
                        {
                            "label": entry.label,
                            "current": entry.current,
                            "high": entry.high,
                            "critical": entry.critical,
                        }
                        for entry in entries
                    ]
                    for name, entries in sensors.items()
                }
    except Exception as e:
        temps["error"] = str(e)

    # macOS specific
    if platform.system() == "Darwin":
        # Try powermetrics for thermal data (requires sudo, may fail)
        result = safe_run(
            ["powermetrics", "--samplers", "smc", "-n", "1", "-i", "1000"],
            timeout=3,
        )
        if result["returncode"] == 0:
            temps["powermetrics"] = result["stdout"]

    return temps
