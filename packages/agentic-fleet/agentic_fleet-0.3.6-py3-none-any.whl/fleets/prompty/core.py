"""
Prompty integration for prompt management and observability
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class PromptTemplate(BaseModel):
    """Prompt template with variables"""
    name: str
    template: str
    description: Optional[str] = None
    variables: Dict[str, str] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class PromptInvocation(BaseModel):
    """Record of a prompt invocation"""
    template_name: str
    variables: Dict[str, Any]
    rendered_prompt: str
    completion: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    duration_ms: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PromptManager:
    """Manager for prompt templates and invocations"""

    def __init__(self):
        """Initialize prompt manager"""
        self._templates: Dict[str, PromptTemplate] = {}
        self._invocations: List[PromptInvocation] = []

    def add_template(self, template: PromptTemplate) -> None:
        """Add a prompt template

        Args:
            template: Prompt template to add
        """
        self._templates[template.name] = template

    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Get a prompt template by name

        Args:
            name: Template name

        Returns:
            Prompt template if found, None otherwise
        """
        return self._templates.get(name)

    def render_prompt(self, template_name: str, variables: Dict[str, Any]) -> str:
        """Render a prompt template with variables

        Args:
            template_name: Template name
            variables: Variable values

        Returns:
            Rendered prompt

        Raises:
            KeyError: If template not found
            ValueError: If required variables missing
        """
        template = self.get_template(template_name)
        if not template:
            raise KeyError(f"Template '{template_name}' not found")

        try:
            return template.template.format(**variables)
        except KeyError as e:
            raise ValueError(f"Missing required variable: {e}")

    def record_invocation(
        self,
        template_name: str,
        variables: Dict[str, Any],
        rendered_prompt: str,
        completion: Optional[str] = None,
        duration_ms: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> PromptInvocation:
        """Record a prompt invocation

        Args:
            template_name: Template name
            variables: Variable values
            rendered_prompt: Rendered prompt
            completion: Optional completion
            duration_ms: Optional duration in milliseconds
            metadata: Optional metadata

        Returns:
            Recorded invocation
        """
        invocation = PromptInvocation(
            template_name=template_name,
            variables=variables,
            rendered_prompt=rendered_prompt,
            completion=completion,
            duration_ms=duration_ms,
            metadata=metadata or {},
        )
        self._invocations.append(invocation)
        return invocation

    def get_invocations(
        self,
        template_name: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[PromptInvocation]:
        """Get recorded invocations

        Args:
            template_name: Optional template name filter
            limit: Optional limit on number of invocations

        Returns:
            List of invocations
        """
        invocations = self._invocations
        if template_name:
            invocations = [i for i in invocations if i.template_name == template_name]
        if limit:
            invocations = invocations[-limit:]
        return invocations

    def get_template_stats(self, template_name: str) -> Dict[str, Any]:
        """Get statistics for a template

        Args:
            template_name: Template name

        Returns:
            Template statistics
        """
        invocations = self.get_invocations(template_name)
        durations = [i.duration_ms for i in invocations if i.duration_ms is not None]

        return {
            "total_invocations": len(invocations),
            "avg_duration_ms": sum(durations) / len(durations) if durations else None,
            "completion_rate": len([i for i in invocations if i.completion]) / len(invocations) if invocations else 0,
            "last_invocation": invocations[-1].timestamp if invocations else None,
        }


# Global prompt manager instance
_manager: Optional[PromptManager] = None


def get_prompt_manager() -> PromptManager:
    """Get global prompt manager instance

    Returns:
        Prompt manager instance
    """
    global _manager
    if _manager is None:
        _manager = PromptManager()
    return _manager 