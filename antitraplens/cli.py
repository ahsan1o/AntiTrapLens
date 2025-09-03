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
from antitraplens.scraper.crawler import WebCrawler, save_to_json
from antitraplens.detector import DarkPatternDetector
from antitraplens.reporter import ReportGenerator

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

    with console.status("[bold green]Initializing crawler...") as status:
        with WebCrawler(timeout=args.timeout) as crawler:
            if args.depth == 1:
                status.update("[bold green]Crawling single page...")
                data = crawler.crawl_page(args.url)
                results = [data] if 'error' not in data else []
            else:
                status.update("[bold green]Crawling with depth...")
                results = crawler.crawl_with_depth(args.url, max_depth=args.depth, max_pages=args.max_pages)

    if not results:
        console.print("[red]No data collected. Check the URL or network connection.[/red]")
        sys.exit(1)

    # Run detection on each page
    detector = DarkPatternDetector()
    reporter = ReportGenerator()
    all_findings = []

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Analyzing pages for dark patterns...", total=len(results))
        for page in results:
            detection_result = detector.detect(page)
            page['dark_patterns'] = detection_result
            all_findings.extend(detection_result['findings'])
            progress.advance(task)

    output_data = {
        'scan_info': {
            'start_url': args.url,
            'depth': args.depth,
            'max_pages': args.max_pages,
            'pages_scanned': len(results),
            'total_findings': len(all_findings)
        },
        'pages': results
    }

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    if args.report_format == 'json':
        reporter.generate_json_report(output_data, args.output)
        console.print(f"[green]JSON report saved to {args.output}[/green]")
    elif args.report_format == 'markdown':
        report_file = args.report_file or args.output.replace('.json', '.md')
        reporter.generate_markdown_report(output_data, report_file)
        console.print(f"[green]Markdown report saved to {report_file}[/green]")
    elif args.report_format == 'html':
        report_file = args.report_file or args.output.replace('.json', '.html')
        reporter.generate_html_report(output_data, report_file)
        console.print(f"[green]HTML report saved to {report_file}[/green]")
    elif args.report_format == 'console':
        reporter.generate_console_report(output_data)

    # Summary
    table = Table(title="Scan Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("Pages Scanned", str(len(results)))
    table.add_row("Dark Patterns Found", str(len(all_findings)))
    table.add_row("Scan Depth", str(args.depth))
    console.print(table)

    if all_findings:
        console.print("\n[bold red]Top Findings:[/bold red]")
        for finding in all_findings[:5]:
            console.print(f"• [red]{finding['pattern']}[/red] ({finding['severity']}): {finding['description']}")
        if len(all_findings) > 5:
            console.print(f"[dim]... and {len(all_findings) - 5} more.[/dim]")
    else:
        console.print("[green]No dark patterns detected![/green]")

    if args.verbose and args.depth == 1 and results:
        page = results[0]
        console.print(f"\n[bold]Page Details:[/bold]")
        console.print(f"Title: {page.get('title', 'N/A')}")
        console.print(f"Popups: {len(page.get('popups', []))}")
        console.print(f"Forms: {len(page.get('forms', []))}")
        console.print(f"Links: {len(page.get('links', []))}")

if __name__ == "__main__":
    main()
