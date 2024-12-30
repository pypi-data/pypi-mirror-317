"""Utility functions for web surfer operations."""
from typing import Dict, Any, Optional, List, cast
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup, Tag
from ._types import ElementInfo, PageInfo

def normalize_url(base_url: str, url: str) -> str:
    """Normalize a URL against a base URL."""
    if not url:
        return base_url
    if not bool(urlparse(url).netloc):
        return urljoin(base_url, url)
    return url

def extract_element_info(element: Any) -> ElementInfo:
    """Extract information about an element."""
    return {
        "tag": element.name or "",
        "text": element.get_text(strip=True),
        "attributes": dict(element.attrs),
        "xpath": _get_element_xpath(element),
        "is_visible": _is_element_visible(element)
    }

def _get_element_xpath(element: Any) -> str:
    """Get XPath for an element."""
    components = []
    child = element
    for parent in element.parents:
        siblings = parent.find_all(child.name, recursive=False)
        if len(siblings) == 1:
            components.append(child.name)
        else:
            index = siblings.index(child) + 1
            components.append(f"{child.name}[{index}]")
        child = parent
    components.reverse()
    return '/' + '/'.join(components)

def _is_element_visible(element: Any) -> bool:
    """Check if an element is likely visible."""
    style = element.get('style', '').lower()
    classes = ' '.join(element.get('class', [])).lower()
    
    # Check style attributes
    if 'display: none' in style or 'visibility: hidden' in style:
        return False
        
    # Check common hidden classes
    hidden_classes = {'hidden', 'invisible', 'collapsed', 'display-none'}
    if any(cls in classes for cls in hidden_classes):
        return False
        
    return True

def extract_page_info(url: str, html: str, headers: Dict[str, str], cookies: List[Dict[str, Any]]) -> PageInfo:
    """Extract information about a web page."""
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract links
    links = []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href:
            links.append({
                "text": link.get_text(strip=True),
                "url": normalize_url(url, href)
            })
            
    # Extract elements
    elements = []
    for element in soup.find_all(True):  # Find all elements
        elements.append(extract_element_info(element))
        
    # Get title with fallback
    title = ""
    if soup.title and soup.title.string:
        title_text = soup.title.string
        if isinstance(title_text, str):
            title = title_text.strip()
    else:
        h1 = soup.find('h1')
        if h1 and isinstance(h1, Tag):
            title = h1.get_text(strip=True)
        else:
            meta_title = soup.find('meta', property='og:title')
            if meta_title and isinstance(meta_title, Tag):
                content = meta_title.get('content')
                if isinstance(content, str):
                    title = content.strip()
        
    return {
        "url": url,
        "title": title,
        "text": soup.get_text(strip=True),
        "links": links,
        "elements": elements,
        "cookies": cookies,
        "headers": headers
    }

def extract_text_content(html: str, selector: Optional[str] = None) -> str:
    """Extract text content from HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    if selector:
        elements = soup.select(selector)
        return ' '.join(element.get_text(strip=True) for element in elements)
    return soup.get_text(strip=True)

def find_elements_by_text(html: str, text: str, case_sensitive: bool = False) -> List[ElementInfo]:
    """Find elements containing specific text."""
    soup = BeautifulSoup(html, 'html.parser')
    elements = []
    
    text_pattern = re.compile(re.escape(text), re.IGNORECASE if not case_sensitive else 0)
    
    for element in soup.find_all(text=text_pattern):
        if element.parent:
            elements.append(extract_element_info(element.parent))
            
    return elements

def find_elements_by_selector(html: str, selector: str) -> List[ElementInfo]:
    """Find elements matching a CSS selector."""
    soup = BeautifulSoup(html, 'html.parser')
    return [extract_element_info(element) for element in soup.select(selector)] 