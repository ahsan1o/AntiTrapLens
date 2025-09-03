#!/usr/bin/env python3
"""
AntiTrapLens CLI - Enhanced Crawler for Dark Pattern Detection
"""

import argparse
import sys
import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table

# Import from new modular structure
from .core.config import AntiTrapLensConfig
from .crawler.playwright_crawler import PlaywrightCrawler
from .detector.engine import DarkPatternDetector
from .analyzer.cookie_analyzer import CookieAnalyzer
from .analyzer.image_analyzer import ImageAnalyzer
from .analyzer.content_analyzer import ContentAnalyzer
from .analyzer.website_categorizer import WebsiteCategorizer
from .reporter.console.reporter import ConsoleReporter
from .reporter.html.reporter import HTMLReporter
from .reporter.json.reporter import JSONReporter
from .reporter.markdown.reporter import MarkdownReporter
from .core.types import ScanResult, PageData

console = Console()

def main():
    parser = argparse.ArgumentParser(description="AntiTrapLens: Scan websites for dark patterns.")
    parser.add_argument("url", help="The website URL to scan.")
    parser.add_argument("--output", default="reports/scan_result.json", help="Output JSON file path.")
    parser.add_argument("--report-format", choices=['json', 'markdown', 'console', 'html'], default='json', help="Report format.")
    parser.add_argument("--report-file", help="Output file for report (if format is not json).")
    parser.add_argument("--timeout", type=int, default=30000, help="Timeout in ms for page load.")
    parser.add_argument("--depth", type=int, default=1, help="Crawling depth (1 = homepage only, 2+ = follow links).")
    parser.add_argument("--max-pages", type=int, default=10, help="Maximum pages to crawl.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
    parser.add_argument("--version", action="version", version="AntiTrapLens 1.0.0")
    args = parser.parse_args()

    console.print(Panel.fit("[bold blue]AntiTrapLens[/bold blue] - Dark Pattern Scanner", border_style="blue"))

    if args.verbose:
        console.print(f"[dim]Scanning {args.url} with depth {args.depth}, timeout {args.timeout}ms[/dim]")

    # Initialize configuration
    config = AntiTrapLensConfig()
    config.crawler.timeout = args.timeout
    config.crawler.retries = 2  # Set some defaults
    # Note: max_pages and depth are handled in the crawler methods

    with console.status("[bold green]Initializing crawler...") as status:
        with PlaywrightCrawler(config) as crawler:
            if args.depth == 1:
                status.update("[bold green]Crawling single page...")
                page_data = crawler.crawl_page(args.url)
                results = [page_data] if page_data else []
            else:
                status.update("[bold green]Crawling with depth...")
                results = crawler.crawl_with_depth(args.url, max_depth=args.depth, max_pages=args.max_pages)

    if not results:
        console.print("[red]No data collected. Check the URL or network connection.[/red]")
        sys.exit(1)

    # Initialize analyzers
    cookie_analyzer = CookieAnalyzer(config)
    image_analyzer = ImageAnalyzer(config)
    content_analyzer = ContentAnalyzer(config)
    detector = DarkPatternDetector(config)
    categorizer = WebsiteCategorizer()

    # Process each page
    processed_pages = []
    all_findings = []

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Analyzing pages...", total=len(results))
        for page in results:
            # Categorize website
            page.category = categorizer.categorize(page)
            
            # Run analyses
            if hasattr(page, 'cookies'):
                page.cookie_access_analysis = cookie_analyzer.analyze(page)
                page.tracking_access = cookie_analyzer.get_tracking_domains_with_access(page)
                page.privacy_assessment = cookie_analyzer.get_privacy_impact_assessment(page)

            if hasattr(page, 'images'):
                page.image_analysis = image_analyzer.analyze(page)

            page.content_analysis = content_analyzer.analyze(page)

            # Detect dark patterns
            detection_result = detector.detect(page)
            page.dark_patterns = detection_result

            processed_pages.append(page)
            all_findings.extend(detection_result.findings)
            progress.advance(task)

    # Create scan result
    scan_result = ScanResult(
        scan_info={
            'start_url': args.url,
            'depth': args.depth,
            'max_pages': args.max_pages,
            'pages_scanned': len(processed_pages),
            'total_findings': len(all_findings),
            'timestamp': None  # Will be set by reporters if needed
        },
        pages=processed_pages
    )

    # Generate report
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    if args.report_format == 'json':
        reporter = JSONReporter(config)
        report_file = args.report_file or args.output
        result = reporter.generate(scan_result, report_file)
        console.print(f"[green]{result}[/green]")
    elif args.report_format == 'markdown':
        reporter = MarkdownReporter(config)
        report_file = args.report_file or args.output.replace('.json', '.md')
        result = reporter.generate(scan_result, report_file)
        console.print(f"[green]{result}[/green]")
    elif args.report_format == 'html':
        reporter = HTMLReporter(config)
        report_file = args.report_file or args.output.replace('.json', '.html')
        result = reporter.generate(scan_result, report_file)
        console.print(f"[green]{result}[/green]")
    elif args.report_format == 'console':
        reporter = ConsoleReporter(config)
        result = reporter.generate(scan_result)
        console.print(f"[green]{result}[/green]")

    # Summary
    table = Table(title="Scan Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("Pages Scanned", str(len(processed_pages)))
    table.add_row("Dark Patterns Found", str(len(all_findings)))
    table.add_row("Scan Depth", str(args.depth))
    console.print(table)

    if all_findings:
        console.print("\n[bold red]Top Findings:[/bold red]")
        for finding in all_findings[:5]:
            console.print(f"• [red]{finding.pattern}[/red] ({finding.severity}): {finding.description}")
        if len(all_findings) > 5:
            console.print(f"[dim]... and {len(all_findings) - 5} more.[/dim]")
    else:
        console.print("[green]No dark patterns detected![/green]")

    if args.verbose and args.depth == 1 and processed_pages:
        page = processed_pages[0]
        console.print(f"\n[bold]Page Details:[/bold]")
        console.print(f"Title: {getattr(page, 'title', 'N/A')}")
        console.print(f"Popups: {len(getattr(page, 'popups', []))}")
        console.print(f"Forms: {len(getattr(page, 'forms', []))}")
        console.print(f"Links: {len(getattr(page, 'links', []))}")
        console.print(f"Images: {len(getattr(page, 'images', []))}")
        console.print(f"Cookies: {len(getattr(page, 'cookies', []))}")

        # Display cookie analysis
        if hasattr(page, 'cookie_access_analysis'):
            analysis = page.cookie_access_analysis
            if analysis.get('data_collection'):
                console.print(f"[yellow]Data Collection: {', '.join(analysis['data_collection'])}[/yellow]")
            if analysis.get('third_party_access'):
                console.print(f"[red]Third-party Access: {len(analysis['third_party_access'])} domains[/red]")
            if analysis.get('tracking_capabilities'):
                console.print(f"[red]Tracking: {len(analysis['tracking_capabilities'])} systems[/red]")
            if analysis.get('privacy_concerns'):
                console.print(f"[red]Privacy Concerns: {len(analysis['privacy_concerns'])}[/red]")

if __name__ == "__main__":
    main()
