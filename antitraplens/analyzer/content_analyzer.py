"""
Content analysis module for AntiTrapLens.
"""

from typing import Dict, List, Any, Optional
from ..core.types import PageData
from ..core.config import config
from .cookie_analyzer import CookieAnalyzer
from .image_analyzer import ImageAnalyzer

class ContentAnalyzer:
    """Main content analyzer that combines all analysis types."""

    def __init__(self, config=None):
        self.config = config or config.analyzer
        self.cookie_analyzer = CookieAnalyzer(self.config)
        self.image_analyzer = ImageAnalyzer(self.config)

    def analyze(self, page_data: PageData) -> Dict[str, Any]:
        """Perform complete content analysis."""
        analysis = {
            'category': self._categorize_website(page_data),
            'cookie_analysis': self.cookie_analyzer.analyze(page_data),
            'image_analysis': self.image_analyzer.analyze(page_data),
            'content_quality': self._analyze_content_quality(page_data),
            'privacy_score': self._calculate_privacy_score(page_data)
        }

        return analysis

    def _categorize_website(self, page_data: PageData) -> str:
        """Categorize website based on content analysis."""
        title = page_data.title.lower()
        html = page_data.html.lower()

        # Category keywords
        categories = {
            'ecommerce': ['shop', 'buy', 'cart', 'product', 'store', 'price', 'sale'],
            'adult_streaming': ['adult', 'porn', 'sex', 'xxx', 'jav', '18+', 'nude', 'erotic', 'movie', 'series', 'watch', 'stream'],
            'streaming': ['watch', 'movie', 'series', 'stream', 'video', 'tv', 'film'],
            'news': ['news', 'article', 'blog', 'politics', 'sports', 'headline'],
            'social': ['social', 'community', 'forum', 'chat', 'profile', 'post', 'like', 'share'],
            'educational': ['learn', 'course', 'tutorial', 'education', 'lesson'],
            'gaming': ['game', 'play', 'gaming', 'esports', 'console']
        }

        scores = {}
        for cat, keywords in categories.items():
            score = 0
            for kw in keywords:
                if kw in title or kw in html:
                    score += 1
            scores[cat] = score

        # Image-based scoring
        image_analysis = self.image_analyzer.analyze(page_data)
        primary_type = image_analysis.get('primary_content_type', 'general')
        if primary_type in scores:
            scores[primary_type] += 2

        # Return best category
        best_cat = max(scores, key=scores.get)
        return best_cat.replace('_', ' ').title() if scores[best_cat] > 0 else 'General'

    def _analyze_content_quality(self, page_data: PageData) -> Dict[str, Any]:
        """Analyze content quality metrics."""
        quality = {
            'score': 100,
            'issues': [],
            'strengths': []
        }

        # Check for HTTPS
        if not page_data.url.startswith('https'):
            quality['score'] -= 20
            quality['issues'].append('Not using HTTPS')

        # Check for meta description
        has_meta_desc = any(meta.content for meta in page_data.meta_tags
                          if meta.name == 'description' or meta.property == 'og:description')
        if has_meta_desc:
            quality['strengths'].append('Has meta description')
        else:
            quality['score'] -= 10
            quality['issues'].append('Missing meta description')

        # Check for title
        if page_data.title and len(page_data.title) > 10:
            quality['strengths'].append('Has descriptive title')
        else:
            quality['score'] -= 15
            quality['issues'].append('Poor or missing title')

        # Check for images with alt text
        image_analysis = self.image_analyzer.analyze(page_data)
        alt_ratio = image_analysis['image_stats']['with_alt'] / max(image_analysis['image_stats']['total'], 1)
        if alt_ratio > 0.8:
            quality['strengths'].append('Good alt text coverage')
        elif alt_ratio < 0.5:
            quality['score'] -= 10
            quality['issues'].append('Poor alt text coverage')

        return quality

    def _calculate_privacy_score(self, page_data: PageData) -> Dict[str, Any]:
        """Calculate privacy score based on cookies and tracking."""
        score = 100
        concerns = []

        cookie_analysis = self.cookie_analyzer.analyze(page_data)

        # Deduct points for privacy concerns
        if len(cookie_analysis['third_party_access']) > 5:
            score -= 30
            concerns.append('Extensive third-party tracking')
        elif len(cookie_analysis['third_party_access']) > 2:
            score -= 15
            concerns.append('Multiple third-party domains')

        if len(cookie_analysis['tracking_capabilities']) > 3:
            score -= 25
            concerns.append('Multiple tracking systems')
        elif len(cookie_analysis['tracking_capabilities']) > 0:
            score -= 10
            concerns.append('Tracking systems detected')

        if len(cookie_analysis['privacy_concerns']) > 2:
            score -= 20
            concerns.append('Multiple privacy concerns')
        elif len(cookie_analysis['privacy_concerns']) > 0:
            score -= 10
            concerns.append('Privacy concerns detected')

        return {
            'score': max(0, score),
            'grade': 'A' if score >= 80 else 'B' if score >= 60 else 'C' if score >= 40 else 'D' if score >= 20 else 'F',
            'concerns': concerns
        }
