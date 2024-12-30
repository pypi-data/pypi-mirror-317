"""Markdown file browser implementation."""
from typing import List, Dict, Any, Optional, Union
import logging
from pathlib import Path
import re

logger = logging.getLogger(__name__)

class MarkdownFileBrowser:
    """Browser for markdown files with enhanced functionality."""
    
    def __init__(self, base_dir: Optional[Union[str, Path]] = None):
        """Initialize markdown browser."""
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        
    def _resolve_path(self, path: Union[str, Path]) -> Path:
        """Resolve path relative to base_dir."""
        path = Path(path)
        return path if path.is_absolute() else self.base_dir / path
        
    def extract_headers(self, content: str) -> List[Dict[str, Any]]:
        """Extract markdown headers with their levels."""
        headers = []
        for line in content.split('\n'):
            if line.startswith('#'):
                match = re.match(r'^#+', line)
                if match:
                    level = len(match.group())
                    text = line.lstrip('#').strip()
                    headers.append({
                        "level": level,
                        "text": text,
                        "line": content.split('\n').index(line) + 1
                    })
        return headers
        
    def extract_links(self, content: str) -> List[Dict[str, str]]:
        """Extract markdown links."""
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        return [
            {"text": match.group(1), "url": match.group(2)}
            for match in re.finditer(link_pattern, content)
        ]
        
    def extract_code_blocks(self, content: str) -> List[Dict[str, Any]]:
        """Extract code blocks with language info."""
        blocks = []
        in_block = False
        current_block = {"language": "", "code": [], "start_line": 0}
        
        for i, line in enumerate(content.split('\n'), 1):
            if line.startswith('```'):
                if not in_block:
                    in_block = True
                    current_block = {
                        "language": line[3:].strip(),
                        "code": [],
                        "start_line": i
                    }
                else:
                    in_block = False
                    if current_block["code"]:
                        blocks.append(dict(current_block))
            elif in_block:
                current_block["code"].append(line)
                
        return blocks
        
    def extract_lists(self, content: str) -> List[Dict[str, Any]]:
        """Extract markdown lists."""
        lists = []
        current_list = {"items": [], "start_line": 0, "type": ""}
        in_list = False
        
        for i, line in enumerate(content.split('\n'), 1):
            stripped = line.strip()
            if re.match(r'^[-*+]\s', stripped):  # Unordered list
                if not in_list:
                    in_list = True
                    current_list = {"items": [], "start_line": i, "type": "unordered"}
                current_list["items"].append(stripped[2:])
            elif re.match(r'^\d+\.\s', stripped):  # Ordered list
                if not in_list:
                    in_list = True
                    current_list = {"items": [], "start_line": i, "type": "ordered"}
                current_list["items"].append(stripped[stripped.find(' ')+1:])
            elif in_list and not stripped:
                in_list = False
                if current_list["items"]:
                    lists.append(dict(current_list))
                    
        if in_list and current_list["items"]:
            lists.append(dict(current_list))
            
        return lists
        
    def extract_tables(self, content: str) -> List[Dict[str, Any]]:
        """Extract markdown tables."""
        tables = []
        current_table = {"headers": [], "rows": [], "start_line": 0}
        in_table = False
        
        for i, line in enumerate(content.split('\n'), 1):
            stripped = line.strip()
            if stripped.startswith('|') and stripped.endswith('|'):
                cells = [cell.strip() for cell in stripped[1:-1].split('|')]
                if not in_table:
                    in_table = True
                    current_table = {"headers": cells, "rows": [], "start_line": i}
                elif re.match(r'^\|[-:| ]+\|$', stripped):  # Separator line
                    continue
                else:
                    current_table["rows"].append(cells)
            elif in_table:
                in_table = False
                if current_table["headers"] and current_table["rows"]:
                    tables.append(dict(current_table))
                    
        if in_table and current_table["headers"] and current_table["rows"]:
            tables.append(dict(current_table))
            
        return tables
        
    def analyze_markdown(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Analyze a markdown file and extract its structure."""
        try:
            file_path = self._resolve_path(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            return {
                "headers": self.extract_headers(content),
                "links": self.extract_links(content),
                "code_blocks": self.extract_code_blocks(content),
                "lists": self.extract_lists(content),
                "tables": self.extract_tables(content),
                "word_count": len(content.split()),
                "line_count": len(content.split('\n'))
            }
            
        except Exception as e:
            logger.error(f"Error analyzing markdown file {file_path}: {e}")
            return {} 