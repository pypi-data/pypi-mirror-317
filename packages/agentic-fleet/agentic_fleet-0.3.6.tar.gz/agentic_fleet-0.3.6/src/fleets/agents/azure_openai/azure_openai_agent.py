"""Azure OpenAI agent implementation."""
from typing import Any, Dict, List, Optional, Union, Callable, cast
import logging
import json
import os
from openai import AsyncAzureOpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessage,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionFunctionMessageParam,
)
from openai.types.chat.chat_completion import Choice
from openai.types.chat.completion_create_params import Function
from openai.types.completion_usage import CompletionUsage
from azure.identity import DefaultAzureCredential

from ...core.agent import Agent
from ...core.config import AgentConfig
from ._types import (
    AzureConfig, Message, CompletionResult,
    ChatResult, FunctionCallResult, EmbeddingResult
)

logger = logging.getLogger(__name__)

class AzureOpenAIAgent(Agent):
    """Agent specialized in Azure OpenAI API interactions."""
    
    def __init__(
        self,
        config: AgentConfig,
        system_message: Optional[str] = None,
        tools: Optional[Dict[str, Callable]] = None,
        functions: Optional[List[Dict[str, Any]]] = None,
        azure_config: Optional[AzureConfig] = None
    ):
        if system_message is None:
            system_message = """You are an Azure OpenAI expert that can:
1. Generate text completions
2. Process chat conversations
3. Handle function calling
4. Generate embeddings
5. Optimize API usage and costs"""
            
        super().__init__(config, system_message, tools, functions)
        
        # Initialize Azure OpenAI configuration
        self.azure_config = azure_config or {}
        self._client: Optional[AsyncAzureOpenAI] = None
        
    async def _ensure_client(self):
        """Ensure Azure OpenAI client exists."""
        if self._client is None:
            # Try environment variables first
            api_key = self.azure_config.get('api_key') or os.getenv('AZURE_OPENAI_API_KEY')
            endpoint = self.azure_config.get('endpoint') or os.getenv('AZURE_OPENAI_ENDPOINT')
            api_version = self.azure_config.get('api_version') or os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
            
            if api_key and endpoint:
                self._client = AsyncAzureOpenAI(
                    api_key=api_key,
                    api_version=api_version,
                    azure_endpoint=endpoint
                )
            elif endpoint:
                # Fall back to Azure credentials
                credential = DefaultAzureCredential()
                self._client = AsyncAzureOpenAI(
                    api_version=api_version,
                    azure_endpoint=endpoint,
                    azure_ad_token_provider=credential
                )
                
    async def cleanup(self):
        """Clean up resources."""
        self._client = None
        await super().cleanup()
        
    def _convert_to_chat_message(self, message: Message) -> ChatCompletionMessageParam:
        """Convert internal message format to OpenAI chat message format."""
        if message["role"] == "system":
            return ChatCompletionSystemMessageParam(
                role="system",
                content=message["content"]
            )
        elif message["role"] == "user":
            return ChatCompletionUserMessageParam(
                role="user",
                content=message["content"]
            )
        elif message["role"] == "assistant":
            return ChatCompletionAssistantMessageParam(
                role="assistant",
                content=message["content"]
            )
        else:  # function
            return ChatCompletionFunctionMessageParam(
                role="function",
                content=message["content"],
                name=message["name"] or ""
            )
            
    def _extract_usage(self, usage: Optional[CompletionUsage]) -> Dict[str, int]:
        """Extract usage information from response."""
        if usage:
            return {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens
            }
        return {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
        
    def _convert_to_function(self, func_dict: Dict[str, Any]) -> Function:
        """Convert function dictionary to OpenAI Function type."""
        return Function(
            name=func_dict["name"],
            description=func_dict.get("description", ""),
            parameters=func_dict.get("parameters", {})
        )
        
    async def complete(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Optional[CompletionResult]:
        """Generate a completion for the given prompt."""
        try:
            await self._ensure_client()
            if not self._client:
                return None
                
            messages: List[ChatCompletionMessageParam] = []
            if system_message:
                messages.append(self._convert_to_chat_message({
                    "role": "system",
                    "content": system_message,
                    "name": None,
                    "function_call": None
                }))
            messages.append(self._convert_to_chat_message({
                "role": "user",
                "content": prompt,
                "name": None,
                "function_call": None
            }))
            
            response = await self._client.chat.completions.create(
                model=self.azure_config.get('deployment_name', 'gpt-4o'),
                messages=messages,
                temperature=temperature or self.azure_config.get('temperature', 0.7),
                max_tokens=max_tokens or self.azure_config.get('max_tokens'),
                top_p=self.azure_config.get('top_p', 1.0),
                frequency_penalty=self.azure_config.get('frequency_penalty', 0.0),
                presence_penalty=self.azure_config.get('presence_penalty', 0.0),
                stop=self.azure_config.get('stop')
            )
            
            if response.choices:
                return {
                    "text": response.choices[0].message.content or "",
                    "finish_reason": response.choices[0].finish_reason or "",
                    "usage": self._extract_usage(response.usage)
                }
            return None
            
        except Exception as e:
            logger.error(f"Error generating completion: {e}")
            return None
            
    async def chat(
        self,
        messages: List[Message],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Optional[ChatResult]:
        """Process a chat conversation."""
        try:
            await self._ensure_client()
            if not self._client:
                return None
                
            chat_messages = [self._convert_to_chat_message(msg) for msg in messages]
            
            response = await self._client.chat.completions.create(
                model=self.azure_config.get('deployment_name', 'gpt-4o'),
                messages=chat_messages,
                temperature=temperature or self.azure_config.get('temperature', 0.7),
                max_tokens=max_tokens or self.azure_config.get('max_tokens'),
                top_p=self.azure_config.get('top_p', 1.0),
                frequency_penalty=self.azure_config.get('frequency_penalty', 0.0),
                presence_penalty=self.azure_config.get('presence_penalty', 0.0),
                stop=self.azure_config.get('stop')
            )
            
            if response.choices:
                return {
                    "messages": messages + [{
                        "role": "assistant",
                        "content": response.choices[0].message.content or "",
                        "name": None,
                        "function_call": None
                    }],
                    "usage": self._extract_usage(response.usage),
                    "finish_reason": response.choices[0].finish_reason or ""
                }
            return None
            
        except Exception as e:
            logger.error(f"Error processing chat: {e}")
            return None
            
    async def function_call(
        self,
        prompt: str,
        functions: List[Dict[str, Any]],
        temperature: Optional[float] = None
    ) -> Optional[FunctionCallResult]:
        """Make a function call using the Azure OpenAI API."""
        try:
            await self._ensure_client()
            if not self._client:
                return None
                
            openai_functions = [self._convert_to_function(f) for f in functions]
            
            response = await self._client.chat.completions.create(
                model=self.azure_config.get('deployment_name', 'gpt-4o'),
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                functions=openai_functions,
                temperature=temperature or self.azure_config.get('temperature', 0.7)
            )
            
            if response.choices and response.choices[0].message.function_call:
                return {
                    "name": response.choices[0].message.function_call.name,
                    "arguments": json.loads(response.choices[0].message.function_call.arguments),
                    "response": response.choices[0].message.content
                }
            return None
            
        except Exception as e:
            logger.error(f"Error making function call: {e}")
            return None
            
    async def embed(
        self,
        text: Union[str, List[str]],
        model: Optional[str] = None
    ) -> Optional[Union[EmbeddingResult, List[EmbeddingResult]]]:
        """Generate embeddings for text."""
        try:
            await self._ensure_client()
            if not self._client:
                return None
                
            response = await self._client.embeddings.create(
                model=model or self.azure_config.get('deployment_name', 'text-embedding-ada-002'),
                input=text
            )
            
            if isinstance(text, str):
                if response.data:
                    return {
                        "embedding": response.data[0].embedding,
                        "usage": {
                            "prompt_tokens": response.usage.prompt_tokens,
                            "total_tokens": response.usage.total_tokens
                        }
                    }
            else:
                return [{
                    "embedding": data.embedding,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "total_tokens": response.usage.total_tokens
                    }
                } for data in response.data]
            return None
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return None 