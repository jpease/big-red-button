"""Tests for package structure and imports."""

import big_red_button


def test_package_has_version():
    """Test that package has version attribute."""
    assert hasattr(big_red_button, "__version__")
    assert isinstance(big_red_button.__version__, str)


def test_package_has_main():
    """Test that package has main function."""
    assert hasattr(big_red_button, "main")
    assert callable(big_red_button.main)


def test_can_import_collectors():
    """Test that collectors can be imported."""
    from big_red_button import collectors

    assert hasattr(collectors, "collect_system_info")
    assert hasattr(collectors, "collect_cpu_memory")
    assert hasattr(collectors, "collect_disks")


def test_can_import_config():
    """Test that config module can be imported."""
    from big_red_button import config

    assert hasattr(config, "load_config")


def test_can_import_snapshot():
    """Test that snapshot module can be imported."""
    from big_red_button import snapshot

    assert hasattr(snapshot, "create_snapshot")
    assert hasattr(snapshot, "zip_snapshot")
