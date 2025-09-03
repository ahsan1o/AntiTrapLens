#!/usr/bin/env python3
"""
AntiTrapLens CLI - Enhanced Crawler for Dark Pattern Detection
"""

import argparse
import sys
import os
from antitraplens.scraper.crawler import WebCrawler, save_to_json
from antitraplens.detector import DarkPatternDetector

def main():
    parser = argparse.ArgumentParser(description="AntiTrapLens: Scan websites for dark patterns.")
    parser.add_argument("url", help="The website URL to scan.")
    parser.add_argument("--output", default="reports/scan_result.json", help="Output JSON file path.")
    parser.add_argument("--timeout", type=int, default=30000, help="Timeout in ms for page load.")
    parser.add_argument("--depth", type=int, default=1, help="Crawling depth (1 = homepage only, 2+ = follow links).")
    parser.add_argument("--max-pages", type=int, default=10, help="Maximum pages to crawl.")
    args = parser.parse_args()

    print(f"Scanning {args.url}...")

    with WebCrawler(timeout=args.timeout) as crawler:
        if args.depth == 1:
            data = crawler.crawl_page(args.url)
            results = [data] if 'error' not in data else []
        else:
            results = crawler.crawl_with_depth(args.url, max_depth=args.depth, max_pages=args.max_pages)

    if not results:
        print("No data collected.")
        sys.exit(1)

    # Run detection on each page
    detector = DarkPatternDetector()
    all_findings = []
    for page in results:
        findings = detector.detect(page)
        page['dark_patterns'] = findings
        all_findings.extend(findings)

    # Save all results
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
    save_to_json(output_data, args.output)
    print(f"Scan complete. {len(results)} pages scanned. {len(all_findings)} dark patterns found. Data saved to {args.output}")
    if all_findings:
        print("Findings:")
        for finding in all_findings[:5]:  # Show first 5
            print(f"- {finding['pattern']}: {finding['description']} (Severity: {finding['severity']})")
        if len(all_findings) > 5:
            print(f"... and {len(all_findings) - 5} more.")
    if args.depth == 1 and results:
        print(f"Title: {results[0].get('title', 'N/A')}")
        print(f"Popups detected: {len(results[0].get('popups', []))}")
        print(f"Forms found: {len(results[0].get('forms', []))}")

if __name__ == "__main__":
    main()
