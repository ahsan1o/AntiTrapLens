"""
JSON reporter for AntiTrapLens.
"""

import json
from pathlib import Path
from typing import Dict, Any
from ..core.types import ScanResult
from .base import BaseReporter

class JSONReporter(BaseReporter):
    """JSON-based report generator."""

    def __init__(self, config=None):
        super().__init__(config)

    def generate(self, scan_result: ScanResult, output_path: str = None) -> str:
        """Generate JSON report."""
        if output_path is None:
            output_path = "antitraplens_report.json"

        # Convert scan result to dictionary
        report_data = self._scan_result_to_dict(scan_result)

        # Write to file with pretty printing
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)

        return f"JSON report saved to {output_path}"

    def _scan_result_to_dict(self, scan_result: ScanResult) -> Dict[str, Any]:
        """Convert ScanResult to dictionary."""
        return {
            "metadata": {
                "tool": "AntiTrapLens",
                "version": "1.0.0",
                "timestamp": scan_result.scan_info.get("timestamp"),
                "format": "json"
            },
            "scan_info": scan_result.scan_info,
            "pages": [self._page_to_dict(page) for page in scan_result.pages]
        }

    def _page_to_dict(self, page) -> Dict[str, Any]:
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
                "details": [self._cookie_to_dict(c) for c in page.cookies]
            }

        # Add cookie access analysis
        if hasattr(page, 'cookie_access_analysis'):
            page_dict["cookie_access_analysis"] = page.cookie_access_analysis

        # Add dark patterns
        if hasattr(page, 'dark_patterns'):
            page_dict["dark_patterns"] = {
                "findings": [self._finding_to_dict(f) for f in page.dark_patterns.findings],
                "score": page.dark_patterns.score
            }

        # Add content analysis
        if hasattr(page, 'content_analysis'):
            page_dict["content_analysis"] = page.content_analysis

        return page_dict

    def _cookie_to_dict(self, cookie) -> Dict[str, Any]:
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

    def _finding_to_dict(self, finding) -> Dict[str, Any]:
        """Convert Finding to dictionary."""
        return {
            "pattern": finding.pattern,
            "severity": finding.severity,
            "description": finding.description,
            "element": getattr(finding, 'element', ''),
            "confidence": getattr(finding, 'confidence', 0.0),
            "evidence": getattr(finding, 'evidence', [])
        }

    def get_format(self) -> str:
        """Get report format."""
        return "json"
