"""
Detection rules for dark patterns in AntiTrapLens.
"""

from typing import List, Dict, Any
import re

class DarkPatternDetector:
    def __init__(self):
        self.rules = [
            self.detect_pre_ticked_checkboxes,
            self.detect_hidden_unsubscribe,
            self.detect_overloaded_consent,
            self.detect_misleading_buttons,
            self.detect_forced_popups,
            self.detect_countdown_timers,
            self.detect_endless_scroll,
        ]

    def detect(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Run all detection rules on the page data.
        """
        findings = []
        for rule in self.rules:
            findings.extend(rule(page_data))
        return findings

    def detect_pre_ticked_checkboxes(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        forms = page_data.get('forms', [])
        for form in forms:
            for inp in form.get('inputs', []):
                if inp.get('type') == 'checkbox' and inp.get('checked'):
                    findings.append({
                        'pattern': 'pre_ticked_checkbox',
                        'severity': 'high',
                        'description': f"Pre-ticked checkbox found: {inp.get('name', 'unnamed')}",
                        'element': inp
                    })
        return findings

    def detect_hidden_unsubscribe(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        html = page_data.get('html', '').lower()
        if 'unsubscribe' in html:
            # Check for hidden elements (simple regex)
            if re.search(r'display:\s*none', html) and 'unsubscribe' in html:
                findings.append({
                    'pattern': 'hidden_unsubscribe',
                    'severity': 'medium',
                    'description': "Potential hidden unsubscribe link detected.",
                    'evidence': "HTML contains 'unsubscribe' with 'display:none'"
                })
        return findings

    def detect_overloaded_consent(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        popups = page_data.get('popups', [])
        buttons = page_data.get('buttons', [])
        accept_buttons = [b for b in buttons if 'accept' in b.get('text', '').lower()]
        reject_buttons = [b for b in buttons if 'reject' in b.get('text', '').lower() or 'decline' in b.get('text', '').lower()]
        if len(accept_buttons) > len(reject_buttons) and len(popups) > 0:
            findings.append({
                'pattern': 'overloaded_consent',
                'severity': 'medium',
                'description': f"Overloaded consent banner: {len(accept_buttons)} accept vs {len(reject_buttons)} reject buttons.",
                'evidence': f"Popups: {len(popups)}, Accept buttons: {len(accept_buttons)}"
            })
        return findings

    def detect_misleading_buttons(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        buttons = page_data.get('buttons', [])
        misleading_terms = ['cancel', 'close', 'no thanks']
        for btn in buttons:
            text = btn.get('text', '').lower()
            for term in misleading_terms:
                if term in text and ('subscribe' in text or 'sign up' in text or 'yes' in text):
                    findings.append({
                        'pattern': 'misleading_button',
                        'severity': 'high',
                        'description': f"Misleading button text: '{btn.get('text')}'",
                        'element': btn
                    })
        return findings

    def detect_forced_popups(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        popups = page_data.get('popups', [])
        if len(popups) > 0:
            # Check if popup blocks interaction (simple: if many popups or modal class)
            modal_popups = [p for p in popups if 'modal' in p.get('selector', '').lower()]
            if len(modal_popups) > 0:
                findings.append({
                    'pattern': 'forced_popup',
                    'severity': 'medium',
                    'description': f"Forced popup/modal detected: {len(modal_popups)} modals.",
                    'evidence': f"Modal selectors: {[p['selector'] for p in modal_popups]}"
                })
        return findings

    def detect_countdown_timers(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        html = page_data.get('html', '').lower()
        if re.search(r'\b\d+\s*(second|minute|hour)', html):
            findings.append({
                'pattern': 'countdown_timer',
                'severity': 'low',
                'description': "Countdown timer detected (potential pressure tactic).",
                'evidence': "HTML contains time-related numbers"
            })
        return findings

    def detect_endless_scroll(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        js_scripts = page_data.get('js_scripts', [])
        html = page_data.get('html', '').lower()
        if any('scroll' in js.lower() for js in js_scripts) or 'infinite' in html or 'load more' in html:
            findings.append({
                'pattern': 'endless_scroll',
                'severity': 'low',
                'description': "Potential endless scroll or auto-load detected.",
                'evidence': "JS scripts or HTML mention scroll/load"
            })
        return findings
