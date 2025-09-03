"""
Data extraction utilities for web crawling.
"""

from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from ..core.types import CookieData, ImageData, FormData, PopupData, MetaTagData

class DataExtractor:
    """Utility class for extracting data from web pages."""

    @staticmethod
    def extract_meta_tags(soup: BeautifulSoup) -> List[MetaTagData]:
        """Extract meta tags from soup."""
        meta_tags = []
        for meta in soup.find_all('meta'):
            meta_tags.append(MetaTagData(
                name=meta.get('name'),
                property=meta.get('property'),
                content=meta.get('content')
            ))
        return meta_tags

    @staticmethod
    def extract_css_links(soup: BeautifulSoup) -> List[str]:
        """Extract CSS links from soup."""
        css_links = []
        for link in soup.find_all('link', rel='stylesheet'):
            if link.get('href'):
                css_links.append(link.get('href'))
        return css_links

    @staticmethod
    def extract_js_scripts(soup: BeautifulSoup) -> List[str]:
        """Extract JavaScript scripts from soup."""
        js_scripts = []
        for script in soup.find_all('script'):
            if script.get('src'):
                js_scripts.append(script.get('src'))
        return js_scripts

    @staticmethod
    def extract_forms(soup: BeautifulSoup) -> List[FormData]:
        """Extract forms from soup."""
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
            forms.append(FormData(
                action=form.get('action'),
                method=form.get('method', 'get'),
                inputs=inputs
            ))
        return forms

    @staticmethod
    def extract_images(soup: BeautifulSoup, base_url: str) -> List[ImageData]:
        """Extract images from soup."""
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                full_src = urljoin(base_url, src)
                images.append(ImageData(
                    src=full_src,
                    alt=img.get('alt', ''),
                    width=img.get('width'),
                    height=img.get('height')
                ))
        return images

    @staticmethod
    def extract_cookies(context_cookies: List[Dict[str, Any]], base_domain: str) -> List[CookieData]:
        """Extract and analyze cookies."""
        cookies = []
        for cookie in context_cookies:
            domain = cookie.get('domain', '').lstrip('.')
            is_third_party = not base_domain.endswith(domain)

            cookies.append(CookieData(
                name=cookie.get('name', ''),
                value=cookie.get('value', ''),
                domain=domain,
                path=cookie.get('path', ''),
                expires=cookie.get('expires'),
                httpOnly=cookie.get('httpOnly', False),
                secure=cookie.get('secure', False),
                sameSite=cookie.get('sameSite'),
                is_third_party=is_third_party
            ))
        return cookies

    @staticmethod
    def extract_popups(page, selectors: List[str]) -> List[PopupData]:
        """Extract popup/modal elements."""
        popups = []
        for selector in selectors:
            elements = page.query_selector_all(selector)
            for el in elements:
                try:
                    text = el.inner_text()[:200]
                    popups.append(PopupData(
                        selector=selector,
                        text=text,
                        visible=el.is_visible()
                    ))
                except:
                    pass
        return popups

    @staticmethod
    def extract_links(page, base_url: str) -> List[str]:
        """Extract all links from page."""
        links = []
        link_elements = page.query_selector_all('a[href]')
        for link in link_elements:
            try:
                href = link.get_attribute('href')
                if href:
                    full_url = urljoin(base_url, href)
                    links.append(full_url)
            except:
                pass
        return links
