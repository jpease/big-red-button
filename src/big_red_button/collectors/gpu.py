"""GPU information collector."""

import platform
from typing import Any, Dict

from ..utils import safe_run


def collect_gpu_info() -> Dict[str, Any]:
    """Collect GPU information across platforms.

    Returns:
        Dict containing GPU details.
    """
    system = platform.system()
    gpu_info: Dict[str, Any] = {"platform": system}

    # Try nvidia-smi for NVIDIA GPUs
    nvidia_smi = safe_run(
        [
            "nvidia-smi",
            "--query-gpu=index,name,driver_version,"
            "temperature.gpu,utilization.gpu,utilization.memory,"
            "memory.total,memory.used,memory.free",
            "--format=csv,noheader,nounits",
        ],
        timeout=5,
    )
    if nvidia_smi["returncode"] == 0:
        gpu_info["nvidia_smi"] = nvidia_smi["stdout"]

    # Try py3nvml for detailed NVIDIA info
    try:
        import py3nvml.py3nvml as nvml  # type: ignore[import-untyped]

        nvml.nvmlInit()
        device_count = nvml.nvmlDeviceGetCount()
        nvidia_devices = []

        for i in range(device_count):
            handle = nvml.nvmlDeviceGetHandleByIndex(i)
            name = nvml.nvmlDeviceGetName(handle)
            try:
                temp = nvml.nvmlDeviceGetTemperature(
                    handle, nvml.NVML_TEMPERATURE_GPU
                )
            except Exception:
                temp = None

            try:
                util = nvml.nvmlDeviceGetUtilizationRates(handle)
                gpu_util = util.gpu
                mem_util = util.memory
            except Exception:
                gpu_util = None
                mem_util = None

            try:
                mem_info = nvml.nvmlDeviceGetMemoryInfo(handle)
                mem_total = mem_info.total
                mem_used = mem_info.used
                mem_free = mem_info.free
            except Exception:
                mem_total = None
                mem_used = None
                mem_free = None

            nvidia_devices.append(
                {
                    "index": i,
                    "name": name,
                    "temperature": temp,
                    "gpu_utilization": gpu_util,
                    "memory_utilization": mem_util,
                    "memory_total": mem_total,
                    "memory_used": mem_used,
                    "memory_free": mem_free,
                }
            )

        nvml.nvmlShutdown()
        gpu_info["nvidia_devices"] = nvidia_devices
    except Exception as e:
        gpu_info["nvidia_py3nvml_error"] = str(e)

    # Try GPUtil as fallback
    try:
        import GPUtil  # type: ignore[import-untyped]

        gpus = GPUtil.getGPUs()
        gpu_info["gputil_devices"] = [
            {
                "id": gpu.id,
                "name": gpu.name,
                "load": gpu.load,
                "memory_util": gpu.memoryUtil,
                "memory_total": gpu.memoryTotal,
                "memory_used": gpu.memoryUsed,
                "memory_free": gpu.memoryFree,
                "temperature": gpu.temperature,
            }
            for gpu in gpus
        ]
    except Exception as e:
        gpu_info["gputil_error"] = str(e)

    # Platform-specific commands
    if system == "Darwin":
        gpu_info["system_profiler"] = safe_run(
            ["system_profiler", "SPDisplaysDataType"], timeout=10
        )
    elif system == "Windows":
        gpu_info["wmic_video"] = safe_run(
            [
                "wmic",
                "path",
                "win32_VideoController",
                "get",
                "Name,AdapterRAM,DriverVersion",
                "/format:list",
            ],
            timeout=10,
        )

    return gpu_info
