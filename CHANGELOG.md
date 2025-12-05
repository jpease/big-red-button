# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-12-05

### Fixed
- Runtime crash in non-interactive environments (CI/headless) by replacing `os.getlogin()` with `getpass.getuser()`.
- CI build failures on Windows caused by line ending inconsistencies.
- Numerous static type errors (`mypy`) and security warnings (`bandit`).
- CI pipeline optimizations (caching for pre-commit and mypy).

## [0.1.0] - 2025-12-04

### Added
- Initial release of Big Red Button.
- Performance snapshot tool for creative workstations.
- System performance snapshot collection: CPU, memory, disk, network, GPU, temperatures.
- Process analysis and foreground application detection.
- Storage connectivity checks (Avid Nexis, NetApp).
- Automatic ZIP bundling and email draft creation for support.
- Cross-platform support (macOS, Windows).
- Configurable via TOML (e.g., support email, studio name, snapshot root).
- Command-line interface: `capture-snapshot` and `big-red-button`.
- Module interface: `python -m big_red_button`.
- Modern Python packaging (src-layout, pyproject.toml).
- Pre-commit hooks with Ruff (linter/formatter) and Bandit (security scanner).
- pytest test suite with type hints (mypy) and CI/CD with GitHub Actions.
- Comprehensive documentation: README, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT.
- New `--init-config` CLI option to generate default config file.
- User prompt UX improvements (question numbering).
- Enhanced mail client opening with platform-specific commands.

[0.1.1]: https://github.com/jpease/big-red-button/releases/tag/v0.1.1
[0.1.0]: https://github.com/jpease/big-red-button/releases/tag/v0.1.0
