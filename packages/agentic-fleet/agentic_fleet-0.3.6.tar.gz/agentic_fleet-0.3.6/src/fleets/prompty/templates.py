"""
Template management with inheritance and composition support.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import jinja2
from .base import BasePromptManager, PromptConfig, Tool


class TemplateManager:
    """Manager for prompt templates with inheritance and composition"""
    
    def __init__(self, templates_dir: Optional[str] = None):
        """Initialize template manager
        
        Args:
            templates_dir: Optional custom templates directory path
        """
        self.templates_dir = templates_dir or str(Path(__file__).parent / "templates")
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
    def render_template(self, template_name: str, **kwargs) -> str:
        """Render a template with provided variables
        
        Args:
            template_name: Name of template to render
            **kwargs: Template variables
            
        Returns:
            Rendered template string
        """
        template = self.env.get_template(template_name)
        return template.render(**kwargs)


class PromptTemplate:
    """Base class for prompt templates"""
    
    def __init__(self, name: str, description: str):
        """Initialize prompt template
        
        Args:
            name: Template name
            description: Template description
        """
        self.name = name
        self.description = description
        self.system_message = ""
        self.tools: List[Tool] = []
        self.examples: Dict[str, Any] = {}
        
    def add_tool(self, tool: Tool) -> 'PromptTemplate':
        """Add a tool to the template
        
        Args:
            tool: Tool to add
            
        Returns:
            Self for chaining
        """
        self.tools.append(tool)
        return self
        
    def add_example(self, name: str, example: Dict[str, Any]) -> 'PromptTemplate':
        """Add an example to the template
        
        Args:
            name: Example name
            example: Example data
            
        Returns:
            Self for chaining
        """
        self.examples[name] = example
        return self
        
    def extend(self, other: 'PromptTemplate') -> 'PromptTemplate':
        """Extend this template with another
        
        Args:
            other: Template to extend from
            
        Returns:
            New combined template
        """
        new_template = PromptTemplate(
            f"{self.name}_extended",
            f"{self.description} (extended from {other.name})"
        )
        new_template.system_message = self.system_message + "\n" + other.system_message
        new_template.tools = self.tools + other.tools
        new_template.examples = {**other.examples, **self.examples}
        return new_template
        
    def to_config(self) -> PromptConfig:
        """Convert template to prompt configuration
        
        Returns:
            Prompt configuration
        """
        return PromptConfig(
            name=self.name,
            description=self.description,
            version="1.0.0",
            author="System",
            system_message=self.system_message,
            tools=self.tools,
            examples=self.examples
        )


class BaseAgentTemplate(PromptTemplate):
    """Base template for agent prompts"""
    
    def __init__(self):
        """Initialize base agent template"""
        super().__init__(
            name="base_agent",
            description="Base template for agent prompts"
        )
        self.system_message = """
        You are an AI agent designed to assist with specific tasks.
        Follow these guidelines:
        1. Be clear and concise in your responses
        2. Use available tools appropriately
        3. Handle errors gracefully
        4. Provide helpful feedback
        """


class BasePlannerTemplate(BaseAgentTemplate):
    """Base template for planner agents"""
    
    def __init__(self):
        """Initialize base planner template"""
        super().__init__()
        self.name = "base_planner"
        self.description = "Base template for planner agents"
        self.system_message += """
        As a planner agent:
        1. Break down complex tasks into manageable steps
        2. Consider dependencies between tasks
        3. Estimate resource requirements
        4. Create clear execution plans
        """


class BaseExecutorTemplate(BaseAgentTemplate):
    """Base template for executor agents"""
    
    def __init__(self):
        """Initialize base executor template"""
        super().__init__()
        self.name = "base_executor"
        self.description = "Base template for executor agents"
        self.system_message += """
        As an executor agent:
        1. Execute tasks according to plan
        2. Monitor progress and handle errors
        3. Report status updates
        4. Optimize execution when possible
        """ 