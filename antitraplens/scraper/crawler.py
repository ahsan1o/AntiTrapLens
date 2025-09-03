"""
Crawler module for AntiTrapLens.
Handles web page scraping using Playwright.
"""

import json
import logging
from typing import Dict, List, Any
from playwright.sync_api import sync_playwright, Page, Browser
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebCrawler:
    def __init__(self, headless: bool = True, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
        self.browser = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless, args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--disable-gpu'
        ])
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            self.browser.close()
        self.playwright.stop()

    def crawl_page(self, url: str, timeout: int = 60000) -> Dict[str, Any]:
        """
        Crawl the given URL and extract data, with anti-bot measures.
        """
        try:
            context = self.browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                viewport={'width': 1280, 'height': 720}
            )
            page = context.new_page()
            page.goto(url, timeout=timeout, wait_until='networkidle')

            # Wait for potential Cloudflare challenge
            page.wait_for_timeout(5000)  # Wait 5 seconds for challenges

            # Check if it's a challenge page
            if 'challenge' in page.url.lower() or 'just a moment' in page.title().lower():
                logger.info("Detected challenge page, waiting longer...")
                page.wait_for_timeout(10000)  # Wait additional 10 seconds

            # Extract basic HTML
            html = page.content()
            soup = BeautifulSoup(html, 'lxml')

            # Extract title
            title = soup.title.string if soup.title else "No title"

            # Extract meta tags
            meta_tags = []
            for meta in soup.find_all('meta'):
                meta_tags.append({
                    'name': meta.get('name'),
                    'property': meta.get('property'),
                    'content': meta.get('content')
                })

            # Extract CSS links
            css_links = []
            for link in soup.find_all('link', rel='stylesheet'):
                css_links.append(link.get('href'))

            # Extract JS scripts
            js_scripts = []
            for script in soup.find_all('script'):
                if script.get('src'):
                    js_scripts.append(script.get('src'))

            # Detect popups/modals (basic: look for elements with modal classes or high z-index)
            popups = []
            modal_selectors = ['.modal', '.popup', '.overlay', '[role="dialog"]', '.lightbox']
            for selector in modal_selectors:
                elements = page.query_selector_all(selector)
                for el in elements:
                    try:
                        text = el.inner_text()[:200]  # First 200 chars
                        popups.append({
                            'selector': selector,
                            'text': text,
                            'visible': el.is_visible()
                        })
                    except:
                        pass

            # Extract forms (potential for pre-ticked checkboxes)
            forms = []
            for form in soup.find_all('form'):
                inputs = []
                for inp in form.find_all('input'):
                    inputs.append({
                        'type': inp.get('type'),
                        'name': inp.get('name'),
                        'checked': inp.get('checked') == 'checked',
                        'value': inp.get('value')
                    })
                forms.append({
                    'action': form.get('action'),
                    'method': form.get('method'),
                    'inputs': inputs
                })

            # Extract links
            link_elements = page.query_selector_all('a[href]')
            links = []
            for link in link_elements:
                try:
                    href = link.get_attribute('href')
                    if href:
                        full_url = urljoin(url, href)
                        links.append(full_url)
                except:
                    pass

            # Basic JS event listeners (via page evaluation) - REMOVED due to compatibility
            js_events = []  # Placeholder, can add back with alternative method

            data = {
                'url': url,
                'title': title,
                'html_length': len(html),
                'meta_tags': meta_tags,
                'css_links': css_links,
                'js_scripts': js_scripts,
                'popups': popups,
                'forms': forms,
                'js_events': js_events,
                'links': links,
                'timestamp': str(page.evaluate("Date.now()"))
            }

            return data

        except Exception as e:
            logger.error(f"Error crawling {url}: {e}")
            return {'url': url, 'error': str(e)}

    def crawl_with_depth(self, start_url: str, max_depth: int = 1, max_pages: int = 10) -> List[Dict[str, Any]]:
        """
        Crawl the website starting from start_url up to max_depth, collecting data from each page.
        """
        base_domain = urlparse(start_url).netloc
        visited = set()
        queue = deque([(start_url, 0)])  # (url, depth)
        results = []

        while queue and len(results) < max_pages:
            current_url, depth = queue.popleft()
            if current_url in visited or depth > max_depth:
                continue
            visited.add(current_url)

            print(f"Crawling: {current_url} (depth {depth})")
            page_data = self.crawl_page(current_url)
            if 'error' not in page_data:
                # Categorize website and add to data
                data = page_data
                data['category'] = categorize_website(data)
                data['url'] = current_url
                data['status'] = 'success'
                results.append(data)

                if depth < max_depth:
                    # Extract internal links from data
                    links = data.get('links', [])
                    internal_links = []
                    for href in links:
                        full_url = urljoin(current_url, href)
                        if urlparse(full_url).netloc == base_domain and full_url not in visited:
                            internal_links.append(full_url)
                    print(f"Found {len(internal_links)} internal links: {internal_links[:5]}")  # Debug
                    for link in internal_links[:10]:  # Limit to 10 per page to avoid explosion
                        queue.append((link, depth + 1))
            print(f"Queue size: {len(queue)}, Results: {len(results)}")

        return results

def categorize_website(page_data: Dict[str, Any]) -> str:
        """
        Categorize the website based on content analysis.
        """
        title = page_data.get('title', '').lower()
        meta_desc = ''
        for meta in page_data.get('meta_tags', []):
            if meta.get('name') == 'description':
                meta_desc = meta.get('content', '').lower()
                break
        html = page_data.get('html', '').lower()

        # Keywords for categories
        categories = {
            'ecommerce': ['shop', 'buy', 'cart', 'product', 'store', 'price'],
            'adult': ['adult', 'porn', 'sex', 'xxx', 'jav', '18+', 'nude'],
            'streaming': ['watch', 'movie', 'series', 'stream', 'video', 'tv'],
            'news': ['news', 'article', 'blog', 'politics', 'sports'],
            'social': ['social', 'community', 'forum', 'chat'],
            'educational': ['learn', 'course', 'tutorial', 'education'],
            'gaming': ['game', 'play', 'gaming', 'esports'],
        }

        scores = {}
        for cat, keywords in categories.items():
            score = 0
            for kw in keywords:
                if kw in title or kw in meta_desc or kw in html:
                    score += 1
            scores[cat] = score

        # Return category with highest score
        best_cat = max(scores, key=scores.get)
        if scores[best_cat] > 0:
            return best_cat.capitalize()
        return 'General'

def save_to_json(data: Dict[str, Any], filename: str):
    """
    Save extracted data to a JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    logger.info(f"Data saved to {filename}")
