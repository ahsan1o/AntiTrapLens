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

    def get_tracking_domains_with_access(self, page_data: PageData) -> Dict[str, Any]:
        """Get comprehensive list of domains that will have tracking access."""
        cookies = page_data.cookies
        js_scripts = page_data.js_scripts
        
        tracking_access = {
            'cookie_tracking_domains': [],
            'script_tracking_domains': [],
            'all_tracking_domains': set(),
            'access_summary': {},
            'potential_trackers': []  # New: All third-party domains
        }
        
        # Get ALL third-party domains (potential trackers)
        all_third_party_domains = set()
        for cookie in cookies:
            if cookie.is_third_party:
                all_third_party_domains.add(cookie.domain.lower())
        
        # Analyze each third-party domain for tracking likelihood
        for domain in all_third_party_domains:
            is_known_tracker = any(tracker in domain for tracker in self.config.analyzer.tracking_domains)
            tracking_likelihood = self._assess_tracking_likelihood(domain, cookies, js_scripts)
            
            tracker_info = {
                'domain': domain,
                'is_known_tracker': is_known_tracker,
                'tracking_likelihood': tracking_likelihood,
                'tracker_type': self._identify_tracker_type(domain) if is_known_tracker else 'Potential Tracker',
                'cookie_count': len([c for c in cookies if c.domain.lower() == domain]),
                'has_scripts': any(domain in script.lower() for script in js_scripts),
                'risk_level': self._calculate_risk_level(domain, cookies, tracking_likelihood)
            }
            
            tracking_access['potential_trackers'].append(tracker_info)
            tracking_access['all_tracking_domains'].add(domain)
            
            # If it's a known tracker or high likelihood, add to specific tracking lists
            if is_known_tracker or tracking_likelihood > 0.7:
                # Add cookie tracking info
                domain_cookies = [c for c in cookies if c.domain.lower() == domain]
                for cookie in domain_cookies[:3]:  # Limit to first 3 cookies per domain
                    cookie_info = {
                        'domain': cookie.domain,
                        'tracker_type': tracker_info['tracker_type'],
                        'cookie_name': cookie.name,
                        'cookie_purpose': self._identify_cookie_purpose(cookie.name),
                        'expires': cookie.expires,
                        'is_session': not cookie.expires,
                        'tracking_likelihood': tracking_likelihood
                    }
                    tracking_access['cookie_tracking_domains'].append(cookie_info)
        
        # Get domains loading tracking scripts
        for script in js_scripts:
            script_lower = script.lower()
            for tracker in self.config.analyzer.tracking_domains:
                if tracker in script_lower:
                    script_info = {
                        'domain': tracker,
                        'tracker_type': self._identify_tracker_type(tracker),
                        'script_url': script[:100] + '...' if len(script) > 100 else script,
                        'capabilities': self._get_tracker_capabilities(tracker),
                        'tracking_likelihood': 1.0  # Known trackers from scripts are definite
                    }
                    tracking_access['script_tracking_domains'].append(script_info)
                    tracking_access['all_tracking_domains'].add(tracker)
                    break
        
        # Create access summary
        tracking_access['access_summary'] = {
            'total_tracking_domains': len(tracking_access['all_tracking_domains']),
            'known_trackers': len([t for t in tracking_access['potential_trackers'] if t['is_known_tracker']]),
            'potential_trackers': len([t for t in tracking_access['potential_trackers'] if not t['is_known_tracker']]),
            'high_risk_domains': len([t for t in tracking_access['potential_trackers'] if t['risk_level'] == 'high']),
            'cookie_domains': len(set(d['domain'] for d in tracking_access['cookie_tracking_domains'])),
            'script_domains': len(set(d['domain'] for d in tracking_access['script_tracking_domains'])),
            'data_shared_with': list(tracking_access['all_tracking_domains'])
        }
        
        # Remove duplicates from lists
        tracking_access['cookie_tracking_domains'] = self._remove_duplicate_domains(tracking_access['cookie_tracking_domains'])
        tracking_access['script_tracking_domains'] = self._remove_duplicate_domains(tracking_access['script_tracking_domains'])
        tracking_access['potential_trackers'] = self._remove_duplicate_domains(tracking_access['potential_trackers'])
        
        return tracking_access
    
    def _identify_tracker_type(self, tracker: str) -> str:
        """Identify the type of tracker based on domain."""
        tracker = tracker.lower()
        if 'google' in tracker:
            return 'Analytics & Advertising'
        elif 'facebook' in tracker:
            return 'Social Media & Advertising'
        elif 'twitter' in tracker or 'linkedin' in tracker:
            return 'Social Media'
        elif 'hotjar' in tracker:
            return 'User Experience Analytics'
        elif 'mixpanel' in tracker or 'amplitude' in tracker:
            return 'Product Analytics'
        elif 'segment' in tracker:
            return 'Customer Data Platform'
        elif 'doubleclick' in tracker:
            return 'Advertising'
        else:
            return 'Tracking & Analytics'
    
    def _identify_cookie_purpose(self, cookie_name: str) -> str:
        """Identify the purpose of a tracking cookie."""
        name = cookie_name.lower()
        if any(term in name for term in ['_ga', '_gid', '_gat']):
            return 'Google Analytics - User behavior tracking'
        elif 'fbp' in name or 'fbc' in name:
            return 'Facebook Pixel - Social tracking and retargeting'
        elif 'twclid' in name:
            return 'Twitter - Click tracking'
        elif '_hj' in name:
            return 'Hotjar - Session recording'
        elif 'mp_' in name:
            return 'Mixpanel - Event tracking'
        else:
            return 'General tracking and analytics'
    
    def _get_tracker_capabilities(self, tracker: str) -> List[str]:
        """Get the tracking capabilities of a domain."""
        tracker = tracker.lower()
        capabilities = []
        
        if 'google' in tracker:
            capabilities.extend(['User behavior analytics', 'Conversion tracking', 'Audience targeting', 'Cross-device tracking'])
        elif 'facebook' in tracker:
            capabilities.extend(['Social interactions', 'Retargeting ads', 'Audience building', 'Conversion tracking'])
        elif 'twitter' in tracker:
            capabilities.extend(['Social engagement', 'Retargeting', 'Audience insights'])
        elif 'hotjar' in tracker:
            capabilities.extend(['Heatmaps', 'Session recordings', 'User feedback', 'Conversion funnels'])
        elif 'mixpanel' in tracker:
            capabilities.extend(['Event tracking', 'User segmentation', 'A/B testing', 'Retention analysis'])
        elif 'doubleclick' in tracker:
            capabilities.extend(['Advertising targeting', 'Conversion tracking', 'Remarketing'])
        else:
            capabilities.append('Advanced tracking and analytics')
        
        return capabilities
    
    def _remove_duplicate_domains(self, domain_list: List[Dict]) -> List[Dict]:
        """Remove duplicate domains from list while preserving the most detailed info."""
        seen_domains = set()
        unique_list = []
        
        for item in domain_list:
            domain = item.get('domain', item.get('tracker_domain', ''))
            if domain and domain not in seen_domains:
                seen_domains.add(domain)
                unique_list.append(item)
        
        return unique_list
    
    def _assess_tracking_likelihood(self, domain: str, cookies: List[CookieData], js_scripts: List[str]) -> float:
        """Assess how likely a domain is to be tracking based on various heuristics."""
        likelihood = 0.0
        domain_lower = domain.lower()
        
        # Check if it's a known tracking domain
        if any(tracker in domain_lower for tracker in self.config.analyzer.tracking_domains):
            likelihood += 1.0
        
        # Check cookie names for tracking patterns
        domain_cookies = [c for c in cookies if c.domain.lower() == domain_lower]
        tracking_cookie_patterns = [
            '_ga', '_gid', '_gat', 'fbp', 'fbc', '_hj', 'mp_', 'twclid',
            'utm_', 'ads_', 'track', 'analytics', 'pixel', 'beacon',
            'session', 'visitor', 'user', 'event', 'conversion'
        ]
        
        tracking_cookies = 0
        for cookie in domain_cookies:
            if any(pattern in cookie.name.lower() for pattern in tracking_cookie_patterns):
                tracking_cookies += 1
        
        if len(domain_cookies) > 0:
            cookie_tracking_ratio = tracking_cookies / len(domain_cookies)
            likelihood += cookie_tracking_ratio * 0.8
        
        # Check for scripts from this domain
        has_scripts = any(domain_lower in script.lower() for script in js_scripts)
        if has_scripts:
            likelihood += 0.6
        
        # Check domain patterns
        suspicious_patterns = [
            'track', 'analytics', 'pixel', 'beacon', 'ads', 'advertising',
            'marketing', 'metrics', 'stats', 'data', 'collect', 'monitor'
        ]
        
        if any(pattern in domain_lower for pattern in suspicious_patterns):
            likelihood += 0.4
        
        # Check for common tracking TLDs
        tracking_tlds = ['.io', '.co', '.app', '.tech', '.digital', '.online']
        if any(domain_lower.endswith(tld) for tld in tracking_tlds):
            likelihood += 0.2
        
        # Cap at 1.0
        return min(likelihood, 1.0)
    
    def _calculate_risk_level(self, domain: str, cookies: List[CookieData], tracking_likelihood: float) -> str:
        """Calculate the risk level of a tracking domain."""
        domain_lower = domain.lower()
        domain_cookies = [c for c in cookies if c.domain.lower() == domain_lower]
        
        # High risk factors
        high_risk_factors = 0
        
        if tracking_likelihood > 0.8:
            high_risk_factors += 1
        if len(domain_cookies) > 3:
            high_risk_factors += 1
        if any(tracker in domain_lower for tracker in self.config.analyzer.tracking_domains):
            high_risk_factors += 1
        if any('ads' in c.name.lower() or 'track' in c.name.lower() for c in domain_cookies):
            high_risk_factors += 1
        
        if high_risk_factors >= 3:
            return 'high'
        elif high_risk_factors >= 2:
            return 'medium'
        elif tracking_likelihood > 0.3:
            return 'low'
        else:
            return 'minimal'
    
    def get_privacy_impact_assessment(self, page_data: PageData) -> Dict[str, Any]:
        """Generate comprehensive privacy impact assessment with actionable recommendations."""
        tracking_data = self.get_tracking_domains_with_access(page_data)
        cookies = page_data.cookies
        
        assessment = {
            'overall_privacy_score': 0,
            'risk_level': 'low',
            'privacy_concerns': [],
            'actionable_recommendations': [],
            'data_protection_measures': [],
            'tracking_intensity': 'minimal',
            'consent_effectiveness': 'unknown'
        }
        
        # Calculate privacy score based on tracking data
        total_domains = tracking_data['access_summary']['total_tracking_domains']
        known_trackers = tracking_data['access_summary'].get('known_trackers', 0)
        high_risk_domains = tracking_data['access_summary'].get('high_risk_domains', 0)
        
        # Base score starts at 100 (best privacy)
        privacy_score = 100
        
        # Deduct points for tracking domains
        privacy_score -= min(total_domains * 2, 40)  # Max 40 points for domain count
        privacy_score -= min(known_trackers * 5, 30)  # Max 30 points for known trackers
        privacy_score -= min(high_risk_domains * 10, 30)  # Max 30 points for high-risk
        
        # Deduct for cookie issues
        third_party_cookies = len([c for c in cookies if c.is_third_party])
        privacy_score -= min(third_party_cookies * 0.5, 20)  # Max 20 points for third-party cookies
        
        # Deduct for session cookies (continuous tracking)
        session_cookies = len([c for c in cookies if not c.expires])
        privacy_score -= min(session_cookies * 0.3, 15)  # Max 15 points for session cookies
        
        assessment['overall_privacy_score'] = max(0, int(privacy_score))
        
        # Determine risk level
        if privacy_score >= 80:
            assessment['risk_level'] = 'minimal'
            assessment['tracking_intensity'] = 'minimal'
        elif privacy_score >= 60:
            assessment['risk_level'] = 'low'
            assessment['tracking_intensity'] = 'low'
        elif privacy_score >= 40:
            assessment['risk_level'] = 'medium'
            assessment['tracking_intensity'] = 'moderate'
        elif privacy_score >= 20:
            assessment['risk_level'] = 'high'
            assessment['tracking_intensity'] = 'high'
        else:
            assessment['risk_level'] = 'critical'
            assessment['tracking_intensity'] = 'extreme'
        
        # Generate privacy concerns
        if total_domains > 10:
            assessment['privacy_concerns'].append({
                'concern': 'Extensive third-party tracking network',
                'impact': 'high',
                'description': f'{total_domains} companies will have access to your browsing data'
            })
        
        if known_trackers > 5:
            assessment['privacy_concerns'].append({
                'concern': 'Major advertising networks present',
                'impact': 'high',
                'description': f'{known_trackers} known tracking companies detected'
            })
        
        if high_risk_domains > 0:
            assessment['privacy_concerns'].append({
                'concern': 'High-risk tracking domains',
                'impact': 'critical',
                'description': f'{high_risk_domains} domains pose significant privacy risks'
            })
        
        if third_party_cookies > 20:
            assessment['privacy_concerns'].append({
                'concern': 'Excessive third-party cookies',
                'impact': 'medium',
                'description': f'{third_party_cookies} third-party cookies will track your activity'
            })
        
        # Generate actionable recommendations
        if assessment['risk_level'] in ['high', 'critical']:
            assessment['actionable_recommendations'].extend([
                {
                    'action': 'Use privacy-focused browser extensions',
                    'priority': 'high',
                    'tools': ['uBlock Origin', 'Privacy Badger', 'HTTPS Everywhere']
                },
                {
                    'action': 'Consider browser anti-fingerprinting measures',
                    'priority': 'high',
                    'tools': ['Tor Browser', 'Brave Browser with shields']
                },
                {
                    'action': 'Review and limit cookie consent',
                    'priority': 'medium',
                    'description': 'Only accept essential cookies, reject advertising and analytics'
                }
            ])
        elif assessment['risk_level'] == 'medium':
            assessment['actionable_recommendations'].extend([
                {
                    'action': 'Install ad and tracker blockers',
                    'priority': 'medium',
                    'tools': ['uBlock Origin', 'AdBlock Plus']
                },
                {
                    'action': 'Use browser privacy features',
                    'priority': 'medium',
                    'description': 'Enable "Do Not Track" and block third-party cookies'
                }
            ])
        else:
            assessment['actionable_recommendations'].append({
                'action': 'Maintain current privacy practices',
                'priority': 'low',
                'description': 'Your privacy exposure on this site appears minimal'
            })
        
        # Data protection measures
        assessment['data_protection_measures'] = [
            {
                'measure': 'Regular cookie cleanup',
                'description': 'Clear cookies and site data regularly',
                'frequency': 'weekly'
            },
            {
                'measure': 'Use incognito/private browsing',
                'description': 'Prevents persistent tracking across sessions',
                'frequency': 'when privacy is critical'
            },
            {
                'measure': 'VPN usage',
                'description': 'Mask your IP address from trackers',
                'frequency': 'recommended for high-risk sites'
            }
        ]
        
        # Assess consent effectiveness
        consent_banner = any('consent' in str(f).lower() for f in getattr(page_data, 'dark_patterns', []))
        if consent_banner:
            if total_domains > 15:
                assessment['consent_effectiveness'] = 'poor'
            elif total_domains > 5:
                assessment['consent_effectiveness'] = 'moderate'
            else:
                assessment['consent_effectiveness'] = 'good'
        else:
            assessment['consent_effectiveness'] = 'no_consent_required'
        
        return assessment
