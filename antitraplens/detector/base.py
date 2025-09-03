"""
Base detector interface for AntiTrapLens.
"""

from abc import ABC, abstractmethod
from typing import List
from ..core.types import PageData, Finding, DetectionResult

class BaseDetector(ABC):
    """Abstract base class for dark pattern detectors."""

    def __init__(self, config=None):
        self.config = config

    @abstractmethod
    def detect(self, page_data: PageData) -> DetectionResult:
        """Detect dark patterns in page data."""
        pass

    @abstractmethod
    def get_supported_patterns(self) -> List[str]:
        """Get list of supported dark pattern types."""
        pass
