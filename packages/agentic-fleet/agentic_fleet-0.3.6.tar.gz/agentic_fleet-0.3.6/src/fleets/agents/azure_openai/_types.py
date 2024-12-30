"""Type definitions for Azure OpenAI operations."""
from typing import TypedDict, List, Optional, Dict, Any, Union, Literal

class AzureConfig(TypedDict, total=False):
    """Azure OpenAI configuration."""
    api_version: str
    api_key: str
    endpoint: str
    deployment_name: str
    model: str
    temperature: float
    max_tokens: int
    top_p: float
    frequency_penalty: float
    presence_penalty: float
    stop: Optional[List[str]]

class Message(TypedDict):
    """Chat message format."""
    role: Literal["system", "user", "assistant", "function"]
    content: str
    name: Optional[str]
    function_call: Optional[Dict[str, str]]

class CompletionResult(TypedDict):
    """Result of a completion request."""
    text: str
    finish_reason: str
    usage: Dict[str, int]

class ChatResult(TypedDict):
    """Result of a chat request."""
    messages: List[Message]
    usage: Dict[str, int]
    finish_reason: str

class FunctionCallResult(TypedDict):
    """Result of a function call."""
    name: str
    arguments: Dict[str, Any]
    response: Optional[str]

class EmbeddingResult(TypedDict):
    """Result of an embedding request."""
    embedding: List[float]
    usage: Dict[str, int] 