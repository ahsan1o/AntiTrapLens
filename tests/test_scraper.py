"""
Unit tests for the scraper module.
"""

import pytest
from unittest.mock import Mock, patch
from antitraplens.scraper.crawler import WebCrawler, categorize_website

def test_categorize_website_adult():
    """Test categorization for adult content."""
    page_data = {
        'title': 'Adult Movies',
        'html': 'watch adult porn jav 18+',
        'meta_tags': [{'name': 'description', 'content': 'adult content'}]
    }
    category = categorize_website(page_data)
    assert category == 'Adult'

def test_categorize_website_ecommerce():
    """Test categorization for ecommerce."""
    page_data = {
        'title': 'Shop Online',
        'html': 'buy products cart store',
        'meta_tags': [{'name': 'description', 'content': 'ecommerce site'}]
    }
    category = categorize_website(page_data)
    assert category == 'Ecommerce'

def test_categorize_website_general():
    """Test categorization fallback to general."""
    page_data = {
        'title': 'Random Site',
        'html': 'some content',
        'meta_tags': []
    }
    category = categorize_website(page_data)
    assert category == 'General'

@patch('antitraplens.scraper.crawler.sync_playwright')
def test_crawl_page_success(mock_playwright):
    """Test successful page crawl."""
    # Set up mocks properly
    mock_started = Mock()
    mock_chromium = Mock()
    mock_browser = Mock()
    mock_context = Mock()
    mock_page = Mock()
    
    mock_playwright.return_value.start.return_value = mock_started
    mock_started.chromium = mock_chromium
    mock_chromium.launch.return_value = mock_browser
    mock_browser.new_context.return_value = mock_context
    mock_context.new_page.return_value = mock_page
    
    # Mock page methods
    mock_page.content.return_value = '<html><title>Test</title></html>'
    mock_page.title.return_value = 'Test'
    mock_page.query_selector_all.return_value = []
    mock_page.evaluate.return_value = 1234567890
    mock_page.url = 'https://example.com'
    mock_page.goto = Mock()
    mock_page.wait_for_timeout = Mock()
    
    # Mock BeautifulSoup
    with patch('antitraplens.scraper.crawler.BeautifulSoup') as mock_bs:
        mock_soup = Mock()
        mock_soup.title.string = 'Test'
        mock_soup.find_all.return_value = []
        mock_bs.return_value = mock_soup
        
        with WebCrawler() as crawler:
            data = crawler.crawl_page('https://example.com')
    
    assert 'status' not in data  # Since it's success, no status key
    assert data['title'] == 'Test'

@patch('antitraplens.scraper.crawler.sync_playwright')
def test_crawl_page_error(mock_playwright):
    """Test page crawl with error."""
    # Set up mocks properly
    mock_started = Mock()
    mock_chromium = Mock()
    mock_browser = Mock()
    mock_context = Mock()
    mock_page = Mock()
    
    mock_playwright.return_value.start.return_value = mock_started
    mock_started.chromium = mock_chromium
    mock_chromium.launch.return_value = mock_browser
    mock_browser.new_context.return_value = mock_context
    mock_context.new_page.return_value = mock_page
    
    # Mock page to raise exception
    mock_page.goto.side_effect = Exception('Timeout')
    
    with WebCrawler() as crawler:
        data = crawler.crawl_page('https://example.com')
    
    assert 'error' in data
    assert data['error'] == 'Timeout'
