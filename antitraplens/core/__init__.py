"""
Core module for AntiTrapLens.
"""

from .config import AntiTrapLensConfig, config
from .types import (
    CookieData, ImageData, FormData, PopupData, LinkData, MetaTagData,
    PageData, Finding, DetectionResult, ScanResult,
    CookieList, ImageList, FindingList, PageList
)

__all__ = [
    'AntiTrapLensConfig', 'config',
    'CookieData', 'ImageData', 'FormData', 'PopupData', 'LinkData', 'MetaTagData',
    'PageData', 'Finding', 'DetectionResult', 'ScanResult',
    'CookieList', 'ImageList', 'FindingList', 'PageList'
]
