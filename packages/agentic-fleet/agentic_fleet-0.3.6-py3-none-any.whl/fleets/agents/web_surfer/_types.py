"""Type definitions for web surfer operations."""
from typing import TypedDict, List, Optional, Dict, Any

class ElementInfo(TypedDict):
    """Information about a web element."""
    tag: str
    text: str
    attributes: Dict[str, str]
    xpath: str
    is_visible: bool

class PageInfo(TypedDict, total=False):
    """Information about a web page."""
    url: str
    title: str
    text: str
    links: List[Dict[str, str]]
    elements: List[ElementInfo]
    cookies: List[Dict[str, Any]]
    headers: Dict[str, str]

class NavigationResult(TypedDict):
    """Result of a navigation action."""
    success: bool
    url: str
    status: int
    error: Optional[str]

class ClickResult(TypedDict):
    """Result of a click action."""
    success: bool
    element: Optional[ElementInfo]
    error: Optional[str]

class InputResult(TypedDict):
    """Result of an input action."""
    success: bool
    element: Optional[ElementInfo]
    value: str
    error: Optional[str]

class ScrapingResult(TypedDict):
    """Result of a scraping action."""
    success: bool
    data: List[Any]
    error: Optional[str]

class BrowserConfig(TypedDict, total=False):
    """Browser configuration."""
    headless: bool
    user_agent: str
    viewport_size: Dict[str, int]
    locale: str
    timezone: str
    geolocation: Dict[str, float]
    proxy: Optional[Dict[str, str]]
    cookies: List[Dict[str, Any]]
    headers: Dict[str, str] 