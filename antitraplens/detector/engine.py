"""
Main detector engine for AntiTrapLens.
"""

from typing import List, Dict, Any
from ..core.types import PageData, Finding, DetectionResult
from ..core.config import config
from .base import BaseDetector
from .rules.dark_patterns import DarkPatternRules
from .rules.cookie_analysis import CookieAnalysisRules

class DarkPatternDetector(BaseDetector):
    """Main detector that combines all detection rules."""

    def __init__(self, config=None):
        super().__init__(config)
        self.dark_pattern_rules = DarkPatternRules(self.config)
        self.cookie_rules = CookieAnalysisRules(self.config)

        # Define all detection methods
        self.detection_methods = [
            self.dark_pattern_rules.detect_pre_ticked_checkboxes,
            self.dark_pattern_rules.detect_hidden_unsubscribe,
            self.dark_pattern_rules.detect_overloaded_consent,
            self.dark_pattern_rules.detect_misleading_buttons,
            self.dark_pattern_rules.detect_forced_popups,
            self.dark_pattern_rules.detect_countdown_timers,
            self.dark_pattern_rules.detect_endless_scroll,
            self.dark_pattern_rules.detect_hidden_costs,
            self.dark_pattern_rules.detect_fake_reviews,
            self.dark_pattern_rules.detect_subscription_traps,
            self.dark_pattern_rules.detect_privacy_policy_issues,
            self.dark_pattern_rules.detect_aggressive_ads,
            self.dark_pattern_rules.detect_data_collection,
            self.dark_pattern_rules.detect_accessibility_issues,
            self.cookie_rules.detect_cookie_issues,
            self.cookie_rules.detect_third_party_tracking,
        ]

    def detect(self, page_data: PageData) -> DetectionResult:
        """Run all detection rules on page data."""
        findings = []

        # Run all detection methods
        for method in self.detection_methods:
            try:
                findings.extend(method(page_data))
            except Exception as e:
                # Log error but continue with other detections
                print(f"Error in {method.__name__}: {e}")

        # Calculate score
        score = self._calculate_score(findings)

        return DetectionResult(findings=findings, score=score)

    def get_supported_patterns(self) -> List[str]:
        """Get list of supported dark pattern types."""
        return [
            'pre_ticked_checkbox',
            'hidden_unsubscribe',
            'overloaded_consent',
            'misleading_button',
            'forced_popup',
            'countdown_timer',
            'endless_scroll',
            'hidden_costs',
            'fake_reviews',
            'subscription_trap',
            'privacy_buried',
            'aggressive_ads',
            'data_collection',
            'accessibility_issues',
            'cookie_consent_banner',
            'excessive_cookies',
            'third_party_tracking',
            'tracking_scripts'
        ]

    def _calculate_score(self, findings: List[Finding]) -> Dict[str, Any]:
        """Calculate overall score from findings."""
        severity_weights = self.config.detector.severity_weights
        total_score = sum(severity_weights.get(f.severity, 0) for f in findings)
        max_score = 100
        normalized_score = min(total_score, max_score)

        grade = ('A' if normalized_score < 20 else
                'B' if normalized_score < 40 else
                'C' if normalized_score < 60 else
                'D' if normalized_score < 80 else 'F')

        breakdown = {
            'high': len([f for f in findings if f.severity == 'high']),
            'medium': len([f for f in findings if f.severity == 'medium']),
            'low': len([f for f in findings if f.severity == 'low'])
        }

        return {
            'total_score': normalized_score,
            'grade': grade,
            'breakdown': breakdown
        }
