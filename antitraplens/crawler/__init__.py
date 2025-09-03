"""
Crawler module for AntiTrapLens.
"""

from .base import BaseCrawler
from .playwright_crawler import PlaywrightCrawler
from .data_extractor import DataExtractor

__all__ = ['BaseCrawler', 'PlaywrightCrawler', 'DataExtractor']
