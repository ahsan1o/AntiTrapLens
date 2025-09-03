"""
Core configuration and settings for AntiTrapLens.
"""

from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class CrawlerConfig:
    """Configuration for web crawler."""
    headless: bool = True
    timeout: int = 30000
    retries: int = 2
    user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    viewport: Dict[str, int] = None

    def __post_init__(self):
        if self.viewport is None:
            self.viewport = {'width': 1920, 'height': 1080}

@dataclass
class DetectorConfig:
    """Configuration for dark pattern detector."""
    enable_nlp: bool = True
    severity_weights: Dict[str, int] = None
    max_findings: int = 50

    def __post_init__(self):
        if self.severity_weights is None:
            self.severity_weights = {'high': 10, 'medium': 5, 'low': 2}

@dataclass
class AnalyzerConfig:
    """Configuration for content analyzers."""
    enable_image_analysis: bool = True
    enable_cookie_analysis: bool = True
    max_image_analysis: int = 20
    tracking_domains: List[str] = None

    def __post_init__(self):
        if self.tracking_domains is None:
            self.tracking_domains = [
                'google-analytics.com', 'googletagmanager.com', 'doubleclick.net',
                'facebook.com', 'facebook.net', 'twitter.com', 'linkedin.com',
                'hotjar.com', 'mixpanel.com', 'segment.com', 'amplitude.com'
            ]

@dataclass
class ReporterConfig:
    """Configuration for report generation."""
    output_dir: str = 'reports'
    default_format: str = 'json'
    include_raw_data: bool = False
    max_console_findings: int = 10

class AntiTrapLensConfig:
    """Main configuration class."""
    def __init__(self):
        self.crawler = CrawlerConfig()
        self.detector = DetectorConfig()
        self.analyzer = AnalyzerConfig()
        self.reporter = ReporterConfig()

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'AntiTrapLensConfig':
        """Create config from dictionary."""
        config = cls()
        if 'crawler' in config_dict:
            config.crawler = CrawlerConfig(**config_dict['crawler'])
        if 'detector' in config_dict:
            config.detector = DetectorConfig(**config_dict['detector'])
        if 'analyzer' in config_dict:
            config.analyzer = AnalyzerConfig(**config_dict['analyzer'])
        if 'reporter' in config_dict:
            config.reporter = ReporterConfig(**config_dict['reporter'])
        return config

# Global configuration instance
config = AntiTrapLensConfig()
