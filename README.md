# Sometimes you need a Big Red Button

<p align="center">
  <a href="https://github.com/jpease/big-red-button/actions/workflows/ci.yml">
    <img src="https://github.com/jpease/big-red-button/actions/workflows/ci.yml/badge.svg" alt="CI">
  </a>
  <a href="https://codecov.io/gh/jpease/big-red-button">
    <img src="https://codecov.io/gh/jpease/big-red-button/branch/main/graph/badge.svg" alt="Coverage">
  </a>
  <!--
  <a href="https://pypi.org/project/big-red-button/">
    <img src="https://img.shields.io/pypi/v/big-red-button.svg" alt="PyPI">
  </a>
  <a href="https://pypi.org/project/big-red-button/">
    <img src="https://img.shields.io/pypi/pyversions/big-red-button.svg" alt="Python Versions">
  </a>
  -->
  <a href="https://github.com/jpease/big-red-button/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/jpease/big-red-button.svg" alt="License">
  </a>
</p>

<p align="center">
  <img src="./assets/big-red-button.jpg" alt="A big red button" width="66%">
</p>

Big Red Button provides a performance snapshot tool for creative workstations. When artists experience performance issues, they can hit the "big red button" to capture a comprehensive system snapshot for IT support.

## Features

- **Comprehensive System Metrics**: CPU, memory, disk I/O, network stats
- **GPU Monitoring**: NVIDIA, AMD, and Intel GPU utilization and VRAM usage
- **Multi-Sample CPU Collection**: Captures multiple CPU samples to detect intermittent spikes
- **Storage Connectivity**: Tests connectivity to Avid Nexis, NetApp, and other storage hosts
- **Temperature Monitoring**: System and GPU temperature tracking
- **Process Analysis**: Top processes by CPU and memory usage
- **Application Detection**: Identifies installed creative applications (Pro Tools, Resolve, Nuke, Houdini, Maya)
- **User Context**: Prompts user for description of what they were doing and what went wrong
- **Auto-Bundle**: Creates ZIP file and opens email client with pre-filled support email
- **Cross-Platform**: Works on macOS and Windows

## Installation

### Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/jpease/big-red-button.git
cd big-red-button

# Install the package
pip install .

# Or install with all optional dependencies
pip install ".[all]"
```

### Configuration

Initialize a new configuration file:

```bash
# Create config.toml in the current directory
big-red-button --init-config

# Or create it in a specific location (e.g., user config directory)
big-red-button --init-config ~/.config/big-red-button/config.toml
```

Edit `config.toml` with your studio settings:

```toml
support_email = "support@yourstudio.com"
studio_name = "Your Studio Name"
storage_hosts = ["nexis1.yourdomain.local", "netapp1.yourdomain.local"]
# snapshot_root = "/Users/Shared/PerformanceSnapshots"  # Uncomment to override default
max_processes = 30
cpu_sample_count = 10
cpu_sample_interval = 1.0
```

See the generated `config.toml` for detailed documentation of all configuration options.

### Optional Dependencies

The base install includes core functionality. For additional features:

```bash
# GPU monitoring (NVIDIA/AMD)
pip install ".[gpu]"

# Windows foreground app detection
pip install ".[windows]"

# Everything
pip install ".[all]"
```

## Usage

### Command Line

After installation, run from anywhere:

```bash
# Primary command
capture-snapshot

# Alternative command
big-red-button

# Or run as a module
python -m big_red_button
```

### What Happens

1. The script collects comprehensive system metrics
2. You'll be prompted to describe:
   - Which application you were using
   - What you were doing
   - What went wrong
   - How long the issue lasted
   - Severity of the issue
3. All data is bundled into a ZIP file
4. Your file manager opens showing the ZIP file
5. Your default email client opens with a pre-filled email to support
6. Attach the ZIP file and send!

### Creating a Desktop Shortcut

After installing the package, you can create desktop shortcuts for easy access.

#### macOS

Create an AppleScript application:

1. Open **Script Editor**
2. Paste this code:

```applescript
do shell script "capture-snapshot"
```

3. Save as an Application to your Desktop (File → Export, File Format: Application)
4. Optional: Change the icon to a red button image (Get Info → drag image to icon)

#### Windows

Create a batch file:

1. Create a new file called `PerformanceSnapshot.bat`
2. Add this content:

```batch
@echo off
capture-snapshot
pause
```

3. Save to Desktop or any convenient location
4. Optional: Create a shortcut and change the icon to a red button image

## What Gets Collected

The snapshot includes:

| File                  | Description                                                       |
| --------------------- | ----------------------------------------------------------------- |
| `system_info.json`    | OS version, hostname, uptime, boot time                           |
| `cpu_memory.json`     | Multiple CPU samples, RAM usage, swap usage                       |
| `disks.json`          | Mounted volumes, disk space, I/O counters                         |
| `network.json`        | Network interfaces, bandwidth counters, storage host connectivity |
| `processes.json`      | Top processes by CPU and memory                                   |
| `gpu_info.json`       | GPU model, utilization, VRAM, temperature                         |
| `temperatures.json`   | System temperature sensors                                        |
| `foreground_app.json` | Application in focus when snapshot was taken                      |
| `installed_apps.json` | Detected creative applications and versions                       |
| `user_context.json`   | User's description of the issue                                   |
| `README.txt`          | Summary and triage guide                                          |

### Privacy Note

The script minimizes sensitive data collection:

- Only captures process names, not full command-line arguments
- No file contents are captured
- No screenshots are taken
- Users can review the ZIP contents before sending

## Troubleshooting

### "config.toml not found"

Make sure you've copied `config.toml.example` to `config.toml`:

```bash
cp config.toml.example config.toml
```

### "psutil is required but not installed"

Install or reinstall the package:

```bash
pip install .
# Or with all optional dependencies
pip install ".[all]"
```

### GPU information not captured

- **NVIDIA GPUs**: Install `nvidia-smi` (comes with NVIDIA drivers) or `py3nvml`
- **AMD GPUs**: Install vendor tools
- **macOS**: Limited GPU info available, uses `system_profiler`

### Storage host checks failing

- Verify hostnames in `config.toml` are correct and reachable
- Check firewall settings allow ping/ICMP
- Ensure network connectivity to storage hosts

## Contributing

Interested in contributing? See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development setup
- Code style guidelines
- Testing procedures
- Pull request process

## License

See [LICENSE](LICENSE) file for details.

## Support

For issues or questions:

1. Check this README
2. Review the [Issues](https://github.com/jpease/big-red-button/issues) page
3. Contact your IT support team
