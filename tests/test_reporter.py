"""
Unit tests for the reporter module.
"""

import pytest
import os
import json
from unittest.mock import Mock
from antitraplens.reporter import ConsoleReporter, JSONReporter, MarkdownReporter, HTMLReporter
from antitraplens.core.types import ScanResult

def create_mock_scan_result():
    """Create a mock ScanResult for testing."""
    scan_result = Mock(spec=ScanResult)
    scan_result.scan_info = {
        'start_url': 'https://example.com',
        'pages_scanned': 1,
        'total_findings': 1,
        'timestamp': '2024-01-01T00:00:00Z'
    }
    
    # Mock page
    page = Mock()
    page.url = 'https://example.com'
    page.title = 'Test Page'
    page.category = 'General'
    
    # Mock cookies with proper attributes
    cookie = Mock()
    cookie.name = 'test_cookie'
    cookie.domain = 'example.com'
    cookie.path = '/'
    cookie.value = 'test_value'
    cookie.secure = True
    cookie.http_only = False
    cookie.same_site = 'Lax'
    cookie.expires = None
    cookie.is_third_party = False
    cookie.category = 'Essential'
    page.cookies = [cookie]
    
    # Mock cookie analysis
    page.cookie_access_analysis = {
        'data_collection': ['email'],
        'privacy_concerns': ['tracking']
    }
    
    # Mock dark patterns
    finding = Mock()
    finding.pattern = 'test_pattern'
    finding.severity = 'medium'
    finding.description = 'Test finding'
    finding.element = ''
    finding.confidence = 0.8
    finding.evidence = []
    
    dark_patterns = Mock()
    dark_patterns.findings = [finding]
    dark_patterns.score = {'total_score': 50, 'grade': 'C'}
    page.dark_patterns = dark_patterns
    
    scan_result.pages = [page]
    return scan_result

def test_console_reporter(capsys):
    """Test console report generation."""
    reporter = ConsoleReporter()
    scan_result = create_mock_scan_result()
    result = reporter.generate(scan_result)
    
    assert "Console report generated" in result
    captured = capsys.readouterr()
    assert 'AntiTrapLens Report' in captured.out

def test_json_reporter():
    """Test JSON report generation."""
    reporter = JSONReporter()
    scan_result = create_mock_scan_result()
    filename = 'test_report.json'
    result = reporter.generate(scan_result, filename)
    
    assert os.path.exists(filename)
    assert "JSON report saved" in result
    with open(filename, 'r') as f:
        loaded_data = json.load(f)
    assert loaded_data['scan_info']['start_url'] == 'https://example.com'
    
    os.remove(filename)  # Cleanup

def test_markdown_reporter():
    """Test Markdown report generation."""
    reporter = MarkdownReporter()
    scan_result = create_mock_scan_result()
    filename = 'test_report.md'
    result = reporter.generate(scan_result, filename)
    
    assert os.path.exists(filename)
    assert "Markdown report saved" in result
    with open(filename, 'r') as f:
        content = f.read()
    assert 'AntiTrapLens Report' in content
    
    os.remove(filename)  # Cleanup

def test_html_reporter():
    """Test HTML report generation."""
    reporter = HTMLReporter()
    scan_result = create_mock_scan_result()
    filename = 'test_report.html'
    result = reporter.generate(scan_result, filename)
    
    assert os.path.exists(filename)
    assert "HTML report saved" in result
    with open(filename, 'r') as f:
        content = f.read()
    assert 'AntiTrapLens' in content
    assert '<!DOCTYPE html>' in content
    
    os.remove(filename)  # Cleanup
