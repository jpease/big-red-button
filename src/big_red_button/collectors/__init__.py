"""Data collectors for system metrics and information."""

from .cpu_memory import collect_cpu_memory
from .disks import collect_disks
from .foreground_app import collect_foreground_app
from .gpu import collect_gpu_info
from .installed_apps import detect_installed_apps
from .network import collect_network
from .processes import collect_processes
from .system import collect_system_info
from .temperatures import collect_temperatures

__all__ = [
    "collect_system_info",
    "collect_cpu_memory",
    "collect_disks",
    "collect_network",
    "collect_gpu_info",
    "collect_temperatures",
    "collect_processes",
    "collect_foreground_app",
    "detect_installed_apps",
]
