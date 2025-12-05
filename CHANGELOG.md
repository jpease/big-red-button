# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release
- System performance snapshot collection
- CPU, memory, disk, and network monitoring
- GPU utilization tracking (NVIDIA, AMD)
- Temperature monitoring
- Process analysis
- Storage connectivity checks (Avid Nexis, NetApp)
- Automatic ZIP bundling
- Email draft creation for support
- Cross-platform support (macOS, Windows)
- TOML configuration
- Modern Python packaging (src-layout, pyproject.toml)
- Pre-commit hooks with ruff and bandit
- pytest test suite
- Type hints with mypy
- CI/CD with GitHub Actions
- Comprehensive documentation

## [1.0.0] - 2024-12-04

### Added
- Initial public release
- Performance snapshot tool for creative workstations
- Support for Pro Tools, DaVinci Resolve, Nuke, Houdini, Maya
- Configurable via TOML
- Command-line interface: `capture-snapshot`
- Module interface: `python -m big_red_button`

[Unreleased]: https://github.com/jpease/big-red-button/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/jpease/big-red-button/releases/tag/v1.0.0
