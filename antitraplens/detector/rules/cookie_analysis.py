"""
Cookie analysis detection rules for AntiTrapLens.
"""

from typing import List
from ...core.types import PageData, Finding
from ...analyzer.cookie_analyzer import CookieAnalyzer

class CookieAnalysisRules:
    """Cookie-related dark pattern detection rules."""

    def __init__(self, config=None):
        self.cookie_analyzer = CookieAnalyzer(config)

    def detect_cookie_issues(self, page_data: PageData) -> List[Finding]:
        """Detect cookie consent and privacy issues."""
        findings = []
        html = page_data.html.lower()

        # Check for cookie consent banners
        consent_keywords = ['cookie', 'consent', 'privacy', 'tracking', 'gdpr', 'ccpa']
        has_consent_banner = any(keyword in html for keyword in consent_keywords)

        if has_consent_banner:
            findings.append(Finding(
                pattern='cookie_consent_banner',
                severity='low',
                description="Cookie consent banner detected - review what data sharing is allowed.",
                evidence="HTML contains cookie/privacy related terms"
            ))

        # Check for excessive cookies
        cookie_risks = self.cookie_analyzer.get_cookie_risks(page_data)
        for risk in cookie_risks:
            findings.append(Finding(
                pattern=risk['type'],
                severity=risk['severity'],
                description=risk['description'],
                evidence=f"Cookies involved: {len(risk.get('cookies', []))}"
            ))

        return findings

    def detect_third_party_tracking(self, page_data: PageData) -> List[Finding]:
        """Detect third-party tracking cookies."""
        findings = []
        cookie_analysis = self.cookie_analyzer.analyze(page_data)

        if cookie_analysis['third_party_access']:
            findings.append(Finding(
                pattern='third_party_tracking',
                severity='high',
                description=f"Third-party tracking detected from {len(cookie_analysis['third_party_access'])} domains",
                evidence=f"Domains: {', '.join(cookie_analysis['third_party_access'][:5])}"
            ))

        if cookie_analysis['tracking_capabilities']:
            findings.append(Finding(
                pattern='tracking_scripts',
                severity='medium',
                description=f"Tracking scripts detected: {len(cookie_analysis['tracking_capabilities'])} systems",
                evidence=f"Systems: {', '.join(cookie_analysis['tracking_capabilities'][:3])}"
            ))

        return findings
