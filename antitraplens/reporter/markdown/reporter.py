"""
Markdown reporter for AntiTrapLens.
"""

from pathlib import Path
from typing import Dict, Any
from ...core.types import ScanResult
from ..base import BaseReporter
from ..common import DataConverter

class MarkdownReporter(BaseReporter):
    """Markdown-based report generator."""

    def __init__(self, config=None):
        super().__init__(config)

    def generate(self, scan_result: ScanResult, output_path: str = None) -> str:
        """Generate Markdown report."""
        if output_path is None:
            output_path = "antitraplens_report.md"

        markdown_content = self._generate_markdown(scan_result)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        return f"Markdown report saved to {output_path}"

    def _generate_markdown(self, scan_result: ScanResult) -> str:
        """Generate Markdown content."""
        scan_info = scan_result.scan_info
        pages = scan_result.pages

        markdown = self._generate_header(scan_info)
        markdown += self._generate_page_details(pages)
        markdown += self._generate_summary_table(pages, scan_info)

        return markdown

    def _generate_header(self, scan_info: Dict[str, Any]) -> str:
        """Generate markdown header."""
        return f"""# AntiTrapLens Report

## Scan Summary

- **Start URL**: {scan_info.get('start_url', 'N/A')}
- **Pages Scanned**: {scan_info.get('pages_scanned', 0)}
- **Total Findings**: {scan_info.get('total_findings', 0)}
- **Timestamp**: {scan_info.get('timestamp', 'N/A')}

## Page Details

"""

    def _generate_page_details(self, pages) -> str:
        """Generate page details section."""
        markdown = ""
        for i, page in enumerate(pages):
            category = getattr(page, 'category', 'General')
            markdown += f"""### Page {i+1}: [{page.url}]({page.url})
**Category**: {category}

"""
            markdown += self._generate_page_cookies(page)
            markdown += self._generate_page_findings(page)
            markdown += self._generate_page_score(page)
        return markdown

    def _generate_page_cookies(self, page) -> str:
        """Generate cookie information for a page."""
        if not hasattr(page, 'cookies') or not page.cookies:
            return ""

        markdown = f"""#### Cookies
- **Total Cookies**: {len(page.cookies)}
"""
        third_party = [c for c in page.cookies if c.is_third_party]
        if third_party:
            markdown += f"- **Third-party Cookies**: {len(third_party)}\n"

        if hasattr(page, 'cookie_access_analysis'):
            analysis = page.cookie_access_analysis
            if analysis.get('data_collection'):
                markdown += f"- **Data Collection**: {', '.join(analysis['data_collection'][:3])}\n"
            if analysis.get('privacy_concerns'):
                markdown += f"- **Privacy Issues**: {len(analysis['privacy_concerns'])}\n"

        return markdown

    def _generate_page_findings(self, page) -> str:
        """Generate findings for a page."""
        if not hasattr(page, 'dark_patterns') or not page.dark_patterns.findings:
            return ""

        findings = page.dark_patterns.findings
        markdown = f"""#### Findings ({len(findings)})
"""
        for finding in findings:
            severity_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(finding.severity.lower(), '⚪')
            markdown += f"- {severity_emoji} **{finding.pattern}** ({finding.severity}): {finding.description}\n"

        return markdown

    def _generate_page_score(self, page) -> str:
        """Generate score for a page."""
        if not hasattr(page, 'dark_patterns') or not page.dark_patterns.score:
            return ""

        score = page.dark_patterns.score
        grade = score.get('grade', 'N/A')
        total_score = score.get('total_score', 0)
        return f"""#### Score
**{total_score}/100 ({grade})**

"""

    def _generate_summary_table(self, pages, scan_info: Dict[str, Any]) -> str:
        """Generate summary table."""
        if scan_info.get('total_findings', 0) == 0:
            return ""

        markdown = """## Findings Summary

| Pattern | Count | Severity |
|---------|-------|----------|
"""

        pattern_counts = DataConverter.get_pattern_summary(pages)

        for pattern, data in sorted(pattern_counts.items(), key=lambda x: x[1]['count'], reverse=True):
            severity_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(data['severity'].lower(), '⚪')
            markdown += f"| {pattern} | {data['count']} | {severity_emoji} {data['severity']} |\n"

        return markdown

    def get_format(self) -> str:
        """Get report format."""
        return "markdown"
