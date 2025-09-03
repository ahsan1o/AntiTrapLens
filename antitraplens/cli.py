#!/usr/bin/env python3
"""
AntiTrapLens CLI - Basic Crawler for Dark Pattern Detection
"""

import argparse
import sys
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def crawl_page(url: str) -> str:
    """
    Crawl the given URL using Playwright and return the HTML content.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=30000)
            html = page.content()
            return html
        except Exception as e:
            print(f"Error loading page: {e}")
            return ""
        finally:
            browser.close()

def main():
    parser = argparse.ArgumentParser(description="AntiTrapLens: Scan websites for dark patterns.")
    parser.add_argument("url", help="The website URL to scan.")
    args = parser.parse_args()

    print(f"Scanning {args.url}...")
    html = crawl_page(args.url)
    if html:
        soup = BeautifulSoup(html, 'lxml')
        print("Page title:", soup.title.string if soup.title else "No title")
        print("HTML length:", len(html))
        print("Basic extraction complete. (Expand in next phases)")
    else:
        print("Failed to crawl the page.")
        sys.exit(1)

if __name__ == "__main__":
    main()
