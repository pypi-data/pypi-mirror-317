"""
Azure OpenAI integration for language models and embeddings
"""

import os
from typing import Dict, Any, Optional, List
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI
from pydantic import BaseModel, Field
from datetime import datetime

from ..config import get_settings


class AzureConfig(BaseModel):
    """Azure OpenAI configuration"""
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    deployment: str
    api_version: str = "2024-02-15-preview"
    embedding_deployment: Optional[str] = None


class AzureLLMClient:
    """Azure OpenAI client wrapper"""

    def __init__(self, config: Optional[AzureConfig] = None):
        """Initialize Azure OpenAI client

        Args:
            config: Optional Azure configuration. If not provided, uses settings.
        """
        self.settings = get_settings()
        self.config = config or AzureConfig(
            api_key=self.settings.azure_openai_api_key,
            endpoint=self.settings.azure_openai_endpoint,
            deployment=self.settings.azure_openai_gpt4_deployment,
            api_version=self.settings.azure_openai_api_version,
            embedding_deployment=self.settings.azure_openai_embedding_deployment,
        )
        self._client = self._create_client()

    def _create_client(self) -> AzureOpenAI:
        """Create Azure OpenAI client"""
        # Use environment variables if not provided in config
        api_key = self.config.api_key
        endpoint = self.config.endpoint

        if not api_key or not endpoint:
            # Try using Azure credentials
            credential = DefaultAzureCredential(
                tenant_id=self.settings.azure_tenant_id,
                client_id=self.settings.azure_client_id,
                client_secret=self.settings.azure_client_secret,
            )
            return AzureOpenAI(
                azure_endpoint=endpoint,
                api_version=self.config.api_version,
                azure_ad_token_provider=credential,
            )

        return AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=self.config.api_version,
        )

    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stop: Optional[List[str]] = None,
    ) -> str:
        """Generate text using Azure OpenAI

        Args:
            messages: List of messages in the conversation
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stop: Optional stop sequences

        Returns:
            Generated text
        """
        response = await self._client.chat.completions.create(
            model=self.config.deployment,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
        )
        return response.choices[0].message.content

    async def get_embeddings(
        self, texts: List[str], batch_size: int = 100
    ) -> List[List[float]]:
        """Get embeddings for texts

        Args:
            texts: List of texts to embed
            batch_size: Batch size for processing

        Returns:
            List of embeddings
        """
        if not self.config.embedding_deployment:
            raise ValueError("Embedding deployment not configured")

        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = await self._client.embeddings.create(
                model=self.config.embedding_deployment,
                input=batch,
            )
            embeddings.extend([data.embedding for data in response.data])
        return embeddings


# Global client instance
_client: Optional[AzureLLMClient] = None


def initialize_azure(config: Optional[AzureConfig] = None) -> None:
    """Initialize global Azure OpenAI client

    Args:
        config: Optional Azure configuration
    """
    global _client
    _client = AzureLLMClient(config)


def get_azure_client() -> AzureLLMClient:
    """Get global Azure OpenAI client

    Returns:
        Azure OpenAI client

    Raises:
        RuntimeError: If client not initialized
    """
    if _client is None:
        raise RuntimeError("Azure OpenAI client not initialized")
    return _client 