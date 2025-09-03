#!/usr/bin/env python3
"""
AntiTrapLens CLI - Enhanced Crawler for Dark Pattern Detection
"""

import argparse
import sys
import os
from antitraplens.scraper.crawler import WebCrawler, save_to_json

def main():
    parser = argparse.ArgumentParser(description="AntiTrapLens: Scan websites for dark patterns.")
    parser.add_argument("url", help="The website URL to scan.")
    parser.add_argument("--output", default="reports/scan_result.json", help="Output JSON file path.")
    parser.add_argument("--timeout", type=int, default=30000, help="Timeout in ms for page load.")
    args = parser.parse_args()

    print(f"Scanning {args.url}...")

    with WebCrawler(timeout=args.timeout) as crawler:
        data = crawler.crawl_page(args.url)

    if 'error' in data:
        print(f"Error: {data['error']}")
        sys.exit(1)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    save_to_json(data, args.output)
    print(f"Scan complete. Data saved to {args.output}")
    print(f"Title: {data.get('title', 'N/A')}")
    print(f"Popups detected: {len(data.get('popups', []))}")
    print(f"Forms found: {len(data.get('forms', []))}")

if __name__ == "__main__":
    main()
