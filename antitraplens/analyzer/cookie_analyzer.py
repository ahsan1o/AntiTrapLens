"""
Cookie analysis module for AntiTrapLens.
"""

from typing import Dict, List, Any
from ..core.types import CookieData, PageData
from ..core.config import config

class CookieAnalyzer:
    """Analyzes cookies for privacy and tracking implications."""

    def __init__(self, config=None):
        self.config = config or config.analyzer

    def analyze(self, page_data: PageData) -> Dict[str, Any]:
        """Analyze cookies and their implications."""
        cookies = page_data.cookies

        analysis = {
            'data_collection': [],
            'tracking_capabilities': [],
            'third_party_access': [],
            'privacy_concerns': [],
            'cookie_stats': {
                'total': len(cookies),
                'first_party': len([c for c in cookies if not c.is_third_party]),
                'third_party': len([c for c in cookies if c.is_third_party]),
                'session_cookies': len([c for c in cookies if not c.expires]),
                'persistent_cookies': len([c for c in cookies if c.expires])
            }
        }

        # Analyze data collection
        for cookie in cookies:
            name = cookie.name.lower()

            if any(term in name for term in ['analytics', 'ga', '_gid', '_ga']):
                analysis['data_collection'].append('User behavior analytics')
            elif any(term in name for term in ['fb', 'facebook']):
                analysis['data_collection'].append('Social media tracking')
            elif any(term in name for term in ['ads', 'doubleclick']):
                analysis['data_collection'].append('Advertising targeting')
            elif any(term in name for term in ['session', 'auth', 'login']):
                analysis['data_collection'].append('Session management')
            elif any(term in name for term in ['pref', 'setting']):
                analysis['data_collection'].append('User preferences')

        # Analyze tracking capabilities
        for script in page_data.js_scripts:
            script_lower = script.lower()
            for tracker in self.config.analyzer.tracking_domains:
                if tracker in script_lower:
                    if 'google' in tracker:
                        analysis['tracking_capabilities'].append('Google Analytics - User behavior tracking')
                    elif 'facebook' in tracker:
                        analysis['tracking_capabilities'].append('Facebook Pixel - Social tracking and retargeting')
                    elif 'hotjar' in tracker:
                        analysis['tracking_capabilities'].append('Hotjar - Heatmaps and session recordings')
                    elif 'mixpanel' in tracker:
                        analysis['tracking_capabilities'].append('Mixpanel - Event tracking and user analytics')
                    else:
                        analysis['tracking_capabilities'].append(f'{tracker.title()} - Advanced tracking capabilities')

        # Third-party access
        third_party_domains = set()
        for cookie in cookies:
            if cookie.is_third_party:
                third_party_domains.add(cookie.domain)

        analysis['third_party_access'] = list(third_party_domains)

        # Privacy concerns
        if len(cookies) > 10:
            analysis['privacy_concerns'].append('High number of cookies - extensive data collection')
        if len(third_party_domains) > 5:
            analysis['privacy_concerns'].append('Multiple third-party domains - cross-site tracking')
        if any('advertising' in str(analysis['data_collection']) for item in analysis['data_collection']):
            analysis['privacy_concerns'].append('Advertising cookies - interest-based targeting')
        if len([c for c in cookies if not c.expires]) > 5:
            analysis['privacy_concerns'].append('Many session cookies - continuous tracking')

        # Remove duplicates
        analysis['data_collection'] = list(set(analysis['data_collection']))
        analysis['tracking_capabilities'] = list(set(analysis['tracking_capabilities']))
        analysis['privacy_concerns'] = list(set(analysis['privacy_concerns']))

        return analysis

    def get_cookie_risks(self, page_data: PageData) -> List[Dict[str, Any]]:
        """Get specific cookie-related risks."""
        risks = []
        cookies = page_data.cookies

        # Check for tracking cookies
        tracking_cookies = []
        for cookie in cookies:
            if cookie.is_third_party:
                domain = cookie.domain.lower()
                if any(tracker in domain for tracker in self.config.analyzer.tracking_domains):
                    tracking_cookies.append(cookie)

        if tracking_cookies:
            risks.append({
                'type': 'third_party_tracking',
                'severity': 'high',
                'description': f'Third-party tracking cookies from {len(set(c.domain for c in tracking_cookies))} domains',
                'cookies': tracking_cookies
            })

        # Check for excessive cookies
        non_essential = []
        essential_patterns = ['session', 'csrf', 'auth', 'login', 'security']

        for cookie in cookies:
            if not any(pattern in cookie.name.lower() for pattern in essential_patterns):
                non_essential.append(cookie)

        if len(non_essential) > 5:
            risks.append({
                'type': 'excessive_cookies',
                'severity': 'medium',
                'description': f'Excessive non-essential cookies: {len(non_essential)}',
                'cookies': non_essential[:10]  # Limit for display
            })

        return risks
