"""Configuration management for Big Red Button."""

import sys
from pathlib import Path
from typing import Any, Dict, Optional

# TOML support: use tomllib (Python 3.11+) or tomli (older versions)
try:
    import tomllib  # type: ignore[import-not-found]
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[import-not-found]

DEFAULT_CONFIG_TEMPLATE = """# Big Red Button Configuration
# =============================
# Copy this file to config.toml and customize for your studio

# -----------------------------------------------------------------------------
# General Settings
# -----------------------------------------------------------------------------

# Email address where snapshots should be sent
# This will be used in the mailto: link when opening the email client
support_email = "support@example.com"

# Your studio name (appears in email subject line)
# Example: "Acme VFX Studio Performance Snapshot"
studio_name = "Your Studio Name"


# -----------------------------------------------------------------------------
# Storage & Output
# -----------------------------------------------------------------------------

# Directory to save snapshots (optional)
# Leave commented out to use default: ~/SupportSnapshots
# Examples:
#   - macOS shared location: "/Users/Shared/PerformanceSnapshots"
#   - Windows shared location: "C:\\\\ProgramData\\\\PerformanceSnapshots"
# snapshot_root = "/Users/Shared/PerformanceSnapshots"


# -----------------------------------------------------------------------------
# Network
# -----------------------------------------------------------------------------

# Storage server hostnames to check connectivity
# The tool will ping these hosts to verify network connectivity
# Common examples:
#   - Avid Nexis servers: nexis1.yourdomain.local, nexis2.yourdomain.local
#   - NetApp filers: netapp-prod.yourdomain.local
#   - Other NAS/SAN storage: storage1.yourdomain.local
storage_hosts = [
    "nexis1.yourdomain.local",
    "netapp1.yourdomain.local",
]


# -----------------------------------------------------------------------------
# System Collection Settings
# -----------------------------------------------------------------------------

# Number of top processes to capture (by CPU and memory)
# Higher numbers provide more detail but increase snapshot size
# Recommended: 30-50 for most cases
max_processes = 30

# Number of CPU samples to take
# Multiple samples help catch intermittent performance spikes
# Each sample is taken at the interval specified below
# Recommended: 10 samples = 10 seconds of monitoring (with 1.0s interval)
cpu_sample_count = 10

# Seconds between CPU samples (float)
# Shorter intervals catch brief spikes but take longer to complete
# Recommended: 1.0 second for good balance
# Examples:
#   - 0.5: Very detailed, catches brief spikes (5 seconds for 10 samples)
#   - 1.0: Standard monitoring (10 seconds for 10 samples)
#   - 2.0: Longer monitoring period (20 seconds for 10 samples)
cpu_sample_interval = 1.0
"""


def init_config(target_path: Path) -> None:
    """Initialize configuration file at the specified path.

    Args:
        target_path: Path where to write the config file.
    """
    if target_path.exists():
        print(f"Error: File already exists at {target_path}")
        sys.exit(1)

    # Create parent directories if they don't exist
    target_path.parent.mkdir(parents=True, exist_ok=True)

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(DEFAULT_CONFIG_TEMPLATE)

    print(f"Configuration initialized at: {target_path}")
    print("Please edit this file with your studio settings.")


def load_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """Load configuration from config.toml file.

    Args:
        config_path: Optional path to config file. If None, looks in:
                     1. Current directory
                     2. User's home directory
                     3. Package directory

    Returns:
        Dict containing configuration values.

    Raises:
        FileNotFoundError: If config.toml doesn't exist.
        tomllib.TOMLDecodeError: If config.toml is invalid.
    """
    if config_path is None:
        # Search for config in multiple locations
        search_paths = [
            Path.cwd() / "config.toml",
            Path.home() / ".config" / "big-red-button" / "config.toml",
            Path(__file__).parent.parent / "config.toml",
        ]

        for path in search_paths:
            if path.exists():
                config_path = path
                break

        if config_path is None:
            print("ERROR: config.toml not found!")
            print("Searched in:")
            for path in search_paths:
                print(f"  - {path}")
            print()
            print(
                "Please copy config.toml.example to one of these "
                "locations and update with your settings."
            )
            sys.exit(1)

    if not config_path.exists():
        print(f"ERROR: config.toml not found at {config_path}")
        print(
            "Please copy config.toml.example to config.toml and "
            "update with your settings."
        )
        sys.exit(1)

    with open(config_path, "rb") as f:
        config: Dict[str, Any] = tomllib.load(f)

    # Set defaults
    if config.get("snapshot_root") is None:
        config["snapshot_root"] = str(Path.home() / "SupportSnapshots")

    config.setdefault("max_processes", 30)
    config.setdefault("cpu_sample_count", 10)
    config.setdefault("cpu_sample_interval", 1.0)
    config.setdefault("storage_hosts", [])

    return config
