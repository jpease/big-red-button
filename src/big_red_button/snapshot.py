"""Snapshot creation and management."""

import platform
import subprocess  # nosec B404
import textwrap
import webbrowser
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from urllib.parse import quote

from . import collectors
from .utils import write_json, write_text


def prompt_user_context() -> Dict[str, Any]:
    """Prompt user for context about the performance issue.

    Returns:
        Dict containing user-provided context.
    """
    print()
    print("=" * 70)
    print("Performance Snapshot")
    print("=" * 70)
    print("This will collect system info and bundle it for support.")
    print()

    # Question 1/4
    app_name = input(
        "1/4 Which app were you using? "
        "(e.g. Pro Tools, Resolve, Nuke, Houdini, Maya): "
    ).strip()

    print()
    # Question 2/4
    print("2/4 Briefly describe what you were doing and what went wrong.")
    print("Type your description; end with an empty line:")
    print()

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            break
        lines.append(line)

    description = "\n".join(lines).strip()

    # Question 3/4
    print()
    print("3/4 Roughly how long had the issue been happening?")
    print("  1) < 1 minute")
    print("  2) 1-5 minutes")
    print("  3) 5-15 minutes")
    print("  4) 15+ minutes")
    dur_choice = input("Choose 1-4 (or press Enter to skip): ").strip()

    duration_map = {
        "1": "< 1 minute",
        "2": "1-5 minutes",
        "3": "5-15 minutes",
        "4": "15+ minutes",
    }
    duration = duration_map.get(dur_choice)

    # Question 4/4
    print()
    print("4/4 How severe was the performance issue?")
    print("  1) Annoying but workable")
    print("  2) Significantly impacting work")
    print("  3) Work is blocked / app frozen")
    severity_choice = input("Choose 1-3 (or press Enter to skip): ").strip()

    severity_map = {
        "1": "Annoying but workable",
        "2": "Significantly impacting work",
        "3": "Work is blocked / app frozen",
    }
    severity = severity_map.get(severity_choice)

    return {
        "app_name": app_name,
        "description": description,
        "duration_hint": duration,
        "severity": severity,
    }


def create_snapshot(config: Dict[str, Any]) -> Path:
    """Create a complete performance snapshot.

    Args:
        config: Configuration dict.

    Returns:
        Path to the snapshot directory.
    """
    snapshot_root = Path(config["snapshot_root"])
    snapshot_root.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    snap_dir = snapshot_root / f"support_snapshot_{timestamp}"
    snap_dir.mkdir(parents=True, exist_ok=False)

    print()
    print(f"Creating snapshot in: {snap_dir}")
    print()

    # Collect all data
    print("Collecting system info...")
    write_json(snap_dir / "system_info.json", collectors.collect_system_info())

    print("Collecting CPU and memory info...")
    write_json(
        snap_dir / "cpu_memory.json",
        collectors.collect_cpu_memory(
            config["cpu_sample_count"], config["cpu_sample_interval"]
        ),
    )

    print("Collecting disk info...")
    write_json(snap_dir / "disks.json", collectors.collect_disks())

    print("Collecting network info...")
    write_json(
        snap_dir / "network.json",
        collectors.collect_network(config.get("storage_hosts", [])),
    )

    print("Collecting process info...")
    write_json(
        snap_dir / "processes.json",
        collectors.collect_processes(config["max_processes"]),
    )

    print("Collecting GPU info...")
    write_json(snap_dir / "gpu_info.json", collectors.collect_gpu_info())

    print("Collecting temperature info...")
    write_json(
        snap_dir / "temperatures.json", collectors.collect_temperatures()
    )

    print("Detecting foreground app...")
    write_json(
        snap_dir / "foreground_app.json", collectors.collect_foreground_app()
    )

    print("Detecting installed applications...")
    write_json(
        snap_dir / "installed_apps.json", collectors.detect_installed_apps()
    )

    # User context
    user_context = prompt_user_context()
    write_json(snap_dir / "user_context.json", user_context)

    # Create README
    readme = (
        textwrap.dedent(f"""
        Performance Snapshot
        ====================

        Studio: {config['studio_name']}
        Created: {datetime.now().isoformat()}
        Host: {platform.node()}
        Platform: {platform.system()} {platform.release()}

        Files:
          - system_info.json        : OS, hardware, timestamps, boot time
          - cpu_memory.json         : CPU samples, per-core usage, RAM, swap
          - disks.json              : Mounted volumes, usage, I/O counters
          - network.json            : NICs, throughput, storage host checks
          - processes.json          : Top processes by CPU and memory
          - gpu_info.json           : GPU utilization, VRAM, temperature
          - temperatures.json       : System temperature sensors
          - foreground_app.json     : Active application at capture time
          - installed_apps.json     : Detected creative applications
          - user_context.json       : User description of issue

        Triage Steps:
          1. Check user_context.json for user's description and app
          2. Review cpu_memory.json for CPU/RAM saturation or spikes
          3. Check processes.json for runaway processes
          4. Review gpu_info.json for GPU throttling or VRAM issues
          5. Check temperatures.json for thermal throttling
          6. Review disks.json for storage capacity or I/O bottlenecks
          7. Check network.json for storage connectivity issues

    """).strip()
        + "\n"
    )
    write_text(snap_dir / "README.txt", readme)

    print()
    print("Snapshot collection complete!")
    return snap_dir


