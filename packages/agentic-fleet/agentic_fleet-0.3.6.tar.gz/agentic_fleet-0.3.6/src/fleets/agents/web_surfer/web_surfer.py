"""Web surfer agent implementation."""
from typing import Any, Dict, List, Optional, Union, Callable
import logging
from pathlib import Path

from ...core.agent import Agent
from ...core.config import AgentConfig
from ._types import BrowserConfig
from ._tool_definitions import DEFAULT_TOOLS
from .playwright_controller import PlaywrightController

logger = logging.getLogger(__name__)

class WebSurferAgent(Agent):
    """Agent specialized in web browsing and content extraction."""
    
    def __init__(
        self,
        config: AgentConfig,
        system_message: Optional[str] = None,
        tools: Optional[Dict[str, Callable]] = None,
        functions: Optional[List[Dict[str, Any]]] = None,
        browser_config: Optional[BrowserConfig] = None
    ):
        if system_message is None:
            system_message = """You are a web surfing expert that can:
1. Browse web pages and extract content
2. Follow links and navigate websites
3. Parse and analyze web content
4. Extract structured data from HTML
5. Handle web requests safely and efficiently"""
            
        # Add default web surfer tools
        if functions is None:
            functions = []
        functions.extend(DEFAULT_TOOLS)
            
        super().__init__(config, system_message, tools, functions)
        self._controller = PlaywrightController(browser_config)
        
    async def cleanup(self):
        """Clean up resources."""
        await self._controller.cleanup()
        await super().cleanup()
        
    async def navigate(self, url: str):
        """Navigate to a URL."""
        return await self._controller.navigate(url)
        
    async def click(self, selector: str):
        """Click an element on the page."""
        return await self._controller.click(selector)
        
    async def type_text(self, selector: str, text: str):
        """Type text into an input element."""
        return await self._controller.type_text(selector, text)
        
    async def find_elements(self, by: str = 'selector', value: str = '', case_sensitive: bool = False):
        """Find elements on the page."""
        return await self._controller.find_elements(by, value, case_sensitive)
        
    async def extract_data(self, data_type: str = 'links'):
        """Extract specific data from the page."""
        return await self._controller.extract_data(data_type)
        
    async def get_page_info(self):
        """Get information about the current page."""
        return await self._controller.get_page_info() 