"""
HTML reporter for AntiTrapLens.
"""

import json
from pathlib import Path
from typing import Dict, Any
from ...core.types import ScanResult
from ..base import BaseReporter
from ..common import DataConverter
from .styles import CSS_STYLES

class HTMLReporter(BaseReporter):
    """HTML-based report generator."""

    def __init__(self, config=None):
        super().__init__(config)

    def generate(self, scan_result: ScanResult, output_path: str = None) -> str:
        """Generate HTML report."""
        if output_path is None:
            output_path = "antitraplens_report.html"

        html_content = self._generate_html(scan_result)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return f"HTML report saved to {output_path}"

    def _generate_html(self, scan_result: ScanResult) -> str:
        """Generate HTML content."""
        scan_info = scan_result.scan_info
        pages = scan_result.pages

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AntiTrapLens Report</title>
    <style>
        {CSS_STYLES}
    </style>
</head>
<body>
    {self._generate_hero_section(scan_info)}
    <div class="content-wrapper">
        {self._generate_pages_section(pages)}
        {self._generate_summary_section(pages)}
    </div>
</body>
</html>"""
        return html

    def _generate_hero_section(self, scan_info: Dict[str, Any]) -> str:
        """Generate hero section HTML."""
        return f"""<div class="hero-section">
    <div class="hero-overlay">
        <div class="logo">AntiTrapLens</div>
        <h1 class="hero-title">Privacy & Dark Pattern Analysis Report</h1>
        <div class="hero-stats">
            <div class="stat-item">
                <span class="stat-number">{scan_info.get('pages_scanned', 0)}</span>
                <span class="stat-label">Pages Scanned</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{scan_info.get('total_findings', 0)}</span>
                <span class="stat-label">Findings</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{scan_info.get('start_url', 'N/A')}</span>
                <span class="stat-label">Target URL</span>
            </div>
        </div>
    </div>
</div>"""

    def _generate_pages_section(self, pages) -> str:
        """Generate pages section HTML."""
        html = '<section class="pages-section">'

        for i, page in enumerate(pages):
            category = getattr(page, 'category', 'General') or 'General'
            card_class = f"page-card card-variation-{i % 3 + 1}"
            html += f"""
            <div class="{card_class}">
                <div class="card-header">
                    <h3>Page Analysis {i+1}</h3>
                    <span class="category-badge category-{category.lower()}">{category}</span>
                </div>
                <div class="card-content">
                    <div class="url-display">
                        <a href="{page.url}" target="_blank" class="url-link">{page.url}</a>
                    </div>
                    {self._generate_page_cookies(page)}
                    {self._generate_page_findings(page)}
                    {self._generate_page_score(page)}
                </div>
            </div>"""

        html += '</section>'
        return html

    def _generate_page_cookies(self, page) -> str:
        """Generate cookie information HTML."""
        if not hasattr(page, 'cookies') or not page.cookies:
            return '<p class="no-data">No cookies found</p>'

        html = f'<div class="cookies"><h4>Cookies ({len(page.cookies)} total)</h4>'

        third_party = [c for c in page.cookies if c.is_third_party]
        if third_party:
            html += f'<p><strong>Third-party:</strong> {len(third_party)}</p>'

        if hasattr(page, 'cookie_access_analysis'):
            analysis = page.cookie_access_analysis
            if analysis.get('data_collection'):
                html += f'<p><strong>Data Collection:</strong> {", ".join(analysis["data_collection"][:3])}</p>'
            if analysis.get('privacy_concerns'):
                html += f'<p><strong>Privacy Issues:</strong> {len(analysis["privacy_concerns"])}</p>'

        html += '</div>'
        return html

    def _generate_page_findings(self, page) -> str:
        """Generate findings HTML."""
        if not hasattr(page, 'dark_patterns') or not page.dark_patterns.findings:
            return '<p class="no-data">No findings</p>'

        findings = page.dark_patterns.findings
        html = f'<div class="findings"><h4>Findings ({len(findings)})</h4><ul>'

        for finding in findings:
            html += f'<li class="finding severity-{finding.severity.lower()}">'
            html += f'<strong>{finding.pattern}</strong> ({finding.severity}): {finding.description}'
            html += '</li>'

        html += '</ul></div>'
        return html

    def _generate_page_score(self, page) -> str:
        """Generate score HTML."""
        if not hasattr(page, 'dark_patterns') or not page.dark_patterns.score:
            return ''

        score = page.dark_patterns.score
        grade = score.get('grade', 'N/A')
        total_score = score.get('total_score', 0)

        return f'<div class="score"><h4>Score</h4><span class="grade grade-{grade.lower()}">{total_score}/100 ({grade})</span></div>'

    def _generate_summary_section(self, pages) -> str:
        """Generate summary section HTML."""
        pattern_counts = DataConverter.get_pattern_summary(pages)

        if not pattern_counts:
            return '<section class="summary-section"><div class="no-findings">No dark patterns detected - clean scan!</div></section>'

        html = '<section class="summary-section"><h2>Detection Summary</h2><div class="summary-grid">'

        for pattern, data in sorted(pattern_counts.items(), key=lambda x: x[1]['count'], reverse=True):
            severity_class = f"severity-{data['severity'].lower()}"
            html += f'''
            <div class="summary-card {severity_class}">
                <div class="pattern-name">{pattern.replace('_', ' ').title()}</div>
                <div class="pattern-count">{data["count"]}</div>
                <div class="pattern-severity">{data["severity"].upper()}</div>
            </div>'''

        html += '</div></section>'
        return html

    def get_format(self) -> str:
        """Get report format."""
        return "html"
