"""
Crawler module for AntiTrapLens.
Handles web page scraping using Playwright.
"""

import json
import logging
from typing import Dict, List, Any
from playwright.sync_api import sync_playwright, Page, Browser
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebCrawler:
    def __init__(self, headless: bool = True, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
        self.browser = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            self.browser.close()
        self.playwright.stop()

    def crawl_page(self, url: str) -> Dict[str, Any]:
        """
        Crawl a single page and extract relevant data.
        """
        try:
            page = self.browser.new_page()
            page.goto(url, timeout=self.timeout)

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
                'timestamp': str(page.evaluate("Date.now()"))
            }

            page.close()
            return data

        except Exception as e:
            logger.error(f"Error crawling {url}: {e}")
            return {'url': url, 'error': str(e)}

def save_to_json(data: Dict[str, Any], filename: str):
    """
    Save extracted data to a JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    logger.info(f"Data saved to {filename}")
