"""
Azure OpenAI integration for language models and embeddings
"""

import os
import dotenv
from typing import Dict, Any, Optional, List
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam, ChatCompletionAssistantMessageParam
from pydantic import BaseModel, Field
from datetime import datetime

from ..config import get_settings


class AzureConfig(BaseModel):
    """Azure OpenAI configuration"""
    api_key: str = Field(default="")
    endpoint: str = Field(default="")
    deployment: str = Field(default="")
    api_version: str = Field(default="")
    embedding_deployment: str = Field(default="")


class AzureLLMClient:
    """Azure OpenAI client wrapper"""

    def __init__(self, config: Optional[AzureConfig] = None):
        """Initialize Azure OpenAI client

        Args:
            config: Optional Azure configuration. If not provided, uses settings.
        """
        self.settings = get_settings()
        self.config = config or AzureConfig(
            api_key=self.settings.azure_openai_api_key or "",
            endpoint=self.settings.azure_openai_endpoint or "",
            deployment=self.settings.azure_openai_gpt4_deployment or "",
            api_version=self.settings.azure_openai_api_version or "",
            embedding_deployment=self.settings.azure_openai_embedding_deployment or "",
        )
        self._client = self._create_client()

    def _create_client(self) -> AzureOpenAI:
        """Create Azure OpenAI client"""
        # Use environment variables if not provided in config
        api_key = self.config.api_key
        endpoint = self.config.endpoint

        if not isinstance(api_key, str) or not isinstance(endpoint, str):
            # Try using Azure credentials
            credential = DefaultAzureCredential(
                tenant_id=self.settings.azure_tenant_id,
                client_id=self.settings.azure_client_id,
                client_secret=self.settings.azure_client_secret,
            )
            if not isinstance(endpoint, str):
                raise ValueError("Azure endpoint must be a string")
            token = credential.get_token("https://cognitiveservices.azure.com/.default")
            return AzureOpenAI(
                azure_endpoint=endpoint,
                api_version=self.config.api_version,
                api_key=token.token,
            )

        return AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=self.config.api_version,
        )

    def generate(
        self,
        messages: List[ChatCompletionMessageParam],
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
        response = self._client.chat.completions.create(
            model=self.config.deployment,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
        )
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("No content in response")
        return content

    def get_embeddings(
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
            response = self._client.embeddings.create(
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