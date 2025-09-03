"""
Image analysis module for AntiTrapLens.
"""

from typing import Dict, List, Any, Optional
from ..core.types import PageData, ImageData
from ..core.config import config

class ImageAnalyzer:
    """Analyzes images for content classification."""

    def __init__(self, config=None):
        self.config = config or config.analyzer

    def analyze(self, page_data: PageData) -> Dict[str, Any]:
        """Analyze images for content classification."""
        images = page_data.images
        html = page_data.html.lower()

        analysis = {
            'image_stats': {
                'total': len(images),
                'with_alt': len([img for img in images if img.alt]),
                'without_alt': len([img for img in images if not img.alt]),
                'external': len([img for img in images if not img.src.startswith(page_data.url[:page_data.url.find('/', 8)])])
            },
            'content_indicators': [],
            'accessibility_issues': []
        }

        # Analyze alt text for content indicators
        for img in images:
            alt = img.alt.lower()
            src = img.src.lower()

            # E-commerce indicators
            if any(term in alt or term in src for term in ['product', 'item', 'buy', 'price', 'cart', 'shop']):
                analysis['content_indicators'].append('ecommerce')

            # Adult content indicators
            if any(term in alt or term in src for term in ['nude', 'sex', 'adult', 'erotic', 'porn']):
                analysis['content_indicators'].append('adult')

            # Social media indicators
            if any(term in alt or term in src for term in ['profile', 'avatar', 'post', 'like', 'share']):
                analysis['content_indicators'].append('social')

            # Streaming indicators
            if any(term in alt or term in src for term in ['movie', 'series', 'episode', 'watch', 'stream']):
                analysis['content_indicators'].append('streaming')

        # Accessibility analysis
        if analysis['image_stats']['without_alt'] > 0:
            missing_percentage = (analysis['image_stats']['without_alt'] / analysis['image_stats']['total']) * 100
            if missing_percentage > 50:
                analysis['accessibility_issues'].append('Many images missing alt text - poor accessibility')
            elif missing_percentage > 20:
                analysis['accessibility_issues'].append('Some images missing alt text')

        # Content type analysis
        content_types = list(set(analysis['content_indicators']))
        analysis['primary_content_type'] = self._determine_primary_type(content_types, images)

        return analysis

    def _determine_primary_type(self, indicators: List[str], images: List[ImageData]) -> str:
        """Determine the primary content type based on indicators."""
        if not indicators:
            return 'general'

        # Count occurrences
        counts = {}
        for indicator in indicators:
            counts[indicator] = indicators.count(indicator)

        # Special handling for adult content
        if 'adult' in counts and counts['adult'] > 0:
            adult_images = len([img for img in images if any(term in (img.alt + img.src).lower()
                            for term in ['nude', 'sex', 'adult', 'erotic', 'porn'])])
            if adult_images > len(images) * 0.3:  # 30% adult images
                return 'adult'

        # Return most common indicator
        return max(counts, key=counts.get)

    def get_image_recommendations(self, page_data: PageData) -> List[str]:
        """Get recommendations for image optimization."""
        recommendations = []
        images = page_data.images

        if not images:
            return recommendations

        # Alt text recommendations
        missing_alt = len([img for img in images if not img.alt])
        if missing_alt > 0:
            recommendations.append(f"Add alt text to {missing_alt} images for better accessibility")

        # Image size recommendations
        large_images = len([img for img in images if img.width and int(img.width) > 1000])
        if large_images > 5:
            recommendations.append("Consider optimizing large images for better performance")

        # External image recommendations
        external_images = len([img for img in images if 'http' in img.src and page_data.url not in img.src])
        if external_images > len(images) * 0.5:
            recommendations.append("Many images are external - consider hosting locally for better performance")

        return recommendations
