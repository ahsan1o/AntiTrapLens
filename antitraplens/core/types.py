"""
Type definitions for AntiTrapLens.
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass

@dataclass
class CookieData:
    """Cookie data structure."""
    name: str
    value: str
    domain: str
    path: str
    expires: Optional[float]
    httpOnly: bool
    secure: bool
    sameSite: Optional[str]
    is_third_party: bool

@dataclass
class ImageData:
    """Image data structure."""
    src: str
    alt: str
    width: Optional[str]
    height: Optional[str]

@dataclass
class FormData:
    """Form data structure."""
    action: Optional[str]
    method: str
    inputs: List[Dict[str, Any]]

@dataclass
class PopupData:
    """Popup/modal data structure."""
    selector: str
    text: str
    visible: bool

@dataclass
class LinkData:
    """Link data structure."""
    url: str
    text: Optional[str] = None
    is_internal: bool = False

@dataclass
class MetaTagData:
    """Meta tag data structure."""
    name: Optional[str]
    property: Optional[str]
    content: Optional[str]

@dataclass
class PageData:
    """Complete page data structure."""
    url: str
    title: str
    html: str
    html_length: int
    meta_tags: List[MetaTagData]
    css_links: List[str]
    js_scripts: List[str]
    popups: List[PopupData]
    forms: List[FormData]
    links: List[str]
    images: List[ImageData]
    cookies: List[CookieData]
    timestamp: str
    category: Optional[str] = None
    cookie_access_analysis: Optional[Dict[str, Any]] = None

@dataclass
class Finding:
    """Dark pattern finding structure."""
    pattern: str
    severity: str  # 'high', 'medium', 'low'
    description: str
    evidence: Optional[str] = None
    element: Optional[Any] = None
    nlp_analysis: Optional[str] = None

@dataclass
class DetectionResult:
    """Detection result structure."""
    findings: List[Finding]
    score: Dict[str, Any]

@dataclass
class ScanResult:
    """Complete scan result structure."""
    scan_info: Dict[str, Any]
    pages: List[PageData]

# Type aliases
CookieList = List[CookieData]
ImageList = List[ImageData]
FindingList = List[Finding]
PageList = List[PageData]
