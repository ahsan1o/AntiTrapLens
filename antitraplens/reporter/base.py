"""
Base reporter interface for AntiTrapLens.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from ..core.types import ScanResult

class BaseReporter(ABC):
    """Abstract base class for report generators."""

    def __init__(self, config=None):
        self.config = config

    @abstractmethod
    def generate(self, scan_result: ScanResult, output_path: str = None) -> str:
        """Generate report from scan result."""
        pass

    @abstractmethod
    def get_format(self) -> str:
        """Get the report format (json, html, console, etc.)."""
        pass
