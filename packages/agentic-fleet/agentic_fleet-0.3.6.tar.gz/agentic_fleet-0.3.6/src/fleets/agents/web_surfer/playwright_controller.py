"""Playwright controller for browser automation."""
from typing import Dict, Any, Optional, List, Union, cast, TypedDict, Sequence
import logging
import json
from pathlib import Path
from playwright.async_api import (
    async_playwright, Browser, Page, Response,
    ViewportSize, Geolocation, ProxySettings, Cookie
)
from playwright._impl._api_structures import SetCookieParam

from ._types import (
    BrowserConfig, ElementInfo, PageInfo, NavigationResult,
    ClickResult, InputResult, ScrapingResult
)
from ._utils import extract_page_info

logger = logging.getLogger(__name__)

class PlaywrightController:
    """Controller for browser automation using Playwright."""
    
    def __init__(self, config: Optional[BrowserConfig] = None):
        """Initialize controller with configuration."""
        self.config = config or {}
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._page: Optional[Page] = None
        self._script_loaded = False
        
    async def _ensure_browser(self):
        """Ensure browser is launched."""
        if not self._playwright:
            self._playwright = await async_playwright().start()
            
        if not self._browser:
            self._browser = await self._playwright.chromium.launch(
                headless=self.config.get('headless', True)
            )
            
        if not self._page:
            viewport = cast(Optional[ViewportSize], self.config.get('viewport_size'))
            geolocation = cast(Optional[Geolocation], self.config.get('geolocation'))
            proxy = cast(Optional[ProxySettings], self.config.get('proxy'))
            
            self._page = await self._browser.new_page(
                viewport=viewport,
                locale=self.config.get('locale'),
                timezone_id=self.config.get('timezone'),
                geolocation=geolocation,
                proxy=proxy,
                user_agent=self.config.get('user_agent')
            )
            
            # Set cookies and headers if provided
            cookies = self.config.get('cookies', [])
            if cookies:
                await self._page.context.add_cookies(cast(Sequence[SetCookieParam], cookies))
                
            headers = self.config.get('headers', {})
            if headers:
                await self._page.set_extra_http_headers(headers)
                
    async def _load_page_script(self):
        """Load page script for enhanced functionality."""
        if not self._script_loaded and self._page:
            script_path = Path(__file__).parent / 'page_script.js'
            with open(script_path, 'r', encoding='utf-8') as f:
                await self._page.add_init_script(f.read())
            self._script_loaded = True
            
    async def cleanup(self):
        """Clean up resources."""
        if self._page:
            await self._page.close()
            self._page = None
            
        if self._browser:
            await self._browser.close()
            self._browser = None
            
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
            
    async def navigate(self, url: str) -> NavigationResult:
        """Navigate to a URL."""
        try:
            await self._ensure_browser()
            await self._load_page_script()
            
            if not self._page:
                return {
                    "success": False,
                    "url": url,
                    "status": 0,
                    "error": "Browser not initialized"
                }
                
            response = await self._page.goto(url, wait_until='networkidle')
            if not response:
                return {
                    "success": False,
                    "url": url,
                    "status": 0,
                    "error": "No response received"
                }
                
            return {
                "success": response.ok,
                "url": response.url,
                "status": response.status,
                "error": None if response.ok else f"HTTP {response.status}"
            }
            
        except Exception as e:
            logger.error(f"Navigation error: {e}")
            return {
                "success": False,
                "url": url,
                "status": 0,
                "error": str(e)
            }
            
    async def get_page_info(self) -> Optional[PageInfo]:
        """Get information about the current page."""
        try:
            if not self._page:
                return None
                
            html = await self._page.content()
            headers = await self._page.evaluate('() => Object.fromEntries(Array.from(document.getElementsByTagName("meta")).map(m => [m.name, m.content]))')
            cookies = await self._page.context.cookies()
            
            return extract_page_info(
                url=self._page.url,
                html=html,
                headers=headers,
                cookies=[dict(cookie) for cookie in cookies]
            )
            
        except Exception as e:
            logger.error(f"Error getting page info: {e}")
            return None
            
    async def click(self, selector: str) -> ClickResult:
        """Click an element on the page."""
        try:
            if not self._page:
                return {
                    "success": False,
                    "element": None,
                    "error": "Browser not initialized"
                }
                
            element = await self._page.query_selector(selector)
            if not element:
                return {
                    "success": False,
                    "element": None,
                    "error": f"Element not found: {selector}"
                }
                
            info = await element.evaluate('(el) => window.pageTools.getElementInfo(el)')
            await element.click()
            
            return {
                "success": True,
                "element": info,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Click error: {e}")
            return {
                "success": False,
                "element": None,
                "error": str(e)
            }
            
    async def type_text(self, selector: str, text: str) -> InputResult:
        """Type text into an input element."""
        try:
            if not self._page:
                return {
                    "success": False,
                    "element": None,
                    "value": text,
                    "error": "Browser not initialized"
                }
                
            element = await self._page.query_selector(selector)
            if not element:
                return {
                    "success": False,
                    "element": None,
                    "value": text,
                    "error": f"Element not found: {selector}"
                }
                
            info = await element.evaluate('(el) => window.pageTools.getElementInfo(el)')
            await element.fill(text)
            
            return {
                "success": True,
                "element": info,
                "value": text,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Type error: {e}")
            return {
                "success": False,
                "element": None,
                "value": text,
                "error": str(e)
            }
            
    async def find_elements(
        self,
        by: str = 'selector',
        value: str = '',
        case_sensitive: bool = False
    ) -> ScrapingResult:
        """Find elements on the page."""
        try:
            if not self._page:
                return {
                    "success": False,
                    "data": [],
                    "error": "Browser not initialized"
                }
                
            if by == 'text':
                elements = await self._page.evaluate(
                    'args => window.pageTools.findElementsByText(args[0], args[1])',
                    [value, case_sensitive]
                )
            elif by == 'selector':
                elements = await self._page.evaluate(
                    'selector => window.pageTools.findElementsBySelector(selector)',
                    value
                )
            else:
                return {
                    "success": False,
                    "data": [],
                    "error": f"Invalid search method: {by}"
                }
                
            return {
                "success": True,
                "data": elements,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Find elements error: {e}")
            return {
                "success": False,
                "data": [],
                "error": str(e)
            }
            
    async def extract_data(self, data_type: str = 'links') -> ScrapingResult:
        """Extract specific data from the page."""
        try:
            if not self._page:
                return {
                    "success": False,
                    "data": [],
                    "error": "Browser not initialized"
                }
                
            if data_type == 'links':
                data = await self._page.evaluate('() => window.pageTools.extractLinks()')
            elif data_type == 'images':
                data = await self._page.evaluate('() => window.pageTools.extractImages()')
            elif data_type == 'forms':
                data = await self._page.evaluate('() => window.pageTools.extractForms()')
            else:
                return {
                    "success": False,
                    "data": [],
                    "error": f"Invalid data type: {data_type}"
                }
                
            return {
                "success": True,
                "data": data,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Extract data error: {e}")
            return {
                "success": False,
                "data": [],
                "error": str(e)
            } 