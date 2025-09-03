"""
Console reporter for AntiTrapLens.
"""

from typing import Dict, Any
from rich.console import Console
from rich.table import Table
from ...core.types import ScanResult
from ..base import BaseReporter
from ..common import DataConverter

class ConsoleReporter(BaseReporter):
    """Console-based report generator."""

    def __init__(self, config=None):
        super().__init__(config)
        self.console = Console()

    def generate(self, scan_result: ScanResult, output_path: str = None) -> str:
        """Generate console report."""
        scan_info = scan_result.scan_info
        pages = scan_result.pages

        # Project header
        self.console.print()
        self.console.print("[bold blue]🔍 AntiTrapLens[/bold blue] - Privacy & Dark Pattern Detection Tool")
        self.console.print("[dim]Created by: Ahsan Malik[/dim]")
        self.console.print("[dim]GitHub: https://github.com/ahsan1o/AntiTrapLens[/dim]")
        self.console.print()

        # Header
        self.console.print(f"\n[bold]=== Privacy & Dark Pattern Analysis Report ===[/bold]")
        self.console.print(f"Start URL: {scan_info.get('start_url', 'N/A')}")
        self.console.print(f"Pages Scanned: {scan_info.get('pages_scanned', 0)}")
        self.console.print(f"Total Findings: {scan_info.get('total_findings', 0)}")
        self.console.print()

        # Page details
        for i, page in enumerate(pages):
            category = getattr(page, 'category', 'General')
            title = getattr(page, 'title', 'Untitled Page')
            self.console.print(f"[bold]Page {i+1}:[/bold] {page.url}")
            self.console.print(f"  [cyan]Category:[/cyan] {category}")
            self.console.print(f"  [dim]Title:[/dim] {title}")

            # Dark Patterns Section
            self._print_dark_patterns_section(page)
            
            # Cookies & Tracking Section
            self._print_cookies_section(page)

            self.console.print()

        # Summary tables
        dark_pattern_counts = DataConverter.get_dark_pattern_summary(pages)
        cookie_counts = DataConverter.get_cookie_summary(pages)

        if dark_pattern_counts:
            table = Table(title="🎭 Dark Patterns Summary", caption="Manipulative design elements that trick users into unintended actions")
            table.add_column("Pattern", style="cyan")
            table.add_column("Count", style="magenta")
            table.add_column("Severity", style="red")
            table.add_column("Description", style="dim", max_width=40)

            for pattern, data in sorted(dark_pattern_counts.items(), key=lambda x: x[1]['count'], reverse=True):
                pattern_info = DataConverter.get_pattern_description(pattern)
                severity_color = {'high': 'red', 'medium': 'yellow', 'low': 'green'}.get(data['severity'].lower(), 'white')
                table.add_row(
                    pattern.replace('_', ' ').title(),
                    str(data['count']),
                    f"[{severity_color}]{data['severity'].upper()}[/{severity_color}]",
                    pattern_info['description']
                )

            self.console.print(table)

        if cookie_counts:
            table = Table(title="🍪 Cookie & Tracking Issues Summary", caption="Issues related to how websites track your behavior and collect data")
            table.add_column("Pattern", style="cyan")
            table.add_column("Count", style="magenta")
            table.add_column("Severity", style="red")
            table.add_column("Description", style="dim", max_width=40)

            for pattern, data in sorted(cookie_counts.items(), key=lambda x: x[1]['count'], reverse=True):
                pattern_info = DataConverter.get_pattern_description(pattern)
                severity_color = {'high': 'red', 'medium': 'yellow', 'low': 'green'}.get(data['severity'].lower(), 'white')
                table.add_row(
                    pattern.replace('_', ' ').title(),
                    str(data['count']),
                    f"[{severity_color}]{data['severity'].upper()}[/{severity_color}]",
                    pattern_info['description']
                )

            self.console.print(table)

        return "Console report generated"

    def get_format(self) -> str:
        """Get report format."""
        return "console"

    def _print_dark_patterns_section(self, page):
        """Print dark patterns section for a page with enhanced descriptions."""
        self.console.print(f"  [bold]🎭 Dark Patterns Analysis[/bold]")
        self.console.print(f"  [dim]Dark patterns are manipulative design elements that trick users into unintended actions.[/dim]")
        
        if hasattr(page, 'dark_patterns') and page.dark_patterns.findings:
            # Filter out cookie-related findings
            dark_findings = [f for f in page.dark_patterns.findings 
                            if DataConverter.is_dark_pattern(f.pattern)]
            
            if dark_findings:
                self.console.print(f"  [bold]Findings:[/bold] {len(dark_findings)}")
                for finding in dark_findings[:3]:  # Show top 3
                    pattern_info = DataConverter.get_pattern_description(finding.pattern)
                    severity_color = {'high': 'red', 'medium': 'yellow', 'low': 'green'}.get(finding.severity.lower(), 'white')
                    
                    self.console.print(f"    [{severity_color}]•[/{severity_color}] [bold]{finding.pattern.replace('_', ' ').title()}[/bold] ([{severity_color}]{finding.severity.upper()}[/{severity_color}])")
                    self.console.print(f"      [dim]Detection:[/dim] {finding.description}")
                    self.console.print(f"      [dim]Impact:[/dim] {pattern_info['user_impact']}")
                
                if len(dark_findings) > 3:
                    self.console.print(f"    [dim]... and {len(dark_findings) - 3} more[/dim]")
            else:
                self.console.print(f"  [green]✓[/green] No dark patterns detected")

        # Score
        if hasattr(page, 'dark_patterns') and page.dark_patterns.score:
            score = page.dark_patterns.score
            grade_color = {'A': 'green', 'B': 'yellow', 'C': 'orange', 'D': 'red', 'F': 'red'}
            color = grade_color.get(score.get('grade', 'F'), 'red')
            self.console.print(f"  [bold]Score:[/bold] [{color}]{score.get('total_score', 0)}/100 ({score.get('grade', 'N/A')})[/{color}]")

    def _print_cookies_section(self, page):
        """Print cookies section for a page with enhanced descriptions."""
        self.console.print(f"  [bold]🍪 Cookies & Tracking Analysis[/bold]")
        self.console.print(f"  [dim]Analysis of cookies and tracking mechanisms that monitor your browsing behavior.[/dim]")
        
        # Add tracking warning
        if hasattr(page, 'tracking_access') and page.tracking_access['access_summary']['total_tracking_domains'] > 0:
            tracking = page.tracking_access
            self.console.print(f"  [bold red]⚠️  IMPORTANT:[/bold red] These are the websites that will start tracking you")
            self.console.print(f"  [bold red]   if you give cookie consent on this page![/bold red]")
            self.console.print(f"  [yellow]   → {len(tracking['all_tracking_domains'])} companies will have tracking access[/yellow]")
        
        if hasattr(page, 'cookies') and page.cookies:
            self.console.print(f"  [bold]Cookies Found:[/bold] {len(page.cookies)} total")
            third_party = [c for c in page.cookies if c.is_third_party]
            if third_party:
                self.console.print(f"    Third-party: {len(third_party)}")

            if hasattr(page, 'cookie_access_analysis'):
                analysis = page.cookie_access_analysis
                if analysis.get('data_collection'):
                    self.console.print(f"    Data Collection: {', '.join(analysis['data_collection'][:2])}")
                if analysis.get('privacy_concerns'):
                    self.console.print(f"    Privacy Issues: {len(analysis['privacy_concerns'])}")

        # Cookie findings with descriptions
        if hasattr(page, 'dark_patterns'):
            cookie_findings = [f for f in page.dark_patterns.findings 
                             if DataConverter.is_cookie_tracking_pattern(f.pattern)]
            if cookie_findings:
                self.console.print(f"  [bold]Cookie & Tracking Findings:[/bold] {len(cookie_findings)}")
                for finding in cookie_findings[:2]:  # Show top 2
                    pattern_info = DataConverter.get_pattern_description(finding.pattern)
                    severity_color = {'high': 'red', 'medium': 'yellow', 'low': 'green'}.get(finding.severity.lower(), 'white')
                    
                    self.console.print(f"    [{severity_color}]•[/{severity_color}] [bold]{finding.pattern.replace('_', ' ').title()}[/bold] ([{severity_color}]{finding.severity.upper()}[/{severity_color}])")
                    self.console.print(f"      [dim]Detection:[/dim] {finding.description}")
                    self.console.print(f"      [dim]Impact:[/dim] {pattern_info['user_impact']}")
                
                if len(cookie_findings) > 2:
                    self.console.print(f"    [dim]... and {len(cookie_findings) - 2} more[/dim]")
            else:
                self.console.print(f"  [green]✓[/green] No cookie/tracking issues detected")

    def _print_tracking_access_section(self, page):
        """Print tracking access section showing all domains that will track the user."""
        tracking = page.tracking_access
        
        self.console.print(f"  [bold red]🚨 TRACKING ACCESS GRANTED:[/bold red] {tracking['access_summary']['total_tracking_domains']} domains will track you")
        
        if tracking['cookie_tracking_domains']:
            self.console.print(f"  [bold]Cookie Tracking Domains:[/bold]")
            for domain_info in tracking['cookie_tracking_domains'][:5]:  # Show top 5
                self.console.print(f"    🔴 [red]{domain_info['domain']}[/red] ({domain_info['tracker_type']})")
                self.console.print(f"       Purpose: {domain_info['cookie_purpose']}")
                if domain_info['is_session']:
                    self.console.print(f"       [yellow]⚠️  Session cookie - tracks until browser closes[/yellow]")
                else:
                    self.console.print(f"       [yellow]⚠️  Persistent cookie - long-term tracking[/yellow]")
        
        if tracking['script_tracking_domains']:
            self.console.print(f"  [bold]Script Tracking Domains:[/bold]")
            for script_info in tracking['script_tracking_domains'][:5]:  # Show top 5
                self.console.print(f"    🔴 [red]{script_info['domain']}[/red] ({script_info['tracker_type']})")
                self.console.print(f"       Capabilities: {', '.join(script_info['capabilities'][:3])}")
        
        if len(tracking['all_tracking_domains']) > 10:
            remaining = len(tracking['all_tracking_domains']) - 10
            self.console.print(f"  [dim]... and {remaining} more tracking domains[/dim]")
        
        self.console.print(f"  [bold red]📊 SUMMARY:[/bold red] Your data will be shared with {len(tracking['all_tracking_domains'])} companies")
        self.console.print(f"  [dim]Domains: {', '.join(list(tracking['all_tracking_domains'])[:8])}{'...' if len(tracking['all_tracking_domains']) > 8 else ''}[/dim]")
