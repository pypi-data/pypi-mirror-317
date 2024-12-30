"""
Tool management prompt management and loading
"""

import os
import yaml
from typing import Dict, Any, Optional

class ToolPrompts:
    """Manager for Tool management prompts"""
    
    def __init__(self, prompts_dir: Optional[str] = None):
        """Initialize prompt manager
        
        Args:
            prompts_dir: Optional custom prompts directory path
        """
        self.prompts_dir = prompts_dir or os.path.dirname(__file__)
        self.base_prompt = self._load_prompt("base.prompty")
        
    def _load_prompt(self, filename: str) -> Dict[str, Any]:
        """Load a Prompty file
        
        Args:
            filename: Name of the Prompty file to load
            
        Returns:
            Loaded prompt configuration
        """
        prompt_path = os.path.join(self.prompts_dir, filename)
        with open(prompt_path, 'r') as f:
            content = f.read().split('---', 2)
            if len(content) >= 3:
                frontmatter = yaml.safe_load(content[1])
                prompt_content = content[2].strip()
                return {
                    **frontmatter,
                    "content": prompt_content
                }
            return {}
            
    def get_system_message(self) -> str:
        """Get the system message for tool management
        
        Returns:
            System message string
        """
        content = self.base_prompt.get("content", "")
        system_start = content.find("system:") + 8
        tools_start = content.find("# Tools")
        return content[system_start:tools_start].strip()
        
    def get_tools(self) -> list:
        """Get the tool configurations
        
        Returns:
            List of tool configurations
        """
        content = self.base_prompt.get("content", "")
        tools_start = content.find("# Tools")
        example_start = content.find("# Example")
        tools_section = content[tools_start:example_start]
        
        tools = []
        current_tool = None
        
        for line in tools_section.split('\n'):
            if line.startswith('## '):
                if current_tool:
                    tools.append(current_tool)
                current_tool = {"name": line[3:].strip(), "parameters": []}
            elif line.strip().startswith('- ') and current_tool:
                param = line.strip()[2:]
                current_tool["parameters"].append(param)
                
        if current_tool:
            tools.append(current_tool)
            
        return tools
        
    def get_examples(self) -> Dict[str, Any]:
        """Get the example configurations
        
        Returns:
            Example configurations
        """
        return self.base_prompt.get("sample", {}) 