def zip_snapshot(snap_dir: Path) -> Path:
    """Create a ZIP archive of the snapshot directory.

    Args:
        snap_dir: Path to snapshot directory.

    Returns:
        Path to created ZIP file.
    """
    print("Creating ZIP archive...")
    zip_path = snap_dir.parent / f"{snap_dir.name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in snap_dir.rglob("*"):
            if path.is_file():
                zf.write(path, arcname=path.relative_to(snap_dir.parent))
    return zip_path


def reveal_in_file_manager(path: Path) -> None:
    """Open file manager and highlight the specified file.

    Args:
        path: Path to file to reveal.
    """
    system = platform.system()
    if system == "Darwin":
        subprocess.run(["open", "-R", str(path)], check=False)  # nosec B603, B607
    elif system == "Windows":
        subprocess.run(["explorer", f'/select,"{path}"'], check=False)  # nosec B603, B607
    else:
        print(f"Please locate this file manually: {path}")


def open_email_draft(zip_path: Path, config: Dict[str, Any]) -> None:
    """Open default email client with pre-filled support email.

    Args:
        zip_path: Path to the ZIP file to reference.
        config: Configuration dict.
    """
    subject = f"{config['studio_name']} Performance Snapshot"
    body = (
        "A performance snapshot has been created.\n\n"
        f"Snapshot file: {zip_path.name}\n"
        f"Location: {zip_path.parent}\n\n"
        "Please attach this file to the email before sending.\n"
    )

    mailto_link = (
        f"mailto:{config['support_email']}"
        f"?subject={quote(subject)}"
        f"&body={quote(body)}"
    )

    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            # Try to open with Mail.app specifically, fallback to default handler
            subprocess.run(["open", "-a", "Mail", mailto_link], check=True)  # nosec B603, B607
        elif system == "Windows":  # Windows
            subprocess.run(["start", mailto_link], shell=True, check=True)  # nosec B602, B607
        elif system == "Linux":  # Linux
            subprocess.run(["xdg-open", mailto_link], check=True)  # nosec B603, B607
        else:
            # Fallback for other systems or if specific commands fail
            webbrowser.open(mailto_link)
    except subprocess.CalledProcessError as e:
        print(f"Error opening mail client: {e}")
        print("Attempting fallback with webbrowser module...")
        webbrowser.open(mailto_link)
    except FileNotFoundError:
        print(
            "Mail client command not found. Attempting fallback with webbrowser module..."
        )
        webbrowser.open(mailto_link)
    except Exception as e:
        print(f"An unexpected error occurred while opening mail client: {e}")
        print("Attempting fallback with webbrowser module...")
        webbrowser.open(mailto_link)
