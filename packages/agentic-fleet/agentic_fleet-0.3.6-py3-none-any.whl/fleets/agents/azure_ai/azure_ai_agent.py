"""Azure AI Agent implementation."""
from typing import Any, Dict, List, Optional, Union, Callable, Literal
import logging
import json
import os
import aiohttp
from azure.identity import DefaultAzureCredential

from ...core.agent import Agent
from ...core.config import AgentConfig
from ._types import (
    AzureAIConfig, AgentCapability, AgentTool, AgentMessage,
    AgentResponse, SearchResult, FileResult, CodeResult
)

logger = logging.getLogger(__name__)

class AzureAIAgent(Agent):
    """Agent specialized in Azure AI Agent Service interactions."""
    
    def __init__(
        self,
        config: AgentConfig,
        system_message: Optional[str] = None,
        tools: Optional[Dict[str, Callable]] = None,
        capabilities: Optional[List[AgentCapability]] = None,
        azure_config: Optional[AzureAIConfig] = None
    ):
        if system_message is None:
            system_message = """You are an Azure AI Agent that can:
1. Process natural language requests
2. Use Azure Cognitive Search
3. Use Bing Search
4. Handle file operations
5. Execute code and analyze data
6. Integrate with custom tools and APIs"""
            
        super().__init__(config, system_message, tools)
        
        # Initialize Azure AI configuration
        self.azure_config = azure_config or {}
        self.capabilities = capabilities or []
        self._session: Optional[aiohttp.ClientSession] = None
        self._credential: Optional[DefaultAzureCredential] = None
        
    async def _ensure_session(self):
        """Ensure aiohttp session and credentials exist."""
        if self._session is None:
            self._session = aiohttp.ClientSession()
            
        if self._credential is None:
            self._credential = DefaultAzureCredential()
            
    async def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        subscription_key = self.azure_config.get('subscription_key') or os.getenv('AZURE_AI_SUBSCRIPTION_KEY')
        if subscription_key:
            return {
                'Ocp-Apim-Subscription-Key': subscription_key,
                'Content-Type': 'application/json'
            }
        elif self._credential:
            # Use Azure AD authentication
            token = await self._credential.get_token("https://cognitiveservices.azure.com/.default")
            return {
                'Authorization': f'Bearer {token.token}',
                'Content-Type': 'application/json'
            }
        else:
            raise ValueError("No authentication method available")
            
    def _get_endpoint(self, path: str = "") -> str:
        """Get the full endpoint URL."""
        endpoint = self.azure_config.get('endpoint') or os.getenv('AZURE_AI_ENDPOINT')
        if not endpoint:
            raise ValueError("Azure AI endpoint not configured")
            
        api_version = self.azure_config.get('api_version') or os.getenv('AZURE_AI_API_VERSION', '2024-02-01-preview')
        base_url = f"{endpoint}/language/agents/v1.0"
        
        if path:
            return f"{base_url}/{path}?api-version={api_version}"
        return f"{base_url}?api-version={api_version}"
        
    async def cleanup(self):
        """Clean up resources."""
        if self._session:
            await self._session.close()
            self._session = None
        await super().cleanup()
        
    async def chat(
        self,
        messages: List[AgentMessage],
        tools: Optional[List[AgentTool]] = None
    ) -> Optional[AgentResponse]:
        """Process a chat conversation with the agent."""
        try:
            await self._ensure_session()
            if not self._session:
                return None
                
            headers = await self._get_headers()
            endpoint = self._get_endpoint("chat")
            
            payload = {
                "messages": messages,
                "tools": tools or [],
                "capabilities": self.capabilities
            }
            
            async with self._session.post(endpoint, headers=headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return AgentResponse(
                        messages=result["messages"],
                        usage=result["usage"],
                        finish_reason=result["finish_reason"],
                        tool_results=result.get("tool_results")
                    )
                else:
                    error = await response.text()
                    logger.error(f"Error in chat: {error}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return None
            
    async def search(
        self,
        query: str,
        search_type: Literal["azure", "bing"] = "azure",
        filters: Optional[Dict[str, Any]] = None
    ) -> Optional[List[SearchResult]]:
        """Perform a search using Azure Cognitive Search or Bing."""
        try:
            await self._ensure_session()
            if not self._session:
                return None
                
            headers = await self._get_headers()
            endpoint = self._get_endpoint(f"search/{search_type}")
            
            payload = {
                "query": query,
                "filters": filters or {}
            }
            
            async with self._session.post(endpoint, headers=headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return [SearchResult(**item) for item in result["results"]]
                else:
                    error = await response.text()
                    logger.error(f"Error in search: {error}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error in search: {e}")
            return None
            
    async def process_file(
        self,
        operation: Literal["read", "write", "search"],
        path: str,
        content: Optional[str] = None,
        query: Optional[str] = None
    ) -> Optional[Union[FileResult, List[FileResult]]]:
        """Process file operations."""
        try:
            await self._ensure_session()
            if not self._session:
                return None
                
            headers = await self._get_headers()
            endpoint = self._get_endpoint("files")
            
            payload = {
                "operation": operation,
                "path": path,
                "content": content,
                "query": query
            }
            
            async with self._session.post(endpoint, headers=headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    if operation == "search":
                        return [FileResult(**item) for item in result["results"]]
                    return FileResult(**result)
                else:
                    error = await response.text()
                    logger.error(f"Error in file operation: {error}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error in file operation: {e}")
            return None
            
    async def execute_code(
        self,
        code: str,
        language: str,
        inputs: Optional[Dict[str, Any]] = None
    ) -> Optional[CodeResult]:
        """Execute code using the code interpreter."""
        try:
            await self._ensure_session()
            if not self._session:
                return None
                
            headers = await self._get_headers()
            endpoint = self._get_endpoint("code/execute")
            
            payload = {
                "code": code,
                "language": language,
                "inputs": inputs or {}
            }
            
            async with self._session.post(endpoint, headers=headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return CodeResult(**result)
                else:
                    error = await response.text()
                    logger.error(f"Error in code execution: {error}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error in code execution: {e}")
            return None 