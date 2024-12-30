"""Tool definitions for web surfer operations."""
from typing import Dict, Any, Optional

def navigate_tool() -> Dict[str, Any]:
    """Tool definition for navigating to a URL."""
    return {
        "name": "navigate",
        "description": "Navigate to a URL",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to navigate to"
                }
            },
            "required": ["url"]
        }
    }

def click_tool() -> Dict[str, Any]:
    """Tool definition for clicking elements."""
    return {
        "name": "click",
        "description": "Click an element on the page",
        "parameters": {
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                    "description": "CSS selector for the element to click"
                }
            },
            "required": ["selector"]
        }
    }

def type_text_tool() -> Dict[str, Any]:
    """Tool definition for typing text."""
    return {
        "name": "type_text",
        "description": "Type text into an input element",
        "parameters": {
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                    "description": "CSS selector for the input element"
                },
                "text": {
                    "type": "string",
                    "description": "Text to type"
                }
            },
            "required": ["selector", "text"]
        }
    }

def find_elements_tool() -> Dict[str, Any]:
    """Tool definition for finding elements."""
    return {
        "name": "find_elements",
        "description": "Find elements on the page",
        "parameters": {
            "type": "object",
            "properties": {
                "by": {
                    "type": "string",
                    "description": "Search method: 'selector' or 'text'",
                    "enum": ["selector", "text"]
                },
                "value": {
                    "type": "string",
                    "description": "Search value (selector or text)"
                },
                "case_sensitive": {
                    "type": "boolean",
                    "description": "Whether text search should be case sensitive",
                    "default": False
                }
            },
            "required": ["by", "value"]
        }
    }

def extract_data_tool() -> Dict[str, Any]:
    """Tool definition for extracting data."""
    return {
        "name": "extract_data",
        "description": "Extract specific data from the page",
        "parameters": {
            "type": "object",
            "properties": {
                "data_type": {
                    "type": "string",
                    "description": "Type of data to extract",
                    "enum": ["links", "images", "forms"]
                }
            },
            "required": ["data_type"]
        }
    }

def get_page_info_tool() -> Dict[str, Any]:
    """Tool definition for getting page information."""
    return {
        "name": "get_page_info",
        "description": "Get information about the current page",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }

DEFAULT_TOOLS = [
    navigate_tool(),
    click_tool(),
    type_text_tool(),
    find_elements_tool(),
    extract_data_tool(),
    get_page_info_tool()
] 