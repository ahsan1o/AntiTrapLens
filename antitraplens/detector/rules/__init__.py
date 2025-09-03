"""
Rules module for AntiTrapLens detector.
Contains various detection rules for dark patterns and privacy issues.
"""

from .dark_patterns import DarkPatternRules
from .cookie_analysis import CookieAnalysisRules

__all__ = [
    'DarkPatternRules',
    'CookieAnalysisRules'
]
