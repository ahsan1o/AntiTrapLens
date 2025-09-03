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
import random

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

    def crawl_page(self, url: str, timeout: int = 60000, retries: int = 2) -> Dict[str, Any]:
        """
        Crawl the given URL and extract data, with anti-bot measures and retry logic.
        """
        for attempt in range(retries + 1):
            try:
                context = self.browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    viewport={'width': 1920, 'height': 1080},
                    locale='en-US',
                    timezone_id='America/New_York'
                )
                
                # Add more realistic browser fingerprints
                page = context.new_page()
                
                # Set additional headers to appear more human
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

                # Wait for potential Cloudflare challenge with random delay
                wait_time = random.randint(3000, 8000)  # 3-8 seconds
                page.wait_for_timeout(wait_time)

                # Check if it's a challenge page
                if 'challenge' in page.url.lower() or 'just a moment' in page.title().lower() or 'checking your browser' in page.content().lower():
                    logger.info("Detected challenge page, waiting longer...")
                    page.wait_for_timeout(15000)  # Wait additional 15 seconds

                # Try to scroll to make it look more human
                page.evaluate("window.scrollTo(0, document.body.scrollHeight / 4)")
                page.wait_for_timeout(1000)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
                page.wait_for_timeout(1000)

                # Extract cookies
                cookies = []
                for cookie in context.cookies():
                    cookies.append({
                        'name': cookie.get('name'),
                        'value': cookie.get('value'),
                        'domain': cookie.get('domain'),
                        'path': cookie.get('path'),
                        'expires': cookie.get('expires'),
                        'httpOnly': cookie.get('httpOnly', False),
                        'secure': cookie.get('secure', False),
                        'sameSite': cookie.get('sameSite'),
                        'is_third_party': not urlparse(url).netloc.endswith(cookie.get('domain', '').lstrip('.'))
                    })

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

                # Extract images
                images = []
                for img in soup.find_all('img'):
                    src = img.get('src')
                    alt = img.get('alt', '')
                    if src:
                        full_src = urljoin(url, src)
                        images.append({
                            'src': full_src,
                            'alt': alt,
                            'width': img.get('width'),
                            'height': img.get('height')
                        })

                data = {
                    'url': url,
                    'title': title,
                    'html_length': len(html),
                    'meta_tags': meta_tags,
                    'css_links': css_links,
                    'js_scripts': js_scripts,
                    'popups': popups,
                    'forms': forms,
                    'js_events': [],
                    'links': links,
                    'images': images,
                    'cookies': cookies,
                    'timestamp': str(page.evaluate("Date.now()"))
                }
                
                # Add cookie access analysis
                data['cookie_access_analysis'] = analyze_cookie_access(data)

                context.close()
                return data

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < retries:
                    logger.info(f"Retrying {url} in 5 seconds...")
                    import time
                    time.sleep(5)
                else:
                    logger.error(f"All attempts failed for {url}: {e}")
                    return {'url': url, 'error': str(e)}
            finally:
                try:
                    context.close()
                except:
                    pass

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
        Categorize the website based on content analysis, including images.
        """
        title = page_data.get('title', '').lower()
        meta_desc = ''
        for meta in page_data.get('meta_tags', []):
            if meta.get('name') == 'description':
                meta_desc = meta.get('content', '').lower()
                break
        html = page_data.get('html', '').lower()
        images = page_data.get('images', [])

        # Keywords for categories with more specific adult detection
        categories = {
            'ecommerce': ['shop', 'buy', 'cart', 'product', 'store', 'price', 'sale', 'discount'],
            'adult_streaming': ['adult', 'porn', 'sex', 'xxx', 'jav', '18+', 'nude', 'erotic', 'movie', 'series', 'watch', 'stream', 'episode'],
            'streaming': ['watch', 'movie', 'series', 'stream', 'video', 'tv', 'film', 'netflix', 'amazon prime', 'hulu', 'disney+'],
            'news': ['news', 'article', 'blog', 'politics', 'sports', 'headline', 'breaking'],
            'social': ['social', 'community', 'forum', 'chat', 'profile', 'post', 'like', 'share', 'facebook', 'twitter', 'instagram'],
            'educational': ['learn', 'course', 'tutorial', 'education', 'lesson', 'university', 'school'],
            'gaming': ['game', 'play', 'gaming', 'esports', 'console', 'steam', 'nintendo'],
            'adult_ecommerce': ['adult', 'sex toy', 'lingerie', 'condom', 'vibrator', 'dildo', 'porn', 'erotic'],
        }

        scores = {}
        for cat, keywords in categories.items():
            score = 0
            # Text-based scoring
            for kw in keywords:
                if kw in title or kw in meta_desc or kw in html:
                    score += 1
            # Image-based scoring
            for img in images:
                alt = img.get('alt', '').lower()
                src = img.get('src', '').lower()
                for kw in keywords:
                    if kw in alt or kw in src:
                        score += 0.5  # Weight image keywords less
            scores[cat] = score

        # Additional heuristics based on image count and types
        image_count = len(images)
        if image_count > 20:
            scores['ecommerce'] += 1  # Many images likely e-commerce
            if any('adult' in img.get('alt', '').lower() or 'sex' in img.get('alt', '').lower() for img in images):
                scores['adult_ecommerce'] += 2
        elif image_count < 5:
            scores['news'] += 0.5  # Few images might be news/blog

        # Check for specific image patterns
        product_images = sum(1 for img in images if 'product' in img.get('alt', '').lower() or 'item' in img.get('alt', '').lower())
        if product_images > 5:
            scores['ecommerce'] += 2

        adult_images = sum(1 for img in images if any(term in img.get('alt', '').lower() for term in ['nude', 'sex', 'porn', 'adult', 'erotic']))
        if adult_images > 3:
            scores['adult_streaming'] += 3

        profile_images = sum(1 for img in images if 'profile' in img.get('alt', '').lower() or 'avatar' in img.get('alt', '').lower())
        if profile_images > 3:
            scores['social'] += 2

        # Special handling for adult content
        adult_indicators = ['adult', 'porn', 'sex', 'xxx', '18+', 'nude', 'jav']
        adult_score = sum(1 for indicator in adult_indicators if indicator in title or indicator in meta_desc or indicator in html)
        if adult_score > 0:
            # Boost adult categories
            scores['adult_streaming'] += adult_score * 2
            scores['adult_ecommerce'] += adult_score

        # Return category with highest score
        best_cat = max(scores, key=scores.get)
        if scores[best_cat] > 0:
            return best_cat.replace('_', ' ').title()
        return 'General'

def save_to_json(data: Dict[str, Any], filename: str):
    """
    Save extracted data to a JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    logger.info(f"Data saved to {filename}")

