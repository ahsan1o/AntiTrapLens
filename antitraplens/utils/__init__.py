"""
Utilities module for AntiTrapLens.
"""

import re
import hashlib
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, urljoin
from datetime import datetime

class URLUtils:
    """Utility functions for URL handling."""

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if URL is valid."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    @staticmethod
    def get_domain(url: str) -> str:
        """Extract domain from URL."""
        try:
            return urlparse(url).netloc
        except:
            return ""

    @staticmethod
    def is_same_domain(url1: str, url2: str) -> bool:
        """Check if two URLs belong to the same domain."""
        return URLUtils.get_domain(url1) == URLUtils.get_domain(url2)

    @staticmethod
    def normalize_url(url: str) -> str:
        """Normalize URL by removing fragments and trailing slashes."""
        parsed = urlparse(url)
        normalized = parsed._replace(fragment='', path=parsed.path.rstrip('/'))
        return normalized.geturl()

class TextUtils:
    """Utility functions for text processing."""

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text."""
        if not text:
            return ""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        return text

    @staticmethod
    def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
        """Extract keywords from text."""
        if not text:
            return []

        # Simple keyword extraction (can be enhanced with NLP)
        words = re.findall(r'\b\w+\b', text.lower())
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall'}
        keywords = [word for word in words if word not in stop_words and len(word) > 2]

        # Count frequency and return top keywords
        from collections import Counter
        keyword_counts = Counter(keywords)
        return [word for word, _ in keyword_counts.most_common(max_keywords)]

class DataUtils:
    """Utility functions for data processing."""

    @staticmethod
    def hash_string(text: str) -> str:
        """Generate SHA256 hash of string."""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    @staticmethod
    def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
        """Safely get value from dictionary."""
        try:
            return data.get(key, default)
        except:
            return default

    @staticmethod
    def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
        """Merge multiple dictionaries."""
        result = {}
        for d in dicts:
            if d:
                result.update(d)
        return result

class TimeUtils:
    """Utility functions for time handling."""

    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()

    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration in human readable format."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = seconds % 60
            return f"{minutes}m {secs:.1f}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"

class ValidationUtils:
    """Utility functions for data validation."""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_cookie_name(name: str) -> bool:
        """Validate cookie name format."""
        # Cookie names should not contain control characters, spaces, or tabs
        return bool(name and not re.search(r'[\x00-\x1F\x7F\s]', name))

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename by removing invalid characters."""
        return re.sub(r'[<>:"/\\|?*]', '_', filename)
