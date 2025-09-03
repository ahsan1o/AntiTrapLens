"""
Common data conversion utilities for reporters.
"""

from typing import Dict, Any, List
from ...core.types import ScanResult

class DataConverter:
    """Common data conversion utilities."""

    # Dark pattern descriptions and user impact explanations
    DARK_PATTERN_DESCRIPTIONS = {
        'pre_ticked_checkbox': {
            'description': 'Pre-selected checkboxes that opt you into services or subscriptions',
            'user_impact': 'Can lead to unwanted subscriptions, emails, or data sharing without explicit consent'
        },
        'hidden_unsubscribe': {
            'description': 'Unsubscribe links that are difficult to find or deliberately obscured',
            'user_impact': 'Makes it hard to stop unwanted communications, forcing you to continue receiving spam'
        },
        'overloaded_consent': {
            'description': 'Complex consent forms with confusing language or excessive options',
            'user_impact': 'Tricks you into agreeing to more data collection than intended'
        },
        'misleading_button': {
            'description': 'Buttons with confusing labels that don\'t match their actual function',
            'user_impact': 'Can cause you to accidentally agree to terms or purchases you didn\'t intend'
        },
        'forced_popup': {
            'description': 'Popup windows or overlays that are difficult to close or dismiss',
            'user_impact': 'Interrupts your browsing and may force you into unwanted actions'
        },
        'countdown_timer': {
            'description': 'Fake urgency created through countdown timers on deals or offers',
            'user_impact': 'Pressures you into making hasty decisions without proper consideration'
        },
        'endless_scroll': {
            'description': 'Infinite scrolling that keeps loading more content automatically',
            'user_impact': 'Designed to keep you on the site longer, potentially addictive and time-wasting'
        },
        'hidden_costs': {
            'description': 'Additional fees or charges that are revealed only at checkout',
            'user_impact': 'Forces you to pay more than advertised or lose time invested in the purchase process'
        },
        'fake_reviews': {
            'description': 'Artificially inflated ratings or fake testimonials',
            'user_impact': 'Misleads your purchasing decisions with false information'
        },
        'subscription_trap': {
            'description': 'Making it easy to subscribe but difficult to cancel subscriptions',
            'user_impact': 'Can result in unwanted recurring charges that are hard to stop'
        },
        'privacy_buried': {
            'description': 'Important privacy information hidden in long terms or hard-to-find locations',
            'user_impact': 'Prevents informed consent about how your personal data will be used'
        },
        'aggressive_ads': {
            'description': 'Intrusive advertising that disrupts the user experience',
            'user_impact': 'Degrades browsing experience and may trick you into clicking unwanted content'
        },
        'data_collection': {
            'description': 'Excessive collection of personal information beyond what\'s necessary',
            'user_impact': 'Compromises your privacy and may lead to data misuse or breaches'
        },
        'accessibility_issues': {
            'description': 'Design choices that make the site difficult for users with disabilities',
            'user_impact': 'Excludes users with disabilities and may violate accessibility laws'
        },
        'cookie_consent_banner': {
            'description': 'Manipulative cookie consent interfaces that favor data collection',
            'user_impact': 'Tricks you into accepting more tracking than necessary for site functionality'
        },
        'excessive_cookies': {
            'description': 'Websites that set an unreasonable number of tracking cookies',
            'user_impact': 'Enables extensive tracking of your browsing behavior across the web'
        },
        'third_party_tracking': {
            'description': 'Allows external companies to track your behavior on this website',
            'user_impact': 'Your browsing data is shared with multiple third parties for advertising and profiling'
        },
        'tracking_scripts': {
            'description': 'JavaScript code that monitors and records your interactions on the website',
            'user_impact': 'Can track clicks, scrolling, time spent, and other behavioral data for profiling'
        }
    }

    @staticmethod
    def scan_result_to_dict(scan_result: ScanResult) -> Dict[str, Any]:
        """Convert ScanResult to dictionary."""
        return {
            "metadata": {
                "tool": "AntiTrapLens",
                "version": "1.0.0",
                "timestamp": scan_result.scan_info.get("timestamp"),
                "format": "json"
            },
            "scan_info": scan_result.scan_info,
            "pages": [DataConverter._page_to_dict(page) for page in scan_result.pages]
        }

    @staticmethod
    def _page_to_dict(page) -> Dict[str, Any]:
        """Convert PageData to dictionary."""
        page_dict = {
            "url": page.url,
            "title": getattr(page, 'title', ''),
            "category": getattr(page, 'category', 'General'),
            "timestamp": getattr(page, 'timestamp', None)
        }

        # Add cookies information
        if hasattr(page, 'cookies'):
            page_dict["cookies"] = {
                "total": len(page.cookies),
                "third_party": len([c for c in page.cookies if c.is_third_party]),
                "details": [DataConverter._cookie_to_dict(c) for c in page.cookies]
            }

        # Add cookie access analysis
        if hasattr(page, 'cookie_access_analysis'):
            page_dict["cookie_access_analysis"] = page.cookie_access_analysis

        # Add tracking access information
        if hasattr(page, 'tracking_access'):
            page_dict["tracking_access"] = page.tracking_access

        # Add dark patterns and cookies separately
        if hasattr(page, 'dark_patterns'):
            dark_patterns = []
            cookies = []
            for finding in page.dark_patterns.findings:
                if finding.pattern in ['cookie_consent_banner', 'excessive_cookies', 'third_party_tracking', 'tracking_scripts']:
                    cookies.append(DataConverter._finding_to_dict(finding))
                else:
                    dark_patterns.append(DataConverter._finding_to_dict(finding))
            
            page_dict["dark_patterns"] = {
                "findings": dark_patterns,
                "score": page.dark_patterns.score
            }
            page_dict["cookie_findings"] = {
                "findings": cookies
            }

        # Add content analysis
        if hasattr(page, 'content_analysis'):
            page_dict["content_analysis"] = page.content_analysis

        return page_dict

    @staticmethod
    def _cookie_to_dict(cookie) -> Dict[str, Any]:
        """Convert CookieData to dictionary."""
        return {
            "name": cookie.name,
            "domain": cookie.domain,
            "path": cookie.path,
            "value": cookie.value[:50] + "..." if len(cookie.value) > 50 else cookie.value,
            "secure": cookie.secure,
            "http_only": cookie.http_only,
            "same_site": cookie.same_site,
            "expires": cookie.expires,
            "is_third_party": cookie.is_third_party,
            "category": getattr(cookie, 'category', 'Unknown')
        }

    @staticmethod
    def _finding_to_dict(finding) -> Dict[str, Any]:
        """Convert Finding to dictionary with enhanced descriptions."""
        pattern_info = DataConverter.DARK_PATTERN_DESCRIPTIONS.get(finding.pattern, {})
        
        return {
            "pattern": finding.pattern,
            "severity": finding.severity,
            "description": finding.description,
            "pattern_description": pattern_info.get('description', 'Dark pattern detected'),
            "user_impact": pattern_info.get('user_impact', 'May negatively affect user experience'),
            "element": getattr(finding, 'element', ''),
            "confidence": getattr(finding, 'confidence', 0.0),
            "evidence": getattr(finding, 'evidence', [])
        }

    @staticmethod
    def get_pattern_summary(pages) -> Dict[str, Dict[str, Any]]:
        """Get summary of patterns found across all pages."""
        pattern_counts = {}
        for page in pages:
            if hasattr(page, 'dark_patterns'):
                for finding in page.dark_patterns.findings:
                    key = finding.pattern
                    if key not in pattern_counts:
                        pattern_counts[key] = {'count': 0, 'severity': finding.severity}
                    pattern_counts[key]['count'] += 1
        return pattern_counts

    @staticmethod
    def get_dark_pattern_summary(pages) -> Dict[str, Dict[str, Any]]:
        """Get summary of dark patterns found across all pages."""
        pattern_counts = {}
        dark_pattern_types = [
            'pre_ticked_checkbox', 'hidden_unsubscribe', 'overloaded_consent', 'misleading_button',
            'forced_popup', 'countdown_timer', 'endless_scroll', 'hidden_costs', 'fake_reviews',
            'subscription_trap', 'privacy_buried', 'aggressive_ads', 'data_collection', 'accessibility_issues'
        ]
        for page in pages:
            if hasattr(page, 'dark_patterns'):
                for finding in page.dark_patterns.findings:
                    if finding.pattern in dark_pattern_types:
                        key = finding.pattern
                        if key not in pattern_counts:
                            pattern_counts[key] = {'count': 0, 'severity': finding.severity}
                        pattern_counts[key]['count'] += 1
        return pattern_counts

    @staticmethod
    def get_cookie_summary(pages) -> Dict[str, Dict[str, Any]]:
        """Get summary of cookie patterns found across all pages."""
        pattern_counts = {}
        cookie_types = ['cookie_consent_banner', 'excessive_cookies', 'third_party_tracking', 'tracking_scripts']
        for page in pages:
            if hasattr(page, 'dark_patterns'):
                for finding in page.dark_patterns.findings:
                    if finding.pattern in cookie_types:
                        key = finding.pattern
                        if key not in pattern_counts:
                            pattern_counts[key] = {'count': 0, 'severity': finding.severity}
                        pattern_counts[key]['count'] += 1
        return pattern_counts

    @staticmethod
    def get_severity_counts(pages) -> Dict[str, int]:
        """Get counts of findings by severity."""
        counts = {'high': 0, 'medium': 0, 'low': 0}
        for page in pages:
            if hasattr(page, 'dark_patterns'):
                for finding in page.dark_patterns.findings:
                    severity = finding.severity.lower()
                    if severity in counts:
                        counts[severity] += 1
        return counts

    @staticmethod
    def get_dark_pattern_severity_counts(pages) -> Dict[str, int]:
        """Get counts of dark pattern findings by severity."""
        counts = {'high': 0, 'medium': 0, 'low': 0}
        dark_pattern_types = [
            'pre_ticked_checkbox', 'hidden_unsubscribe', 'overloaded_consent', 'misleading_button',
            'forced_popup', 'countdown_timer', 'endless_scroll', 'hidden_costs', 'fake_reviews',
            'subscription_trap', 'privacy_buried', 'aggressive_ads', 'data_collection', 'accessibility_issues'
        ]
        for page in pages:
            if hasattr(page, 'dark_patterns'):
                for finding in page.dark_patterns.findings:
                    if finding.pattern in dark_pattern_types:
                        severity = finding.severity.lower()
                        if severity in counts:
                            counts[severity] += 1
        return counts

    @staticmethod
    def get_cookie_severity_counts(pages) -> Dict[str, int]:
        """Get counts of cookie findings by severity."""
        counts = {'high': 0, 'medium': 0, 'low': 0}
        cookie_types = ['cookie_consent_banner', 'excessive_cookies', 'third_party_tracking', 'tracking_scripts']
        for page in pages:
            if hasattr(page, 'dark_patterns'):
                for finding in page.dark_patterns.findings:
                    if finding.pattern in cookie_types:
                        severity = finding.severity.lower()
                        if severity in counts:
                            counts[severity] += 1
        return counts

    @staticmethod
    def get_pattern_description(pattern: str) -> Dict[str, str]:
        """Get description and user impact for a pattern."""
        return DataConverter.DARK_PATTERN_DESCRIPTIONS.get(pattern, {
            'description': 'Dark pattern detected',
            'user_impact': 'May negatively affect user experience'
        })

    @staticmethod
    def is_dark_pattern(pattern: str) -> bool:
        """Check if pattern is a dark pattern (not cookie/tracking related)."""
        cookie_types = ['cookie_consent_banner', 'excessive_cookies', 'third_party_tracking', 'tracking_scripts']
        return pattern not in cookie_types

    @staticmethod
    def is_cookie_tracking_pattern(pattern: str) -> bool:
        """Check if pattern is cookie/tracking related."""
        cookie_types = ['cookie_consent_banner', 'excessive_cookies', 'third_party_tracking', 'tracking_scripts']
        return pattern in cookie_types
