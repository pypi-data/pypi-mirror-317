"""Type definitions for Azure AI Agent operations."""
from typing import TypedDict, List, Optional, Dict, Any, Union, Literal

class AzureAIConfig(TypedDict, total=False):
    """Azure AI Agent configuration."""
    subscription_key: str
    endpoint: str
    deployment_name: str
    region: str
    api_version: str

class AgentCapability(TypedDict):
    """Agent capability configuration."""
    name: str
    description: str
    enabled: bool
    parameters: Dict[str, Any]

class AgentTool(TypedDict):
    """Agent tool configuration."""
    name: str
    description: str
    type: Literal["azure_search", "bing_search", "file_search", "function_call", "code_interpreter"]
    parameters: Dict[str, Any]

class AgentMessage(TypedDict):
    """Agent message format."""
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    tool_calls: Optional[List[Dict[str, Any]]]
    tool_responses: Optional[List[Dict[str, Any]]]

class AgentResponse(TypedDict):
    """Agent response format."""
    messages: List[AgentMessage]
    usage: Dict[str, int]
    finish_reason: str
    tool_results: Optional[List[Dict[str, Any]]]

class SearchResult(TypedDict):
    """Search result format."""
    title: str
    url: Optional[str]
    snippet: str
    source: str
    score: float

class FileResult(TypedDict):
    """File operation result."""
    path: str
    content: str
    metadata: Dict[str, Any]

class CodeResult(TypedDict):
    """Code execution result."""
    output: str
    error: Optional[str]
    artifacts: List[Dict[str, Any]] 