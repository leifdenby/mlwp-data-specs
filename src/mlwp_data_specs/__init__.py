"""MLWP data specifications package."""

from .api import open_dataset, validate_dataset
from .loaders import import_loader_hooks, open_with_loader, validate_loader_profiles

__all__ = [
    "__version__",
    "validate_dataset",
    "open_dataset",
    "import_loader_hooks",
    "open_with_loader",
    "validate_loader_profiles",
]
__version__ = "0.1.0"
