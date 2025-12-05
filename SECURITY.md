# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by emailing:

**536+jpease@users.noreply.github.com**

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

### What to Include

Please include the following information in your report:

- Type of vulnerability
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### Response Process

1. **Acknowledgment**: We'll acknowledge receipt of your vulnerability report within 48 hours
2. **Investigation**: We'll investigate and validate the vulnerability
3. **Fix Development**: We'll develop a fix and create a security advisory
4. **Disclosure**: We'll coordinate disclosure timing with you
5. **Credit**: We'll publicly credit you (unless you prefer to remain anonymous)

## Security Best Practices

When using this tool:

### For Administrators

- **Review collected data** before sending to ensure no sensitive information is included
- **Configure firewalls** appropriately if deploying across networks
- **Use encrypted channels** when transmitting snapshot files
- **Limit access** to configuration files containing email addresses
- **Regularly update** to the latest version

### For Users

- **Review snapshots** before sending to support
- **Don't include** passwords, API keys, or credentials in descriptions
- **Be aware** that process names and system info are collected
- **Use secure channels** when emailing snapshot files

## Known Limitations

- Process command lines are sanitized (only executable names collected)
- No file contents are captured
- No screenshots are taken
- Network passwords are not collected

## Security Scanning

This project uses:

- **Bandit** - Automated security vulnerability scanner
- **Ruff** - Code quality and security linting
- **Pre-commit hooks** - Automated security checks
- **GitHub Actions** - Automated security scanning on PRs

## Dependency Security

We monitor dependencies for known vulnerabilities:

- Dependencies are specified with minimum versions
- We use Dependabot for automated dependency updates
- Security advisories are monitored via GitHub

## Questions?

If you have questions about security but don't have a vulnerability to report, please open a GitHub discussion or contact us at 536+jpease@users.noreply.github.com.