def analyze_cookie_access(page_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze what access websites gain through cookies.
    """
    cookies = page_data.get('cookies', [])
    js_scripts = page_data.get('js_scripts', [])
    
    access_analysis = {
        'data_collection': [],
        'tracking_capabilities': [],
        'third_party_access': [],
        'privacy_concerns': []
    }
    
    # Analyze cookies for data collection
    for cookie in cookies:
        name = cookie.get('name', '').lower()
        domain = cookie.get('domain', '')
        
        if 'analytics' in name or 'ga' in name or '_gid' in name or '_ga' in name:
            access_analysis['data_collection'].append('User behavior analytics')
        elif 'fb' in name or 'facebook' in name:
            access_analysis['data_collection'].append('Social media tracking')
        elif 'ads' in name or 'doubleclick' in name:
            access_analysis['data_collection'].append('Advertising targeting')
        elif 'session' in name or 'auth' in name:
            access_analysis['data_collection'].append('Session management')
        elif 'pref' in name or 'setting' in name:
            access_analysis['data_collection'].append('User preferences')
    
    # Analyze third-party access
    third_party_domains = set()
    for cookie in cookies:
        if cookie.get('is_third_party'):
            domain = cookie.get('domain', '').lstrip('.')
            third_party_domains.add(domain)
    
    access_analysis['third_party_access'] = list(third_party_domains)
    
    # Analyze tracking capabilities
    tracking_indicators = [
        'google-analytics', 'googletagmanager', 'facebook', 'twitter', 'linkedin',
        'hotjar', 'mixpanel', 'segment', 'amplitude', 'crazyegg'
    ]
    
    for script in js_scripts:
        for tracker in tracking_indicators:
            if tracker in script.lower():
                if 'google' in tracker:
                    access_analysis['tracking_capabilities'].append('Google Analytics - User behavior tracking')
                elif 'facebook' in tracker:
                    access_analysis['tracking_capabilities'].append('Facebook Pixel - Social tracking and retargeting')
                elif 'hotjar' in tracker:
                    access_analysis['tracking_capabilities'].append('Hotjar - Heatmaps and session recordings')
                elif 'mixpanel' in tracker:
                    access_analysis['tracking_capabilities'].append('Mixpanel - Event tracking and user analytics')
                else:
                    access_analysis['tracking_capabilities'].append(f'{tracker.title()} - Advanced tracking capabilities')
    
    # Privacy concerns
    if len(cookies) > 10:
        access_analysis['privacy_concerns'].append('High number of cookies - extensive data collection')
    if len(third_party_domains) > 5:
        access_analysis['privacy_concerns'].append('Multiple third-party domains - cross-site tracking')
    if any('advertising' in str(access_analysis['data_collection']) for item in access_analysis['data_collection']):
        access_analysis['privacy_concerns'].append('Advertising cookies - interest-based targeting')
    
    return access_analysis
