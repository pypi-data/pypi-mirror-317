from typing import Any, Dict, List, Optional, Union, Callable, Sequence, TypedDict
import logging
import json
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion
from openai.types.chat.completion_create_params import Function

from ...core.agent import Agent
from ...core.config import AgentConfig

logger = logging.getLogger(__name__)

class ChatMessage(TypedDict):
    role: str
    content: str

class OpenAIAgent(Agent):
    """Agent specialized in direct OpenAI API interactions with enhanced functionality."""
    
    def __init__(
        self,
        config: AgentConfig,
        system_message: Optional[str] = None,
        tools: Optional[Dict[str, Callable]] = None,
        functions: Optional[List[Dict[str, Any]]] = None,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ):
        if system_message is None:
            system_message = """You are an OpenAI API expert that can:
1. Generate text completions
2. Process chat conversations
3. Handle function calling
4. Manage API parameters
5. Optimize API usage and costs"""
            
        super().__init__(config, system_message, tools, functions)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._client: Optional[AsyncOpenAI] = None
        
    async def _ensure_client(self):
        """Ensure OpenAI client exists"""
        if self._client is None:
            self._client = AsyncOpenAI()
            
    async def cleanup(self):
        """Cleanup resources"""
        self._client = None
        await super().cleanup()
        
    async def complete(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Optional[str]:
        """Generate a completion for the given prompt."""
        try:
            await self._ensure_client()
            if not self._client:
                return None
                
            messages: List[ChatMessage] = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens
            )
            
            if response.choices:
                return response.choices[0].message.content
            return None
            
        except Exception as e:
            logger.error(f"Error generating completion: {e}")
            return None
            
    async def chat(
        self,
        messages: Sequence[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Optional[str]:
        """Process a chat conversation."""
        try:
            await self._ensure_client()
            if not self._client:
                return None
                
            api_messages: List[ChatMessage] = [
                {"role": msg["role"], "content": msg["content"]} 
                for msg in messages
            ]
            
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=api_messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens
            )
            
            if response.choices:
                return response.choices[0].message.content
            return None
            
        except Exception as e:
            logger.error(f"Error processing chat: {e}")
            return None
            
    async def function_call(
        self,
        prompt: str,
        functions: Sequence[Function],
        temperature: Optional[float] = None
    ) -> Optional[Dict[str, Any]]:
        """Make a function call using the OpenAI API."""
        try:
            await self._ensure_client()
            if not self._client:
                return None
                
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                functions=list(functions),
                temperature=temperature or self.temperature
            )
            
            if response.choices and response.choices[0].message.function_call:
                return {
                    "name": response.choices[0].message.function_call.name,
                    "arguments": json.loads(response.choices[0].message.function_call.arguments)
                }
            return None
            
        except Exception as e:
            logger.error(f"Error making function call: {e}")
            return None 