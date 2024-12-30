"""Tool definitions for file surfer operations."""
from typing import List, Dict, Any, Optional
from pathlib import Path

def list_directory_tool(path: Optional[str] = None) -> Dict[str, Any]:
    """Tool definition for listing directory contents."""
    return {
        "name": "list_directory",
        "description": "List contents of a directory",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to directory. If not provided, uses current directory."
                }
            }
        }
    }

def read_file_tool() -> Dict[str, Any]:
    """Tool definition for reading file contents."""
    return {
        "name": "read_file",
        "description": "Read contents of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to file to read"
                },
                "encoding": {
                    "type": "string",
                    "description": "File encoding",
                    "default": "utf-8"
                }
            },
            "required": ["path"]
        }
    }

def write_file_tool() -> Dict[str, Any]:
    """Tool definition for writing file contents."""
    return {
        "name": "write_file",
        "description": "Write content to a file",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to file to write"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to file"
                },
                "encoding": {
                    "type": "string",
                    "description": "File encoding",
                    "default": "utf-8"
                }
            },
            "required": ["path", "content"]
        }
    }

def search_files_tool() -> Dict[str, Any]:
    """Tool definition for searching files."""
    return {
        "name": "search_files",
        "description": "Search for files matching a pattern",
        "parameters": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Pattern to search for in filenames"
                },
                "path": {
                    "type": "string",
                    "description": "Base directory for search. If not provided, uses current directory."
                }
            },
            "required": ["pattern"]
        }
    }

def file_exists_tool() -> Dict[str, Any]:
    """Tool definition for checking file existence."""
    return {
        "name": "file_exists",
        "description": "Check if a file exists",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to file to check"
                }
            },
            "required": ["path"]
        }
    }

DEFAULT_TOOLS = [
    list_directory_tool(),
    read_file_tool(),
    write_file_tool(),
    search_files_tool(),
    file_exists_tool()
] 