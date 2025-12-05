"""Disk and I/O information collector."""

from typing import Any, Dict

import psutil


def collect_disks() -> Dict[str, Any]:
    """Collect disk partition and I/O information.

    Returns:
        Dict containing disk details and I/O counters.
    """
    disks = []
    for part in psutil.disk_partitions(all=True):
        usage = None
        try:
            usage_obj = psutil.disk_usage(part.mountpoint)
            usage = {
                "total": usage_obj.total,
                "used": usage_obj.used,
                "free": usage_obj.free,
                "percent": usage_obj.percent,
            }
        except (PermissionError, OSError):
            # Ignore permission errors or if disk unmounted
            pass  # nosec B110

        disks.append(
            {
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "opts": part.opts,
                "usage": usage,
            }
        )

    # Disk I/O counters
    io_counters: Dict[str, Any] = {}
    try:
        counters = psutil.disk_io_counters(perdisk=True)
        if counters:
            io_counters = {
                disk: {
                    "read_count": c.read_count,
                    "write_count": c.write_count,
                    "read_bytes": c.read_bytes,
                    "write_bytes": c.write_bytes,
                    "read_time": c.read_time,
                    "write_time": c.write_time,
                }
                for disk, c in counters.items()
            }
    except Exception as e:
        io_counters = {"error": str(e)}

    return {
        "partitions": disks,
        "io_counters": io_counters,
    }
