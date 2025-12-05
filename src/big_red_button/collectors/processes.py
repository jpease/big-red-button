"""Process information collector."""

from typing import Any, Dict

import psutil


def sanitize_cmdline(cmdline: Any) -> Any:
    """Sanitize command line arguments to protect privacy.

    Args:
        cmdline: Command line arguments list or None.

    Returns:
        List containing only the executable name, or None.
    """
    if cmdline and len(cmdline) > 0:
        # Only keep the executable, not full paths/args
        return [cmdline[0]]
    return cmdline


def collect_processes(max_processes: int = 30) -> Dict[str, Any]:
    """Collect information about running processes.

    Args:
        max_processes: Maximum number of top processes to capture.

    Returns:
        Dict containing process information.
    """
    procs = []
    for p in psutil.process_iter(
        attrs=[
            "pid",
            "name",
            "username",
            "cpu_percent",
            "memory_info",
            "cmdline",
        ]
    ):
        info = p.info
        mem_info = info.get("memory_info")

        # Sanitize command line to avoid exposing sensitive info
        cmdline_safe = sanitize_cmdline(info.get("cmdline"))

        procs.append(
            {
                "pid": info.get("pid"),
                "name": info.get("name"),
                "username": info.get("username"),
                "cpu_percent": info.get("cpu_percent"),
                "rss": mem_info.rss if mem_info else None,
                "vms": mem_info.vms if mem_info else None,
                "cmdline": cmdline_safe,
            }
        )

    # Sort by CPU descending, take top N
    procs.sort(key=lambda x: (x["cpu_percent"] or 0), reverse=True)
    top_cpu = procs[:max_processes]

    # Also get top by memory
    procs.sort(key=lambda x: (x["rss"] or 0), reverse=True)
    top_mem = procs[:max_processes]

    return {
        "top_processes_by_cpu": top_cpu,
        "top_processes_by_memory": top_mem,
    }
