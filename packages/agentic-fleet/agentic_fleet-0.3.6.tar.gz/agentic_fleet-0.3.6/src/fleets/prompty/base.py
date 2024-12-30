"""
Base prompt management functionality with improved error handling and validation.
"""

import os
from typing import Dict, Any, Optional, List
from functools import lru_cache
import yaml
from pydantic import BaseModel, Field


class PromptLoadError(Exception):
    """Error loading prompt file"""
    pass


class PromptParseError(Exception):
    """Error parsing prompt content"""
    pass


class ToolParameter(BaseModel):
    """Tool parameter definition"""
    name: str
    description: str
    type: str = Field(default="string")
    required: bool = True


class Tool(BaseModel):
    """Tool definition"""
    name: str
    description: str
    parameters: List[ToolParameter]


class PromptConfig(BaseModel):
    """Prompt configuration"""
    name: str
    description: str
    version: str
    author: str
    system_message: str
    tools: List[Tool]
    examples: Dict[str, Any]


class BasePromptManager:
    """Base class for prompt management with caching and validation"""
    
    def __init__(self, prompts_dir: Optional[str] = None):
        """Initialize prompt manager
        
        Args:
            prompts_dir: Optional custom prompts directory path
        """
        self.prompts_dir = prompts_dir or os.path.dirname(__file__)
        
    def _load_prompt(self, filename: str) -> Dict[str, Any]:
        """Load a prompt file
        
        Args:
            filename: Name of the prompt file to load
            
        Returns:
            Loaded prompt configuration
            
        Raises:
            PromptLoadError: If file cannot be loaded
            PromptParseError: If file content cannot be parsed
        """
        try:
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
                raise PromptParseError(f"Invalid prompt format in {filename}")
        except FileNotFoundError:
            raise PromptLoadError(f"Prompt file not found: {filename}")
        except yaml.YAMLError as e:
            raise PromptParseError(f"Invalid YAML in {filename}: {str(e)}")
        except Exception as e:
            raise PromptLoadError(f"Error loading {filename}: {str(e)}")
            
    @lru_cache(maxsize=32)
    def get_prompt(self, name: str) -> Dict[str, Any]:
        """Get a prompt configuration with caching
        
        Args:
            name: Name of the prompt to load
            
        Returns:
            Prompt configuration
        """
        return self._load_prompt(f"{name}.prompty")
            
    def get_system_message(self, content: str) -> str:
        """Extract system message from prompt content
        
        Args:
            content: Prompt content string
            
        Returns:
            System message string
        """
        system_start = content.find("system:") + 8
        tools_start = content.find("# Tools")
        return content[system_start:tools_start].strip()
        
    def parse_tools(self, content: str) -> List[Tool]:
        """Parse tools section from prompt content
        
        Args:
            content: Prompt content string
            
        Returns:
            List of parsed tools
        """
        tools_start = content.find("# Tools")
        example_start = content.find("# Example")
        tools_section = content[tools_start:example_start]
        
        tools = []
        current_tool = None
        
        for line in tools_section.split('\n'):
            if line.startswith('## '):
                if current_tool:
                    tools.append(Tool(**current_tool))
                current_tool = {
                    "name": line[3:].strip(),
                    "description": "",
                    "parameters": []
                }
            elif line.strip().startswith('- ') and current_tool:
                param_line = line.strip()[2:]
                name, *desc = param_line.split(':')
                param = {
                    "name": name.strip(),
                    "description": ':'.join(desc).strip(),
                    "type": "string",
                    "required": True
                }
                current_tool["parameters"].append(ToolParameter(**param))
                
        if current_tool:
            tools.append(Tool(**current_tool))
            
        return tools
        
    def validate_prompt(self, prompt_data: Dict[str, Any]) -> PromptConfig:
        """Validate prompt data against schema
        
        Args:
            prompt_data: Prompt data to validate
            
        Returns:
            Validated prompt configuration
            
        Raises:
            PromptParseError: If validation fails
        """
        try:
            return PromptConfig(**prompt_data)
        except Exception as e:
            raise PromptParseError(f"Invalid prompt configuration: {str(e)}") 