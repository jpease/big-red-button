"""Big Red Button - Performance snapshot tool for creative workstations."""

__version__ = "1.0.0"
__author__ = "Your Studio Name"
__description__ = (
    "One-click performance snapshot tool for artists "
    "experiencing performance issues"
)

from .cli import main

__all__ = ["main", "__version__"]
