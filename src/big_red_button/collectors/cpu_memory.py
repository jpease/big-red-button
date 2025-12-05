"""CPU and memory information collector."""

from datetime import datetime
from typing import Any, Dict

import psutil


def collect_cpu_memory(
    sample_count: int = 10, sample_interval: float = 1.0
) -> Dict[str, Any]:
    """Collect CPU and memory statistics with multiple samples.

    Args:
        sample_count: Number of CPU samples to take.
        sample_interval: Time in seconds between samples.

    Returns:
        Dict containing CPU and memory details.
    """
    print(
        f"  Sampling CPU {sample_count} times "
        f"({sample_interval}s intervals)..."
    )

    cpu_samples = []
    for i in range(sample_count):
        sample = {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent_per_cpu": psutil.cpu_percent(
                interval=sample_interval, percpu=True
            ),
            "cpu_percent_overall": psutil.cpu_percent(interval=None),
        }
        cpu_samples.append(sample)
        if i < sample_count - 1:
            print(f"    Sample {i + 1}/{sample_count} complete")

    vm = psutil.virtual_memory()
    sm = psutil.swap_memory()

    return {
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "cpu_count_physical": psutil.cpu_count(logical=False),
        "cpu_samples": cpu_samples,
        "virtual_memory": {
            "total": vm.total,
            "available": vm.available,
            "used": vm.used,
            "free": vm.free,
            "percent": vm.percent,
        },
        "swap_memory": {
            "total": sm.total,
            "used": sm.used,
            "free": sm.free,
            "percent": sm.percent,
        },
    }
