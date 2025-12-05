"""Tests for collectors modules."""

from big_red_button import collectors


def test_collect_system_info():
    """Test system info collection returns required fields."""
    info = collectors.collect_system_info()

    assert "timestamp_utc" in info
    assert "timestamp_local" in info
    assert "platform" in info
    assert "hostname" in info
    assert "python_version" in info
    assert "boot_time" in info
    assert "uptime_seconds" in info


def test_collect_cpu_memory():
    """Test CPU/memory collection returns required fields."""
    info = collectors.collect_cpu_memory(sample_count=2, sample_interval=0.1)

    assert "cpu_count_logical" in info
    assert "cpu_count_physical" in info
    assert "cpu_samples" in info
    assert len(info["cpu_samples"]) == 2
    assert "virtual_memory" in info
    assert "swap_memory" in info


def test_collect_disks():
    """Test disk collection returns required fields."""
    info = collectors.collect_disks()

    assert "partitions" in info
    assert "io_counters" in info
    assert isinstance(info["partitions"], list)


def test_collect_network():
    """Test network collection returns required fields."""
    info = collectors.collect_network([])

    assert "interfaces" in info
    assert "stats" in info
    assert "counters" in info
    assert "storage_host_checks" in info


def test_collect_processes():
    """Test process collection returns required fields."""
    info = collectors.collect_processes(max_processes=5)

    assert "top_processes_by_cpu" in info
    assert "top_processes_by_memory" in info
    assert len(info["top_processes_by_cpu"]) <= 5
    assert len(info["top_processes_by_memory"]) <= 5


def test_collect_gpu_info():
    """Test GPU collection returns dict."""
    info = collectors.collect_gpu_info()

    assert isinstance(info, dict)
    assert "platform" in info


def test_collect_temperatures():
    """Test temperature collection returns dict."""
    info = collectors.collect_temperatures()

    assert isinstance(info, dict)


def test_collect_foreground_app():
    """Test foreground app detection returns dict."""
    info = collectors.collect_foreground_app()

    assert isinstance(info, dict)
    assert "method" in info


def test_detect_installed_apps():
    """Test app detection returns dict."""
    info = collectors.detect_installed_apps()

    assert isinstance(info, dict)
