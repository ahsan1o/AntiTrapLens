"""
Console reporter for AntiTrapLens.
"""

from typing import Dict, Any
from rich.console import Console
from rich.table import Table
from ..core.types import ScanResult
from .base import BaseReporter

class ConsoleReporter(BaseReporter):
    """Console-based report generator."""

    def __init__(self, config=None):
        super().__init__(config)
        self.console = Console()

    def generate(self, scan_result: ScanResult, output_path: str = None) -> str:
        """Generate console report."""
        scan_info = scan_result.scan_info
        pages = scan_result.pages

        # Header
        self.console.print(f"\n[bold]=== AntiTrapLens Report ===[/bold]")
        self.console.print(f"Start URL: {scan_info.get('start_url', 'N/A')}")
        self.console.print(f"Pages Scanned: {scan_info.get('pages_scanned', 0)}")
        self.console.print(f"Total Findings: {scan_info.get('total_findings', 0)}")
        self.console.print()

        # Page details
        for i, page in enumerate(pages):
            category = getattr(page, 'category', 'General')
            self.console.print(f"[bold]Page {i+1}:[/bold] {page.url} ([cyan]{category}[/cyan])")

            # Cookie information
            if hasattr(page, 'cookies') and page.cookies:
                self.console.print(f"  Cookies: {len(page.cookies)} total")
                third_party = [c for c in page.cookies if c.is_third_party]
                if third_party:
                    self.console.print(f"    Third-party: {len(third_party)}")

                if hasattr(page, 'cookie_access_analysis'):
                    analysis = page.cookie_access_analysis
                    if analysis.get('data_collection'):
                        self.console.print(f"    Data Collection: {', '.join(analysis['data_collection'][:2])}")
                    if analysis.get('privacy_concerns'):
                        self.console.print(f"    Privacy Issues: {len(analysis['privacy_concerns'])}")

            # Findings
            if hasattr(page, 'dark_patterns') and page.dark_patterns.findings:
                findings = page.dark_patterns.findings
                self.console.print(f"  Findings: {len(findings)}")
                for finding in findings[:3]:  # Show top 3
                    self.console.print(f"    - {finding.pattern} ({finding.severity}): {finding.description}")
                if len(findings) > 3:
                    self.console.print(f"    ... and {len(findings) - 3} more")

            # Score
            if hasattr(page, 'dark_patterns') and page.dark_patterns.score:
                score = page.dark_patterns.score
                grade_color = {'A': 'green', 'B': 'yellow', 'C': 'orange', 'D': 'red', 'F': 'red'}
                color = grade_color.get(score.get('grade', 'F'), 'red')
                self.console.print(f"  Score: [{color}]{score.get('total_score', 0)}/100 ({score.get('grade', 'N/A')})[/{color}]")

            self.console.print()

        # Summary table
        if scan_info.get('total_findings', 0) > 0:
            table = Table(title="Findings Summary")
            table.add_column("Pattern", style="cyan")
            table.add_column("Count", style="magenta")
            table.add_column("Severity", style="red")

            pattern_counts = {}
            for page in pages:
                if hasattr(page, 'dark_patterns'):
                    for finding in page.dark_patterns.findings:
                        key = finding.pattern
                        if key not in pattern_counts:
                            pattern_counts[key] = {'count': 0, 'severity': finding.severity}
                        pattern_counts[key]['count'] += 1

            for pattern, data in sorted(pattern_counts.items(), key=lambda x: x[1]['count'], reverse=True):
                table.add_row(pattern, str(data['count']), data['severity'])

            self.console.print(table)

        return "Console report generated"

    def get_format(self) -> str:
        """Get report format."""
        return "console"
