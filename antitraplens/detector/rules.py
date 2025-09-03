"""
Detection rules for dark patterns in AntiTrapLens.
"""

from typing import List, Dict, Any
import re
from bs4 import BeautifulSoup
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
            self.detect_hidden_costs,
            self.detect_fake_reviews,
            self.detect_subscription_traps,
            self.detect_privacy_policy_issues,
            self.detect_aggressive_ads,
            self.detect_data_collection,
            self.detect_accessibility_issues,
            self.detect_cookie_issues,
            self.detect_third_party_tracking,
        ]
        self.nlp = spacy.load('en_core_web_sm')
        self.vectorizer = TfidfVectorizer()

    def detect(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Run all detection rules on the page data.
        """
        findings = []
        for rule in self.rules:
            findings.extend(rule(page_data))
        # Add NLP detection
        findings.extend(self.detect_nlp_misleading_text(page_data))
        score = self.calculate_score(findings)
        return {
            'findings': findings,
            'score': score
        }

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

    def detect_hidden_costs(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        html = page_data.get('html', '').lower()
        if re.search(r'\bshipping\b.*\bfree\b', html) and re.search(r'\$\d+', html):
            findings.append({
                'pattern': 'hidden_costs',
                'severity': 'high',
                'description': "Potential hidden costs detected (e.g., shipping fees).",
                'evidence': "HTML mentions 'free shipping' and prices"
            })
        return findings

    def detect_fake_reviews(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        html = page_data.get('html', '').lower()
        if 'review' in html and re.search(r'\b5\s*star\b', html):
            findings.append({
                'pattern': 'fake_reviews',
                'severity': 'medium',
                'description': "Potential fake reviews or exaggerated ratings.",
                'evidence': "HTML contains reviews and high ratings"
            })
        return findings

    def detect_subscription_traps(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        buttons = page_data.get('buttons', [])
        for btn in buttons:
            text = btn.get('text', '').lower()
            if 'free' in text and ('trial' in text or 'subscribe' in text):
                findings.append({
                    'pattern': 'subscription_trap',
                    'severity': 'high',
                    'description': f"Potential subscription trap: '{btn.get('text')}'",
                    'element': btn
                })
        return findings

    def detect_privacy_policy_issues(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        html = page_data.get('html', '').lower()
        if 'privacy' in html and len(html) > 100000:  # Large pages might bury policy
            findings.append({
                'pattern': 'privacy_buried',
                'severity': 'low',
                'description': "Privacy policy might be buried in long page.",
                'evidence': "Large HTML with 'privacy' mention"
            })
        return findings

    def detect_aggressive_ads(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        html = page_data.get('html', '').lower()
        if 'popup' in html or 'overlay' in html:
            findings.append({
                'pattern': 'aggressive_ads',
                'severity': 'medium',
                'description': "Aggressive ads or overlays detected.",
                'evidence': "HTML contains popup/overlay mentions"
            })
        return findings

    def detect_data_collection(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        js_scripts = page_data.get('js_scripts', [])
        if any('analytics' in js.lower() or 'tracking' in js.lower() for js in js_scripts):
            findings.append({
                'pattern': 'data_collection',
                'severity': 'low',
                'description': "Potential extensive data collection via tracking scripts.",
                'evidence': f"JS scripts: {[js for js in js_scripts if 'analytics' in js.lower()]}"
            })
        return findings

    def detect_accessibility_issues(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        html = page_data.get('html', '')
        soup = BeautifulSoup(html, 'lxml')
        images = soup.find_all('img')
        missing_alt = [img for img in images if not img.get('alt')]
        if len(missing_alt) > len(images) * 0.5:
            findings.append({
                'pattern': 'accessibility_issues',
                'severity': 'low',
                'description': f"Many images missing alt text: {len(missing_alt)}/{len(images)}",
                'evidence': "Accessibility concern for screen readers"
            })
        return findings

    def detect_nlp_misleading_text(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        buttons = page_data.get('buttons', [])
        for btn in buttons:
            text = btn.get('text', '').strip()
            if text:
                doc = self.nlp(text.lower())
                # Simple heuristic: check for negation + positive words
                neg_words = ['cancel', 'no', 'stop', 'close']
                pos_words = ['subscribe', 'join', 'yes', 'continue', 'accept']
                has_neg = any(token.lemma_ in neg_words for token in doc)
                has_pos = any(token.lemma_ in pos_words for token in doc)
                if has_neg and has_pos:
                    findings.append({
                        'pattern': 'nlp_misleading_text',
                        'severity': 'high',
                        'description': f"NLP-detected misleading text: '{text}'",
                        'element': btn,
                        'nlp_analysis': f"Contains negation ({has_neg}) and positive action ({has_pos})"
                    })
        return findings

    def detect_cookie_issues(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        cookies = page_data.get('cookies', [])
        html = page_data.get('html', '').lower()
        
        # Check for cookie consent banners
        consent_selectors = [
            '[id*="cookie"]', '[class*="cookie"]', 
            '[id*="consent"]', '[class*="consent"]',
            '[id*="gdpr"]', '[class*="gdpr"]',
            '.cookie-banner', '.consent-banner'
        ]
        
        # Look for cookie-related text in HTML
        cookie_keywords = ['cookie', 'consent', 'privacy', 'tracking', 'analytics']
        has_cookie_banner = any(keyword in html for keyword in cookie_keywords)
        
        if has_cookie_banner:
            findings.append({
                'pattern': 'cookie_consent_banner',
                'severity': 'low',
                'description': "Cookie consent banner detected - review what data sharing is allowed.",
                'evidence': "HTML contains cookie/privacy related terms"
            })
        
        # Check for pre-accepted cookies
        essential_cookies = ['session', 'csrf', 'auth', 'login']
        non_essential_count = 0
        
        for cookie in cookies:
            name = cookie.get('name', '').lower()
            if not any(essential in name for essential in essential_cookies):
                non_essential_count += 1
        
        if non_essential_count > 5:
            findings.append({
                'pattern': 'excessive_cookies',
                'severity': 'medium',
                'description': f"Excessive non-essential cookies detected: {non_essential_count}",
                'evidence': f"Found {len(cookies)} total cookies, {non_essential_count} non-essential"
            })
        
        return findings

    def detect_third_party_tracking(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        cookies = page_data.get('cookies', [])
        js_scripts = page_data.get('js_scripts', [])
        
        # Known tracking domains
        tracking_domains = [
            'google-analytics.com', 'googletagmanager.com', 'doubleclick.net',
            'facebook.com', 'facebook.net', 'twitter.com', 'linkedin.com',
            'hotjar.com', 'mixpanel.com', 'segment.com', 'amplitude.com',
            'crazyegg.com', 'mouseflow.com', 'fullstory.com'
        ]
        
        third_party_cookies = [c for c in cookies if c.get('is_third_party')]
        tracking_cookies = []
        
        for cookie in third_party_cookies:
            domain = cookie.get('domain', '').lower()
            if any(tracker in domain for tracker in tracking_domains):
                tracking_cookies.append(cookie)
        
        if tracking_cookies:
            findings.append({
                'pattern': 'third_party_tracking',
                'severity': 'high',
                'description': f"Third-party tracking cookies detected from {len(tracking_cookies)} domains",
                'evidence': f"Tracking domains: {[c['domain'] for c in tracking_cookies[:5]]}",
                'tracking_cookies': tracking_cookies
            })
        
        # Check for tracking scripts
        tracking_scripts = [js for js in js_scripts if any(tracker in js.lower() for tracker in tracking_domains)]
        if tracking_scripts:
            findings.append({
                'pattern': 'tracking_scripts',
                'severity': 'medium',
                'description': f"Tracking scripts detected: {len(tracking_scripts)}",
                'evidence': f"Scripts from: {[s.split('/')[-1] for s in tracking_scripts[:3]]}"
            })
        
        return findings

    def calculate_score(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        severity_weights = {'high': 10, 'medium': 5, 'low': 2}
        total_score = sum(severity_weights.get(f['severity'], 0) for f in findings)
        max_score = 100
        normalized_score = min(total_score, max_score)
        grade = 'A' if normalized_score < 20 else 'B' if normalized_score < 40 else 'C' if normalized_score < 60 else 'D' if normalized_score < 80 else 'F'
        return {
            'total_score': normalized_score,
            'grade': grade,
            'breakdown': {
                'high': len([f for f in findings if f['severity'] == 'high']),
                'medium': len([f for f in findings if f['severity'] == 'medium']),
                'low': len([f for f in findings if f['severity'] == 'low'])
            }
        }
