"""
Testing utilities for prompt management.
"""

import pytest
from typing import Dict, Any, Optional
from .base import BasePromptManager, PromptConfig, Tool, ToolParameter


class MockPromptManager(BasePromptManager):
    """Mock prompt manager for testing"""
    
    def __init__(self, mock_prompts: Dict[str, Any]):
        """Initialize mock prompt manager
        
        Args:
            mock_prompts: Dictionary of mock prompts
        """
        super().__init__()
        self.mock_prompts = mock_prompts
        
    def get_prompt(self, name: str) -> Dict[str, Any]:
        """Get a mock prompt
        
        Args:
            name: Name of the prompt to get
            
        Returns:
            Mock prompt data
        """
        return self.mock_prompts.get(name, {})


@pytest.fixture
def sample_tool_parameter() -> Dict[str, Any]:
    """Fixture providing a sample tool parameter"""
    return {
        "name": "test_param",
        "description": "Test parameter",
        "type": "string",
        "required": True
    }


@pytest.fixture
def sample_tool() -> Dict[str, Any]:
    """Fixture providing a sample tool"""
    return {
        "name": "test_tool",
        "description": "Test tool",
        "parameters": [
            {
                "name": "param1",
                "description": "First parameter",
                "type": "string",
                "required": True
            },
            {
                "name": "param2", 
                "description": "Second parameter",
                "type": "integer",
                "required": False
            }
        ]
    }


@pytest.fixture
def sample_prompt_config() -> Dict[str, Any]:
    """Fixture providing a sample prompt configuration"""
    return {
        "name": "test_prompt",
        "description": "Test prompt configuration",
        "version": "1.0.0",
        "author": "Test Author",
        "system_message": "Test system message",
        "tools": [
            {
                "name": "tool1",
                "description": "First tool",
                "parameters": [
                    {
                        "name": "param1",
                        "description": "Parameter one",
                        "type": "string",
                        "required": True
                    }
                ]
            }
        ],
        "examples": {
            "basic": {
                "input": "Test input",
                "output": "Test output"
            }
        }
    }


@pytest.fixture
def mock_prompt_manager(sample_prompt_config: Dict[str, Any]) -> MockPromptManager:
    """Fixture providing a mock prompt manager
    
    Args:
        sample_prompt_config: Sample prompt configuration
        
    Returns:
        Configured mock prompt manager
    """
    mock_prompts = {
        "base": sample_prompt_config
    }
    return MockPromptManager(mock_prompts)


def test_prompt_loading(mock_prompt_manager: MockPromptManager):
    """Test prompt loading functionality
    
    Args:
        mock_prompt_manager: Mock prompt manager fixture
    """
    prompt = mock_prompt_manager.get_prompt("base")
    assert prompt["name"] == "test_prompt"
    assert prompt["version"] == "1.0.0"
    assert len(prompt["tools"]) == 1


def test_prompt_validation(mock_prompt_manager: MockPromptManager):
    """Test prompt validation functionality
    
    Args:
        mock_prompt_manager: Mock prompt manager fixture
    """
    prompt_data = mock_prompt_manager.get_prompt("base")
    config = mock_prompt_manager.validate_prompt(prompt_data)
    assert isinstance(config, PromptConfig)
    assert len(config.tools) == 1
    assert isinstance(config.tools[0], Tool)
    assert isinstance(config.tools[0].parameters[0], ToolParameter) 