"""Tests for config module."""

import tempfile
from pathlib import Path

import pytest

from big_red_button.config import load_config


def test_load_config_with_valid_file():
    """Test loading a valid config file."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".toml", delete=False
    ) as f:
        f.write("""
support_email = "test@example.com"
studio_name = "Test Studio"
storage_hosts = ["host1", "host2"]
max_processes = 50
cpu_sample_count = 5
cpu_sample_interval = 2.0
""")
        config_path = Path(f.name)

    try:
        config = load_config(config_path)

        assert config["support_email"] == "test@example.com"
        assert config["studio_name"] == "Test Studio"
        assert config["storage_hosts"] == ["host1", "host2"]
        assert config["max_processes"] == 50
        assert config["cpu_sample_count"] == 5
        assert config["cpu_sample_interval"] == 2.0
    finally:
        config_path.unlink()


def test_load_config_sets_defaults():
    """Test that missing values get default values."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".toml", delete=False
    ) as f:
        f.write("""
support_email = "test@example.com"
studio_name = "Test Studio"
""")
        config_path = Path(f.name)

    try:
        config = load_config(config_path)

        assert config["max_processes"] == 30
        assert config["cpu_sample_count"] == 10
        assert config["cpu_sample_interval"] == 1.0
        assert config["storage_hosts"] == []
        assert "SupportSnapshots" in config["snapshot_root"]
    finally:
        config_path.unlink()


def test_load_config_missing_file():
    """Test that missing config file exits with error."""
    nonexistent = Path("/tmp/nonexistent_config.toml")
    with pytest.raises(SystemExit):
        load_config(nonexistent)
