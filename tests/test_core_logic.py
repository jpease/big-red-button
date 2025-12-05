"""Integration and unit tests for Big Red Button core logic."""

import os
import zipfile
from pathlib import Path

import pytest

from big_red_button.collectors.processes import sanitize_cmdline
from big_red_button.config import load_config
from big_red_button.snapshot import zip_snapshot


# 1. Configuration Precedence Test
def test_config_precedence(tmp_path, monkeypatch):
    """Test that config loading follows the correct precedence order:
    1. Explicit path (if provided) - Not tested here as load_config logic varies
    2. Current Working Directory
    3. User Home Directory
    4. Package Directory (fallback)
    """
    # Setup directories
    cwd_dir = tmp_path / "cwd"
    home_dir = tmp_path / "home"
    pkg_dir = tmp_path / "pkg"  # Simulation for package dir

    cwd_dir.mkdir()
    home_dir.mkdir()
    pkg_dir.mkdir()

    # Mock paths
    # We need to mock Path.cwd() and Path.home()
    monkeypatch.setattr(Path, "cwd", lambda: cwd_dir)
    monkeypatch.setattr(Path, "home", lambda: home_dir)

    # Note: We can't easily mock __file__ resolution inside the module without reloading it
    # or refactoring load_config to accept a search_paths argument.
    # For this test, we will focus on CWD vs Home precedence which is most critical.

    # Create different configs
    (cwd_dir / "config.toml").write_text(
        'studio_name = "CWD Studio"', encoding="utf-8"
    )
    (home_dir / ".config" / "big-red-button").mkdir(parents=True)
    (home_dir / ".config" / "big-red-button" / "config.toml").write_text(
        'studio_name = "Home Studio"', encoding="utf-8"
    )

    # 1. Test CWD priority
    # When both exist, CWD should win
    config = load_config(config_path=None)
    assert config["studio_name"] == "CWD Studio"

    # 2. Test Home fallback
    # Remove CWD config, should fall back to Home
    (cwd_dir / "config.toml").unlink()
    config = load_config(config_path=None)
    assert config["studio_name"] == "Home Studio"


# 2. Privacy Sanitization Test
@pytest.mark.parametrize(
    "input_cmd,expected",
    [
        (
            ["/usr/bin/python", "-p", "secret_password"],
            ["/usr/bin/python"],
        ),  # Standard case
        (["./my_script.sh"], ["./my_script.sh"]),  # Single arg
        ([], []),  # Empty list
        (None, None),  # None input
        (
            ["app.exe", "--token=12345"],
            ["app.exe"],
        ),  # Windows style with args
    ],
)
def test_sanitize_cmdline(input_cmd, expected):
    """Test that command lines are strictly sanitized to remove arguments."""
    assert sanitize_cmdline(input_cmd) == expected


# 3. ZIP Creation & Structure Test
def test_zip_creation_integrity(tmp_path):
    """Test that zip_snapshot creates a valid ZIP file with correct structure."""
    # Setup: Create a fake snapshot directory
    snap_dir = tmp_path / "support_snapshot_20250101_120000"
    snap_dir.mkdir()

    # Add some dummy content
    (snap_dir / "system_info.json").write_text(
        '{"os": "test"}', encoding="utf-8"
    )
    (snap_dir / "README.txt").write_text("Test Readme", encoding="utf-8")

    # Create a subdirectory to test recursion
    (snap_dir / "logs").mkdir()
    (snap_dir / "logs" / "debug.log").write_text(
        "Log content", encoding="utf-8"
    )

    # Execute
    zip_path = zip_snapshot(snap_dir)

    # Verify 1: File exists
    assert zip_path.exists()
    assert zip_path.name == "support_snapshot_20250101_120000.zip"

    # Verify 2: ZIP validity and contents
    with zipfile.ZipFile(zip_path, "r") as zf:
        file_list = zf.namelist()

        # Check all expected files are present
        # Note: relative_to in zip_snapshot creates paths like "support_snapshot_.../system_info.json"
        base_name = snap_dir.name
        assert f"{base_name}/system_info.json" in file_list
        assert f"{base_name}/README.txt" in file_list
        assert f"{base_name}/logs/debug.log" in file_list

        # Verify 3: Content integrity
        data = zf.read(f"{base_name}/system_info.json").decode("utf-8")
        assert data == '{"os": "test"}'

        # Verify 4: No absolute paths (security check)
        for name in file_list:
            assert not os.path.isabs(name)
            assert ".." not in name
