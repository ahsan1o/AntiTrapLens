"""
Website categorization analyzer for AntiTrapLens.
"""

from typing import Dict, Any, Optional
from ..core.types import PageData

class WebsiteCategorizer:
    """Categorizes websites based on content, URL, and metadata analysis."""

    def __init__(self):
        # Category keywords and patterns
        self.category_patterns = {
            'e-commerce': {
                'url_keywords': ['shop', 'store', 'buy', 'cart', 'checkout', 'product', 'amazon', 'ebay', 'walmart', 'target', 'bestbuy', 'shopping', 'commerce'],
                'content_keywords': ['price', 'buy now', 'add to cart', 'checkout', 'shipping', 'product', 'inventory', 'sale', 'purchase', 'order'],
                'meta_keywords': ['ecommerce', 'shopping', 'retail', 'commerce', 'store']
            },
            'news': {
                'url_keywords': ['news', 'cnn', 'bbc', 'nytimes', 'washingtonpost', 'foxnews', 'reuters', 'apnews'],
                'content_keywords': ['breaking news', 'headline', 'article', 'journalism', 'reporter', 'editorial'],
                'meta_keywords': ['news', 'journalism', 'media', 'press']
            },
            'social-media': {
                'url_keywords': ['facebook', 'twitter', 'instagram', 'linkedin', 'tiktok', 'snapchat', 'reddit', 'youtube'],
                'content_keywords': ['follow', 'like', 'share', 'post', 'timeline', 'feed', 'social'],
                'meta_keywords': ['social', 'networking', 'community']
            },
            'streaming': {
                'url_keywords': ['netflix', 'hulu', 'disney', 'amazonprime', 'hbomax', 'youtube', 'twitch', 'vimeo'],
                'content_keywords': ['stream', 'video', 'watch', 'episode', 'season', 'series', 'movie', 'entertainment'],
                'meta_keywords': ['streaming', 'video', 'entertainment', 'media']
            },
            'adult': {
                'url_keywords': ['porn', 'adult', 'xxx', 'sex', 'nsfw', 'onlyfans', 'brazzers'],
                'content_keywords': ['adult content', 'mature', 'nsfw', 'erotic', 'sexual'],
                'meta_keywords': ['adult', 'mature', 'nsfw']
            },
            'search-engine': {
                'url_keywords': ['google', 'bing', 'yahoo', 'duckduckgo', 'search'],
                'content_keywords': ['search', 'query', 'results', 'web search', 'find'],
                'meta_keywords': ['search', 'engine', 'web search']
            },
            'educational': {
                'url_keywords': ['edu', 'university', 'college', 'school', 'course', 'learn', 'education'],
                'content_keywords': ['course', 'lesson', 'education', 'learning', 'academic', 'student'],
                'meta_keywords': ['education', 'learning', 'academic']
            },
            'government': {
                'url_keywords': ['gov', 'government', 'state', 'federal', 'ministry', 'department'],
                'content_keywords': ['government', 'public service', 'official', 'policy', 'regulation'],
                'meta_keywords': ['government', 'public', 'official']
            },
            'financial': {
                'url_keywords': ['bank', 'finance', 'investment', 'trading', 'wallet', 'crypto', 'bitcoin'],
                'content_keywords': ['banking', 'finance', 'investment', 'trading', 'account', 'transaction'],
                'meta_keywords': ['finance', 'banking', 'investment']
            },
            'healthcare': {
                'url_keywords': ['hospital', 'clinic', 'medical', 'health', 'pharmacy', 'doctor'],
                'content_keywords': ['health', 'medical', 'treatment', 'patient', 'care', 'wellness'],
                'meta_keywords': ['health', 'medical', 'healthcare']
            }
        }

    def categorize(self, page_data: PageData) -> str:
        """Categorize a website based on its content and metadata."""
        
        url = page_data.url.lower()
        title = getattr(page_data, 'title', '').lower()
        html = page_data.html.lower()
        
        # Extract meta description and keywords
        meta_description = ''
        meta_keywords = []
        
        for meta in page_data.meta_tags:
            if meta.name == 'description' or meta.property == 'og:description':
                meta_description = meta.content.lower() if meta.content else ''
            elif meta.name == 'keywords':
                if meta.content:
                    meta_keywords.extend([kw.strip().lower() for kw in meta.content.split(',')])
        
        # Calculate scores for each category
        category_scores = {}
        
        for category, patterns in self.category_patterns.items():
            score = 0
            
            # URL pattern matching
            for keyword in patterns['url_keywords']:
                if keyword in url:
                    score += 3  # Higher weight for URL matches
            
            # Special priority for major e-commerce sites
            if 'amazon' in url or 'ebay' in url or 'walmart' in url:
                if category == 'e-commerce':
                    score += 10  # Much higher priority for major e-commerce sites
            
            # Title matching
            for keyword in patterns['content_keywords']:
                if keyword in title:
                    score += 2
            
            # Content matching
            for keyword in patterns['content_keywords']:
                if keyword in html:
                    score += 1
            
            # Meta keywords matching
            for keyword in patterns['meta_keywords']:
                if keyword in meta_keywords or keyword in meta_description:
                    score += 2
            
            # Special URL patterns
            if '.edu' in url or 'university' in url:
                if category == 'educational':
                    score += 5
            elif '.gov' in url or 'government' in url:
                if category == 'government':
                    score += 5
            
            category_scores[category] = score
        
        # Find the category with the highest score
        best_category = max(category_scores.items(), key=lambda x: x[1])
        
        # Only return the category if it has a reasonable score
        if best_category[1] >= 2:
            return best_category[0].replace('-', ' ').title()
        else:
            return 'General'

    def get_category_details(self, page_data: PageData) -> Dict[str, Any]:
        """Get detailed categorization information."""
        category = self.categorize(page_data)
        
        return {
            'category': category,
            'confidence': 'high' if category != 'General' else 'low',
            'analysis': {
                'url': page_data.url,
                'title': getattr(page_data, 'title', ''),
                'meta_tags_count': len(page_data.meta_tags),
                'content_length': len(page_data.html)
            }
        }