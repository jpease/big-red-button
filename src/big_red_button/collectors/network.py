"""Network and storage connectivity collector."""

import platform
from typing import Any, Dict, List

import psutil

from ..utils import safe_run


def collect_network(storage_hosts: List[str]) -> Dict[str, Any]:
    """Collect network interface and connectivity information.

    Args:
        storage_hosts: List of hostnames to check connectivity.

    Returns:
        Dict containing network details.
    """
    addrs = {}
    for iface, addr_list in psutil.net_if_addrs().items():
        addrs[iface] = [
            {
                "family": str(a.family),
                "address": a.address,
                "netmask": a.netmask,
                "broadcast": a.broadcast,
                "ptp": a.ptp,
            }
            for a in addr_list
        ]

    stats = {}
    for iface, s in psutil.net_if_stats().items():
        stats[iface] = {
            "isup": s.isup,
            "duplex": str(s.duplex),
            "speed": s.speed,
            "mtu": s.mtu,
        }

    counters = psutil.net_io_counters(pernic=True)
    counters_dict = {}
    for iface, c in counters.items():
        counters_dict[iface] = {
            "bytes_sent": c.bytes_sent,
            "bytes_recv": c.bytes_recv,
            "packets_sent": c.packets_sent,
            "packets_recv": c.packets_recv,
            "errin": c.errin,
            "errout": c.errout,
            "dropin": c.dropin,
            "dropout": c.dropout,
        }

    # Storage host connectivity checks
    print("  Checking storage host connectivity...")
    host_checks = []
    for host in storage_hosts:
        if platform.system() == "Windows":
            cmd = ["ping", "-n", "2", host]
        else:
            cmd = ["ping", "-c", "2", host]
        result = safe_run(cmd, timeout=10)
        host_checks.append(
            {
                "host": host,
                "returncode": result["returncode"],
                "stdout": result["stdout"],
                "stderr": result["stderr"],
            }
        )
        status = "OK" if result["returncode"] == 0 else "FAILED"
        print(f"    {host}: {status}")

    return {
        "interfaces": addrs,
        "stats": stats,
        "counters": counters_dict,
        "storage_host_checks": host_checks,
    }
