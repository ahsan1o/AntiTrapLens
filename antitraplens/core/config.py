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
                # Major Analytics & Advertising
                'google-analytics.com', 'googletagmanager.com', 'doubleclick.net',
                'googleadservices.com', 'googlesyndication.com', 'googleusercontent.com',
                
                # Social Media & Advertising
                'facebook.com', 'facebook.net', 'connect.facebook.net', 'fbcdn.net',
                'twitter.com', 't.co', 'ads-twitter.com', 'analytics.twitter.com',
                'linkedin.com', 'licdn.com', 'ads.linkedin.com',
                'instagram.com', 'cdninstagram.com',
                
                # User Experience & Analytics
                'hotjar.com', 'hotjar.io', 'static.hotjar.com',
                'mixpanel.com', 'api.mixpanel.com', 'cdn.mxpnl.com',
                'amplitude.com', 'api.amplitude.com', 'cdn.amplitude.com',
                'segment.com', 'api.segment.io', 'cdn.segment.com',
                
                # Advertising Networks
                'adsystem.amazon.com', 'amazon-adsystem.com', 'c.amazon-adsystem.com',
                'outbrain.com', 'widgets.outbrain.com', 'odb.outbrain.com',
                'taboola.com', 'cdn.taboola.com', 'trc.taboola.com',
                'criteo.com', 'criteo.net', 'static.criteo.net',
                'pubmatic.com', 'ads.pubmatic.com', 'image6.pubmatic.com',
                'openx.net', 'ox-d.openx.net', 'us-u.openx.net',
                'appnexus.com', 'ib.adnxs.com', 'secure.adnxs.com',
                
                # Video & Streaming
                'youtube.com', 'googlevideo.com', 'youtube-nocookie.com',
                'vimeo.com', 'player.vimeo.com', 'f.vimeo.com',
                'dailymotion.com', 'dmxleo.com', 's2.dmcdn.net',
                
                # Content Delivery & CDN
                'cloudflare.com', 'cloudflarestream.com', 'cdn.cloudflare.com',
                'akamai.net', 'akamaihd.net', 'edgesuite.net',
                'fastly.net', 'fastlylb.net', 'map.fastly.net',
                
                # Marketing & CRM
                'hubspot.com', 'js.hs-scripts.com', 'js.hscollectedforms.net',
                'salesforce.com', 'force.com', 'salesforceliveagent.com',
                'marketo.com', 'munchkin.marketo.net', 'mktoresp.com',
                
                # E-commerce & Retail
                'shopify.com', 'cdn.shopify.com', 'shopifyapps.com',
                'woocommerce.com', 'cdn.woocommerce.com',
                'paypal.com', 'paypalobjects.com', 'www.paypal.com',
                
                # Media & Publishing
                'chartbeat.com', 'static.chartbeat.com', 'ping.chartbeat.net',
                'parsely.com', 'cdn.parsely.com', 'config.parsely.com',
                'quantserve.com', 'secure.quantserve.com', 'pixel.quantserve.com',
                'scorecardresearch.com', 'b.scorecardresearch.com', 'sb.scorecardresearch.com',
                
                # Privacy & Consent
                'cookiebot.com', 'consent.cookiebot.com', 'cdn.cookiebot.com',
                'onetrust.com', 'cdn.cookielaw.org', 'geolocation.onetrust.com',
                'quantcast.com', 'static.quantcast.mgr.consensu.org', 'cmp.quantcast.com',
                
                # Performance & Monitoring
                'newrelic.com', 'js-agent.newrelic.com', 'bam.nr-data.net',
                'datadog.com', 'rum.datadoghq.com', 'browser-intake-datadoghq.com',
                'sentry.io', 'browser.sentry-cdn.com', 'js.sentry-cdn.com',
                
                # Email & Marketing Automation
                'mailchimp.com', 'cdn-images.mailchimp.com', 'downloads.mailchimp.com',
                'constantcontact.com', 'static.ctctcdn.com', 'r20.rs6.net',
                'sendinblue.com', 'sibautomation.com', 'sibforms.com',
                
                # Search & Discovery
                'bing.com', 'bat.bing.com', 'c.bing.com',
                'yahoo.com', 'ads.yahoo.com', 'analytics.yahoo.com',
                'duckduckgo.com', 'improving.duckduckgo.com', 'duckduckgo.com/trackerblocking',
                
                # Mobile & App Analytics
                'appsflyer.com', 'app.appsflyer.com', 'impressions.appsflyer.com',
                'adjust.com', 'app.adjust.com', 's2s.adjust.com',
                'branch.io', 'cdn.branch.io', 'api.branch.io',
                
                # Other Common Trackers
                'zendesk.com', 'static.zdassets.com', 'ekr.zdassets.com',
                'intercom.io', 'widget.intercom.io', 'js.intercomcdn.com',
                'drift.com', 'js.driftt.com', 'driftapi.com',
                'olark.com', 'static.olark.com', 'kl.olark.com',
                'livechatinc.com', 'cdn.livechatinc.com', 'api.livechatinc.com',
                'tawk.to', 'embed.tawk.to', 'cdn.tawk.to',
                'crisp.chat', 'client.crisp.chat', 'cdn.crisp.chat'
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
