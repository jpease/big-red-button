# Contributing to Big Red Button

Thank you for your interest in contributing to Big Red Button! This document provides guidelines for developers working on this project.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- pip

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/jpease/big-red-button.git
cd big-red-button

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Code Quality Standards

### Code Style

This project follows strict code quality standards:

- **PEP 8** compliant (79 character line length)
- **Type hints** encouraged for function signatures
- **Docstrings** required for all public functions/classes
- **Import sorting** enforced by ruff
- **Security scanning** via bandit

All standards are automatically enforced by pre-commit hooks.

### Tools

We use modern Python tooling:

- **ruff** - Fast linter and formatter (replaces black, flake8, isort)
- **bandit** - Security vulnerability scanner
- **pre-commit** - Automated checks before commits

### Running Code Quality Checks

#### Automatic (Recommended)

Pre-commit hooks run automatically on `git commit`:

```bash
git add .
git commit -m "Your commit message"
# Hooks run automatically and fix issues
```

#### Manual

```bash
# Check code with ruff
ruff check src/

# Auto-fix issues
ruff check --fix src/

# Format code
ruff format src/

# Run security scan
bandit -c pyproject.toml -r src/

# Run all pre-commit hooks
pre-commit run --all-files
```

## Project Structure

```
big-red-button/
├── src/
│   └── big_red_button/          # Main package
│       ├── __init__.py          # Package metadata
│       ├── __main__.py          # python -m entry point
│       ├── cli.py               # CLI interface
│       ├── config.py            # Configuration loading
│       ├── snapshot.py          # Snapshot orchestration
│       ├── utils.py             # Shared utilities
│       └── collectors/          # Data collection modules
│           ├── __init__.py
│           ├── system.py        # System info
│           ├── cpu_memory.py    # CPU/memory metrics
│           ├── disks.py         # Disk usage/IO
│           ├── network.py       # Network + storage checks
│           ├── gpu.py           # GPU metrics
│           ├── temperatures.py  # Temperature sensors
│           ├── processes.py     # Process info
│           ├── foreground_app.py # Active app detection
│           └── installed_apps.py # App version detection
├── config.toml.example          # Configuration template
├── pyproject.toml               # Package configuration (includes all dependencies)
├── CONTRIBUTING.md              # Developer documentation
└── README.md                    # User documentation
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write code following style guidelines
- Add docstrings to new functions
- Update type hints

### 3. Test Locally

```bash
# Install in editable mode
pip install -e .

# Run the tool
capture-snapshot

# Test in different scenarios
```

### 4. Run Quality Checks

```bash
# Format and lint
ruff check --fix src/
ruff format src/

# Security scan
bandit -c pyproject.toml -r src/

# Or run everything
pre-commit run --all-files
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

Pre-commit hooks will automatically:

- Fix formatting issues
- Sort imports
- Check for common errors
- Scan for security issues
- Format TOML/YAML files

If hooks make changes, review them and commit again.

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Commit Message Guidelines

Use conventional commit format:

- `feat: ` - New features
- `fix: ` - Bug fixes
- `docs: ` - Documentation changes
- `refactor: ` - Code refactoring
- `test: ` - Test additions/changes
- `chore: ` - Build process, dependencies

Examples:

```
feat: add temperature monitoring for AMD GPUs
fix: correct network timeout handling
docs: update installation instructions
refactor: extract disk collection to separate module
```

## Adding New Collectors

To add a new data collector:

1. Create a new file in `src/big_red_button/collectors/`
2. Implement a `collect_*()` function that returns a dict
3. Add appropriate error handling
4. Export the function in `collectors/__init__.py`
5. Call it from `snapshot.py`
6. Update README.md to document what's collected

Example:

```python
# src/big_red_button/collectors/new_metric.py
"""New metric collector."""

from typing import Any, Dict

def collect_new_metric() -> Dict[str, Any]:
    """Collect new metric information.

    Returns:
        Dict containing metric details.
    """
    try:
        # Collection logic here
        return {"metric": "value"}
    except Exception as e:
        return {"error": str(e)}
```

## Testing

Currently, testing is manual. Future improvements:

- [ ] Add pytest test suite
- [ ] Add integration tests
- [ ] Add CI/CD pipeline

Manual testing checklist:

- [ ] Test on macOS
- [ ] Test on Windows
- [ ] Test with high CPU load
- [ ] Test with low disk space
- [ ] Test with network storage disconnected
- [ ] Test config file search paths
- [ ] Test all command-line entry points

## Security

- Never commit sensitive data (credentials, tokens, etc.)
- Use bandit to scan for security issues
- Be cautious when collecting user data (privacy)
- Sanitize command-line arguments in process collection

## Questions?

- Open an issue on GitHub
- Check existing documentation in README.md
- Review code comments and docstrings

Thank you for contributing!
