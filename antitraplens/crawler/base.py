"""
Base crawler interface for AntiTrapLens.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..core.types import PageData

class BaseCrawler(ABC):
    """Abstract base class for web crawlers."""

    def __init__(self, config=None):
        self.config = config

    @abstractmethod
    def crawl_page(self, url: str, **kwargs) -> Optional[PageData]:
        """Crawl a single page and return page data."""
        pass

    @abstractmethod
    def crawl_with_depth(self, start_url: str, max_depth: int = 1, max_pages: int = 10) -> list[PageData]:
        """Crawl website with depth and return list of page data."""
        pass

    @abstractmethod
    def close(self):
        """Close crawler resources."""
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
