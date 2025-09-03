"""
Dark pattern detection rules for AntiTrapLens.
"""

from typing import List, Dict, Any
import re
from ...core.types import PageData, Finding
from ...core.config import config

class DarkPatternRules:
    """Collection of dark pattern detection rules."""

    def __init__(self, config=None):
        self.config = config or config.detector

    def detect_pre_ticked_checkboxes(self, page_data: PageData) -> List[Finding]:
        """Detect pre-ticked checkboxes."""
        findings = []
        for form in page_data.forms:
            for inp in form.inputs:
                if inp.get('type') == 'checkbox' and inp.get('checked'):
                    findings.append(Finding(
                        pattern='pre_ticked_checkbox',
                        severity='high',
                        description=f"Pre-ticked checkbox found: {inp.get('name', 'unnamed')}",
                        element=inp
                    ))
        return findings

    def detect_hidden_unsubscribe(self, page_data: PageData) -> List[Finding]:
        """Detect hidden unsubscribe links."""
        findings = []
        html = page_data.html.lower()
        if 'unsubscribe' in html:
            if re.search(r'display:\s*none', html) and 'unsubscribe' in html:
                findings.append(Finding(
                    pattern='hidden_unsubscribe',
                    severity='medium',
                    description="Potential hidden unsubscribe link detected.",
                    evidence="HTML contains 'unsubscribe' with 'display:none'"
                ))
        return findings

    def detect_overloaded_consent(self, page_data: PageData) -> List[Finding]:
        """Detect overloaded consent banners."""
        findings = []
        buttons = []
        for form in page_data.forms:
            for inp in form.inputs:
                if inp.get('type') == 'submit':
                    buttons.append(inp.get('value', '').lower())

        accept_buttons = [b for b in buttons if 'accept' in b or 'agree' in b]
        reject_buttons = [b for b in buttons if 'reject' in b or 'decline' in b or 'no' in b]

        if len(accept_buttons) > len(reject_buttons) and len(page_data.popups) > 0:
            findings.append(Finding(
                pattern='overloaded_consent',
                severity='medium',
                description=f"Overloaded consent banner: {len(accept_buttons)} accept vs {len(reject_buttons)} reject buttons.",
                evidence=f"Popups: {len(page_data.popups)}, Accept buttons: {len(accept_buttons)}"
            ))
        return findings

    def detect_misleading_buttons(self, page_data: PageData) -> List[Finding]:
        """Detect misleading button text."""
        findings = []
        misleading_terms = ['cancel', 'close', 'no thanks']

        for form in page_data.forms:
            for inp in form.inputs:
                if inp.get('type') == 'submit':
                    text = inp.get('value', '').lower()
                    for term in misleading_terms:
                        if term in text and ('subscribe' in text or 'sign up' in text or 'yes' in text):
                            findings.append(Finding(
                                pattern='misleading_button',
                                severity='high',
                                description=f"Misleading button text: '{inp.get('value')}'",
                                element=inp
                            ))
        return findings

    def detect_forced_popups(self, page_data: PageData) -> List[Finding]:
        """Detect forced popups/modals."""
        findings = []
        modal_popups = [p for p in page_data.popups if 'modal' in p.selector.lower()]

        if len(modal_popups) > 0:
            findings.append(Finding(
                pattern='forced_popup',
                severity='medium',
                description=f"Forced popup/modal detected: {len(modal_popups)} modals.",
                evidence=f"Modal selectors: {[p.selector for p in modal_popups]}"
            ))
        return findings

    def detect_countdown_timers(self, page_data: PageData) -> List[Finding]:
        """Detect countdown timers."""
        findings = []
        html = page_data.html.lower()
        if re.search(r'\b\d+\s*(second|minute|hour)', html):
            findings.append(Finding(
                pattern='countdown_timer',
                severity='low',
                description="Countdown timer detected (potential pressure tactic).",
                evidence="HTML contains time-related numbers"
            ))
        return findings

    def detect_endless_scroll(self, page_data: PageData) -> List[Finding]:
        """Detect endless scroll patterns."""
        findings = []
        html = page_data.html.lower()
        if any(term in html for term in ['infinite', 'load more', 'scroll']):
            findings.append(Finding(
                pattern='endless_scroll',
                severity='low',
                description="Potential endless scroll or auto-load detected.",
                evidence="HTML contains scroll/load related terms"
            ))
        return findings

    def detect_hidden_costs(self, page_data: PageData) -> List[Finding]:
        """Detect hidden costs."""
        findings = []
        html = page_data.html.lower()
        if re.search(r'\bshipping\b.*\bfree\b', html) and re.search(r'\$\d+', html):
            findings.append(Finding(
                pattern='hidden_costs',
                severity='high',
                description="Potential hidden costs detected (e.g., shipping fees).",
                evidence="HTML mentions 'free shipping' and prices"
            ))
        return findings

    def detect_fake_reviews(self, page_data: PageData) -> List[Finding]:
        """Detect fake reviews."""
        findings = []
        html = page_data.html.lower()
        if 'review' in html and re.search(r'\b5\s*star\b', html):
            findings.append(Finding(
                pattern='fake_reviews',
                severity='medium',
                description="Potential fake reviews or exaggerated ratings.",
                evidence="HTML contains reviews and high ratings"
            ))
        return findings

    def detect_subscription_traps(self, page_data: PageData) -> List[Finding]:
        """Detect subscription traps."""
        findings = []
        for form in page_data.forms:
            for inp in form.inputs:
                if inp.get('type') == 'submit':
                    text = inp.get('value', '').lower()
                    if 'free' in text and ('trial' in text or 'subscribe' in text):
                        findings.append(Finding(
                            pattern='subscription_trap',
                            severity='high',
                            description=f"Potential subscription trap: '{inp.get('value')}'",
                            element=inp
                        ))
        return findings

    def detect_privacy_policy_issues(self, page_data: PageData) -> List[Finding]:
        """Detect privacy policy issues."""
        findings = []
        html = page_data.html.lower()
        if 'privacy' in html and len(html) > 100000:
            findings.append(Finding(
                pattern='privacy_buried',
                severity='low',
                description="Privacy policy might be buried in long page.",
                evidence="Large HTML with 'privacy' mention"
            ))
        return findings

    def detect_aggressive_ads(self, page_data: PageData) -> List[Finding]:
        """Detect aggressive ads."""
        findings = []
        html = page_data.html.lower()
        if 'popup' in html or 'overlay' in html:
            findings.append(Finding(
                pattern='aggressive_ads',
                severity='medium',
                description="Aggressive ads or overlays detected.",
                evidence="HTML contains popup/overlay mentions"
            ))
        return findings

    def detect_data_collection(self, page_data: PageData) -> List[Finding]:
        """Detect data collection issues."""
        findings = []
        for script in page_data.js_scripts:
            if any(term in script.lower() for term in ['analytics', 'tracking']):
                findings.append(Finding(
                    pattern='data_collection',
                    severity='low',
                    description="Potential extensive data collection via tracking scripts.",
                    evidence=f"Tracking script: {script}"
                ))
        return findings

    def detect_accessibility_issues(self, page_data: PageData) -> List[Finding]:
        """Detect accessibility issues."""
        findings = []
        images_without_alt = len([img for img in page_data.images if not img.alt])
        total_images = len(page_data.images)

        if total_images > 0 and images_without_alt / total_images > 0.5:
            findings.append(Finding(
                pattern='accessibility_issues',
                severity='low',
                description=f"Many images missing alt text: {images_without_alt}/{total_images}",
                evidence="Accessibility concern for screen readers"
            ))
        return findings
