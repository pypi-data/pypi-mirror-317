"""File surfer agent implementation."""
from typing import Any, Dict, List, Optional, Union, Callable
import logging
import os
from pathlib import Path

from ...core.agent import Agent
from ...core.config import AgentConfig
from ._markdown_file_browser import MarkdownFileBrowser
from ._tool_definitions import DEFAULT_TOOLS

logger = logging.getLogger(__name__)

class FileSurferAgent(Agent):
    """Agent specialized in file system operations and content manipulation."""
    
    def __init__(
        self,
        config: AgentConfig,
        system_message: Optional[str] = None,
        tools: Optional[Dict[str, Callable]] = None,
        functions: Optional[List[Dict[str, Any]]] = None,
        base_dir: Optional[Union[str, Path]] = None
    ):
        if system_message is None:
            system_message = """You are a file system expert that can:
1. Navigate and explore directory structures
2. Read and write files
3. Search for files by name or content
4. Analyze file contents and provide summaries
5. Perform file operations safely and efficiently"""
            
        # Add default file surfer tools
        if functions is None:
            functions = []
        functions.extend(DEFAULT_TOOLS)
            
        super().__init__(config, system_message, tools, functions)
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.markdown_browser = MarkdownFileBrowser(self.base_dir)
        
    def _resolve_path(self, path: Optional[Union[str, Path]]) -> Path:
        """Resolve path relative to base_dir."""
        if path is None:
            return self.base_dir
        path = Path(path)
        return path if path.is_absolute() else self.base_dir / path
        
    async def read_file(self, file_path: Union[str, Path], encoding: str = 'utf-8') -> Optional[str]:
        """Read contents of a file."""
        try:
            file_path = self._resolve_path(file_path)
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None
            
    async def write_file(self, file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> bool:
        """Write content to a file."""
        try:
            file_path = self._resolve_path(file_path)
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"Error writing to file {file_path}: {e}")
            return False
            
    async def list_directory(self, dir_path: Optional[Union[str, Path]] = None) -> Optional[List[str]]:
        """List contents of a directory."""
        try:
            dir_path = self._resolve_path(dir_path) if dir_path else self.base_dir
            return sorted(os.listdir(dir_path))
        except Exception as e:
            logger.error(f"Error listing directory {dir_path}: {e}")
            return None
            
    async def search_files(self, pattern: str, dir_path: Optional[Union[str, Path]] = None) -> List[Path]:
        """Search for files matching a pattern."""
        try:
            dir_path = self._resolve_path(dir_path) if dir_path else self.base_dir
            matches = []
            for root, _, files in os.walk(dir_path):
                for filename in files:
                    if pattern in filename:
                        matches.append(Path(root) / filename)
            return sorted(matches)
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            return []
            
    async def file_exists(self, file_path: Union[str, Path]) -> bool:
        """Check if a file exists."""
        try:
            file_path = self._resolve_path(file_path)
            return file_path.exists()
        except Exception:
            return False
            
    async def analyze_markdown(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Analyze a markdown file and extract its structure."""
        try:
            file_path = self._resolve_path(file_path)
            if not file_path.exists() or not file_path.suffix.lower() == '.md':
                logger.error(f"Invalid markdown file: {file_path}")
                return {}
                
            return self.markdown_browser.analyze_markdown(file_path)
            
        except Exception as e:
            logger.error(f"Error analyzing markdown file {file_path}: {e}")
            return {}
