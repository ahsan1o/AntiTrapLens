"""
HTML reporter for AntiTrapLens.
"""

import json
from pathlib import Path
from typing import Dict, Any
from ..core.types import ScanResult
from .base import BaseReporter

class HTMLReporter(BaseReporter):
    """HTML-based report generator."""

    def __init__(self, config=None):
        super().__init__(config)

    def generate(self, scan_result: ScanResult, output_path: str = None) -> str:
        """Generate HTML report."""
        if output_path is None:
            output_path = "antitraplens_report.html"

        scan_info = scan_result.scan_info
        pages = scan_result.pages

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
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="hero-section">
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
    </div>

    <div class="content-wrapper">
        {self._generate_pages_html(pages)}
        {self._generate_summary_html(pages)}
    </div>
</body>
</html>"""
        return html

    def _generate_pages_html(self, pages) -> str:
        """Generate HTML for pages section."""
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
                    {self._generate_cookie_html(page)}
                    {self._generate_findings_html(page)}
                    {self._generate_score_html(page)}
                </div>
            </div>"""

        html += '</section>'
        return html

    def _generate_cookie_html(self, page) -> str:
        """Generate HTML for cookie information."""
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

    def _generate_findings_html(self, page) -> str:
        """Generate HTML for findings."""
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

    def _generate_score_html(self, page) -> str:
        """Generate HTML for score."""
        if not hasattr(page, 'dark_patterns') or not page.dark_patterns.score:
            return ''

        score = page.dark_patterns.score
        grade = score.get('grade', 'N/A')
        total_score = score.get('total_score', 0)

        return f'<div class="score"><h4>Score</h4><span class="grade grade-{grade.lower()}">{total_score}/100 ({grade})</span></div>'

    def _generate_summary_html(self, pages) -> str:
        """Generate HTML for summary table."""
        pattern_counts = {}
        for page in pages:
            if hasattr(page, 'dark_patterns'):
                for finding in page.dark_patterns.findings:
                    key = finding.pattern
                    if key not in pattern_counts:
                        pattern_counts[key] = {'count': 0, 'severity': finding.severity}
                    pattern_counts[key]['count'] += 1

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

    def _get_css_styles(self) -> str:
        """Get CSS styles for the HTML report."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #ffffff;
            color: #000000;
            line-height: 1.6;
        }

        .hero-section {
            position: relative;
            height: 400px;
            background: linear-gradient(135deg, #ffffff 0%, #f8f8f8 100%);
            overflow: hidden;
        }

        .hero-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            padding: 40px;
            text-align: center;
        }

        .logo {
            font-size: 2.5em;
            font-weight: 300;
            letter-spacing: 2px;
            margin-bottom: 20px;
            color: #000000;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }

        .hero-title {
            font-size: 3em;
            font-weight: 200;
            margin-bottom: 40px;
            color: #000000;
            max-width: 800px;
            line-height: 1.2;
        }

        .hero-stats {
            display: flex;
            gap: 60px;
            margin-top: 30px;
        }

        .stat-item {
            text-align: center;
        }

        .stat-number {
            display: block;
            font-size: 2.5em;
            font-weight: 300;
            color: #000000;
            margin-bottom: 5px;
        }

        .stat-label {
            font-size: 0.9em;
            color: #666666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .content-wrapper {
            max-width: 1400px;
            margin: 0 auto;
            padding: 60px 40px;
        }

        .pages-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 40px;
            margin-bottom: 80px;
        }

        .page-card {
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .page-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        }

        .card-variation-1 { min-height: 450px; }
        .card-variation-2 { min-height: 380px; }
        .card-variation-3 { min-height: 420px; }

        .card-header {
            background: linear-gradient(135deg, #f8f8f8 0%, #ffffff 100%);
            padding: 30px 30px 20px;
            border-bottom: 1px solid #e0e0e0;
        }

        .card-header h3 {
            font-size: 1.5em;
            font-weight: 400;
            color: #000000;
            margin-bottom: 15px;
        }

        .category-badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .category-general { background: #000000; color: #ffffff; }
        .category-ecommerce { background: #333333; color: #ffffff; }
        .category-social { background: #666666; color: #ffffff; }

        .card-content {
            padding: 30px;
        }

        .url-display {
            margin-bottom: 25px;
        }

        .url-link {
            color: #000000;
            text-decoration: none;
            font-weight: 500;
            border-bottom: 1px solid #000000;
            transition: border-color 0.3s ease;
        }

        .url-link:hover {
            border-color: #666666;
        }

        .cookies, .findings, .score {
            margin-bottom: 25px;
        }

        .cookies h4, .findings h4, .score h4 {
            font-size: 1.1em;
            font-weight: 500;
            color: #000000;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .findings ul {
            list-style: none;
            padding: 0;
        }

        .finding {
            background: #f8f8f8;
            padding: 15px 20px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid #000000;
            font-size: 0.9em;
        }

        .severity-high { border-left-color: #000000; background: #f0f0f0; }
        .severity-medium { border-left-color: #666666; background: #f8f8f8; }
        .severity-low { border-left-color: #cccccc; background: #fafafa; }

        .grade {
            font-size: 1.4em;
            font-weight: 300;
            padding: 12px 24px;
            border-radius: 25px;
            display: inline-block;
        }

        .grade-a, .grade-b { background: #000000; color: #ffffff; }
        .grade-c { background: #666666; color: #ffffff; }
        .grade-d, .grade-f { background: #333333; color: #ffffff; }

        .summary-section {
            background: #f8f8f8;
            padding: 60px 0;
            margin-top: 80px;
        }

        .summary-section h2 {
            text-align: center;
            font-size: 2.5em;
            font-weight: 200;
            color: #000000;
            margin-bottom: 50px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 40px;
        }

        .summary-card {
            background: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }

        .summary-card:hover {
            transform: translateY(-3px);
        }

        .pattern-name {
            font-size: 1.2em;
            font-weight: 400;
            color: #000000;
            margin-bottom: 15px;
        }

        .pattern-count {
            font-size: 3em;
            font-weight: 200;
            color: #000000;
            margin-bottom: 10px;
        }

        .pattern-severity {
            font-size: 0.9em;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .severity-high .pattern-severity { color: #000000; }
        .severity-medium .pattern-severity { color: #666666; }
        .severity-low .pattern-severity { color: #cccccc; }

        .no-findings {
            text-align: center;
            font-size: 1.5em;
            color: #666666;
            padding: 60px;
            font-style: italic;
        }

        @media (max-width: 768px) {
            .hero-stats {
                flex-direction: column;
                gap: 30px;
            }

            .pages-section {
                grid-template-columns: 1fr;
                gap: 30px;
            }

            .summary-grid {
                grid-template-columns: 1fr;
                padding: 0 20px;
            }

            .hero-title {
                font-size: 2em;
            }

            .content-wrapper {
                padding: 40px 20px;
            }
        }
        """

    def get_format(self) -> str:
        """Get report format."""
        return "html"
