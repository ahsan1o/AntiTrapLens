"""
Common data conversion utilities for reporters.
"""

from typing import Dict, Any, List
from ...core.types import ScanResult

class DataConverter:
    """Common data conversion utilities."""

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

        # Add dark patterns
        if hasattr(page, 'dark_patterns'):
            page_dict["dark_patterns"] = {
                "findings": [DataConverter._finding_to_dict(f) for f in page.dark_patterns.findings],
                "score": page.dark_patterns.score
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
        """Convert Finding to dictionary."""
        return {
            "pattern": finding.pattern,
            "severity": finding.severity,
            "description": finding.description,
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
