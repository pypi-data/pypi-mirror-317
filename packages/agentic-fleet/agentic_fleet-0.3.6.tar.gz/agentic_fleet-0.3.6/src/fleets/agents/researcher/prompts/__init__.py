"""
Researcher Agent prompt management and loading
"""

import os
import yaml
from typing import Dict, Any, Optional

class ResearcherPrompts:
    """Manager for Researcher Agent prompts"""
    
    def __init__(self, prompts_dir: Optional[str] = None):
        """Initialize prompt manager
        
        Args:
            prompts_dir: Optional custom prompts directory path
        """
        self.prompts_dir = prompts_dir or os.path.dirname(__file__)
        self.base_prompt = self._load_prompt("base.yaml")
        
    def _load_prompt(self, filename: str) -> Dict[str, Any]:
        """Load a YAML prompt file
        
        Args:
            filename: Name of the YAML file to load
            
        Returns:
            Loaded prompt configuration
        """
        prompt_path = os.path.join(self.prompts_dir, filename)
        with open(prompt_path, 'r') as f:
            return yaml.safe_load(f)
            
    def get_system_message(self) -> str:
        """Get the system message for the researcher agent
        
        Returns:
            System message string
        """
        return self.base_prompt.get("system_message", "")
        
    def get_tools(self) -> list:
        """Get the tool configurations
        
        Returns:
            List of tool configurations
        """
        return self.base_prompt.get("tools", [])
        
    def get_research_aspects(self) -> list:
        """Get the research aspects
        
        Returns:
            List of research aspects
        """
        return self.base_prompt.get("research_aspects", [])
        
    def get_examples(self) -> list:
        """Get the example configurations
        
        Returns:
            List of examples
        """
        return self.base_prompt.get("examples", []) 