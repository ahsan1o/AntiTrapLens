"""
Unit tests for the reporter module.
"""

import pytest
import os
import json
from antitraplens.reporter.generator import ReportGenerator

def test_generate_json_report():
    """Test JSON report generation."""
    generator = ReportGenerator()
    data = {
        'scan_info': {'start_url': 'https://example.com', 'total_findings': 1},
        'pages': [{'url': 'https://example.com', 'title': 'Test'}]
    }
    filename = 'test_report.json'
    generator.generate_json_report(data, filename)
    
    assert os.path.exists(filename)
    with open(filename, 'r') as f:
        loaded_data = json.load(f)
    assert loaded_data['scan_info']['start_url'] == 'https://example.com'
    
    os.remove(filename)  # Cleanup

def test_generate_markdown_report():
    """Test Markdown report generation."""
    generator = ReportGenerator()
    data = {
        'scan_info': {'start_url': 'https://example.com', 'total_findings': 1},
        'pages': [{'url': 'https://example.com', 'title': 'Test', 'dark_patterns': {'findings': []}}]
    }
    filename = 'test_report.md'
    generator.generate_markdown_report(data, filename)
    
    assert os.path.exists(filename)
    with open(filename, 'r') as f:
        content = f.read()
    assert 'AntiTrapLens Report' in content
    
    os.remove(filename)  # Cleanup

def test_generate_console_report(capsys):
    """Test console report generation."""
    generator = ReportGenerator()
    data = {
        'scan_info': {'start_url': 'https://example.com', 'total_findings': 1},
        'pages': [{'url': 'https://example.com', 'title': 'Test', 'dark_patterns': {'findings': []}}]
    }
    generator.generate_console_report(data)
    
    captured = capsys.readouterr()
    assert 'AntiTrapLens Report' in captured.out
