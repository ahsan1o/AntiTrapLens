"""
Playwright-based web crawler implementation.
"""

import logging
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright, Browser, Page
from bs4 import BeautifulSoup

from .base import BaseCrawler
from .data_extractor import DataExtractor
from ..core.types import PageData
from ..core.config import config

logger = logging.getLogger(__name__)

class PlaywrightCrawler(BaseCrawler):
    """Playwright-based web crawler with anti-bot measures."""

    def __init__(self, config=None):
        super().__init__(config)
        self.playwright = None
        self.browser = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.config.crawler.headless if self.config else True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu'
            ]
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close browser and playwright."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def crawl_page(self, url: str, **kwargs) -> Optional[PageData]:
        """Crawl a single page with retry logic."""
        timeout = kwargs.get('timeout', self.config.crawler.timeout if self.config else 30000)
        retries = kwargs.get('retries', self.config.crawler.retries if self.config else 2)

        for attempt in range(retries + 1):
            try:
                return self._crawl_single_attempt(url, timeout)
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < retries:
                    logger.info(f"Retrying {url} in 5 seconds...")
                    import time
                    time.sleep(5)
                else:
                    logger.error(f"All attempts failed for {url}: {e}")
                    return None

    def _crawl_single_attempt(self, url: str, timeout: int) -> PageData:
        """Single crawl attempt."""
        context = self.browser.new_context(
            user_agent=self.config.crawler.user_agent if self.config else config.crawler.user_agent,
            viewport=self.config.crawler.viewport if self.config else config.crawler.viewport,
            locale='en-US',
            timezone_id='America/New_York'
        )

        page = context.new_page()

        # Set additional headers
        page.set_extra_http_headers({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        })

        page.goto(url, timeout=timeout, wait_until='domcontentloaded')

        # Wait for potential challenges
        import random
        wait_time = random.randint(3000, 8000)
        page.wait_for_timeout(wait_time)

        # Check for challenge pages
        if 'challenge' in page.url.lower() or 'just a moment' in page.title().lower() or 'checking your browser' in page.content().lower():
            logger.info("Detected challenge page, waiting longer...")
            page.wait_for_timeout(15000)

        # Human-like scrolling
        page.evaluate("window.scrollTo(0, document.body.scrollHeight / 4)")
        page.wait_for_timeout(1000)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        page.wait_for_timeout(1000)

        # Extract data
        html = page.content()
        soup = BeautifulSoup(html, 'lxml')

        # Extract all data
        base_domain = urlparse(url).netloc

        page_data = PageData(
            url=url,
            title=soup.title.string if soup.title else "No title",
            html=html,
            html_length=len(html),
            meta_tags=DataExtractor.extract_meta_tags(soup),
            css_links=DataExtractor.extract_css_links(soup),
            js_scripts=DataExtractor.extract_js_scripts(soup),
            popups=DataExtractor.extract_popups(page, ['.modal', '.popup', '.overlay', '[role="dialog"]', '.lightbox']),
            forms=DataExtractor.extract_forms(soup),
            links=DataExtractor.extract_links(page, url),
            images=DataExtractor.extract_images(soup, url),
            cookies=DataExtractor.extract_cookies(context.cookies(), base_domain),
            timestamp=str(page.evaluate("Date.now()"))
        )

        context.close()
        return page_data

    def crawl_with_depth(self, start_url: str, max_depth: int = 1, max_pages: int = 10) -> List[PageData]:
        """Crawl with depth (simplified implementation)."""
        results = []
        visited = set()
        queue = [(start_url, 0)]  # (url, depth)

        while queue and len(results) < max_pages:
            current_url, depth = queue.pop(0)
            if current_url in visited or depth > max_depth:
                continue
            visited.add(current_url)

            page_data = self.crawl_page(current_url)
            if page_data:
                results.append(page_data)

                if depth < max_depth:
                    # Add internal links to queue
                    base_domain = urlparse(start_url).netloc
                    for link in page_data.links[:10]:  # Limit links
                        if urlparse(link).netloc == base_domain and link not in visited:
                            queue.append((link, depth + 1))

        return results
