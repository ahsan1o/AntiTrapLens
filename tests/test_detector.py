"""
Unit tests for the detector module.
"""

import pytest
from antitraplens.detector.rules import DarkPatternDetector

def test_detect_pre_ticked_checkboxes():
    """Test detection of pre-ticked checkboxes."""
    detector = DarkPatternDetector()
    page_data = {
        'forms': [{
            'inputs': [{'type': 'checkbox', 'checked': True, 'name': 'newsletter'}]
        }]
    }
    findings = detector.detect_pre_ticked_checkboxes(page_data)
    assert len(findings) == 1
    assert findings[0]['pattern'] == 'pre_ticked_checkbox'

def test_detect_misleading_buttons():
    """Test detection of misleading buttons."""
    detector = DarkPatternDetector()
    page_data = {
        'buttons': [{'text': 'Cancel Subscribe', 'class': 'btn'}]
    }
    findings = detector.detect_misleading_buttons(page_data)
    assert len(findings) == 1
    assert findings[0]['pattern'] == 'misleading_button'

def test_calculate_score():
    """Test score calculation."""
    detector = DarkPatternDetector()
    findings = [
        {'severity': 'high'},
        {'severity': 'medium'},
        {'severity': 'low'}
    ]
    score = detector.calculate_score(findings)
    assert score['total_score'] == 17  # 10 + 5 + 2
    assert score['grade'] == 'A'

def test_detect_overall():
    """Test overall detection."""
    detector = DarkPatternDetector()
    page_data = {
        'forms': [],
        'popups': [],
        'buttons': [],
        'html': 'some content'
    }
    result = detector.detect(page_data)
    assert 'findings' in result
    assert 'score' in result
