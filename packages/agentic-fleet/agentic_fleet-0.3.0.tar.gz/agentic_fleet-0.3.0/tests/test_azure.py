"""
Tests for Azure OpenAI integration
"""

import os
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from agenticfleet.llm.azure import (
    AzureConfig,
    AzureLLMClient,
    initialize_azure,
    get_azure_client,
)


@pytest.fixture
def azure_config():
    """Create test Azure configuration"""
    return AzureConfig(
        deployment="test-deployment",
        embedding_deployment="test-embedding",
    )


def test_azure_config_validation():
    """Test Azure configuration validation"""
    # Test minimal config
    config = AzureConfig(deployment="test")
    assert config.deployment == "test"
    assert config.api_key is None
    assert config.endpoint is None
    assert config.embedding_deployment is None

    # Test full config
    config = AzureConfig(
        deployment="test",
        api_key="key",
        endpoint="endpoint",
        embedding_deployment="embedding",
    )
    assert config.api_key == "key"
    assert config.endpoint == "endpoint"
    assert config.embedding_deployment == "embedding"


@pytest.mark.asyncio
async def test_azure_client_initialization(azure_config):
    """Test Azure client initialization"""
    with patch("agenticfleet.llm.azure.AzureOpenAI") as mock_azure:
        # Test with explicit credentials
        azure_config.api_key = "test_key"
        azure_config.endpoint = "test_endpoint"
        client = AzureLLMClient(azure_config)

        mock_azure.assert_called_once_with(
            api_key="test_key",
            azure_endpoint="test_endpoint",
            api_version=azure_config.api_version,
        )

        # Test with environment variables
        mock_azure.reset_mock()
        azure_config.api_key = None
        azure_config.endpoint = None
        with patch.dict(os.environ, {
            "AZURE_OPENAI_API_KEY": "env_key",
            "AZURE_OPENAI_ENDPOINT": "env_endpoint",
        }):
            client = AzureLLMClient(azure_config)

        mock_azure.assert_called_once_with(
            api_key="env_key",
            azure_endpoint="env_endpoint",
            api_version=azure_config.api_version,
        )


@pytest.mark.asyncio
async def test_azure_client_generate(azure_config):
    """Test text generation"""
    with patch("agenticfleet.llm.azure.AzureOpenAI") as mock_azure:
        # Setup mock response
        mock_completion = MagicMock()
        mock_completion.choices = [
            MagicMock(message=MagicMock(content="test response"))
        ]
        mock_chat = AsyncMock()
        mock_chat.completions.create = AsyncMock(return_value=mock_completion)
        mock_instance = MagicMock()
        mock_instance.chat = mock_chat
        mock_azure.return_value = mock_instance

        # Create client and generate text
        client = AzureLLMClient(azure_config)
        response = await client.generate(
            messages=[{"role": "user", "content": "test"}],
            temperature=0.5,
            max_tokens=100,
        )

        assert response == "test response"
        mock_chat.completions.create.assert_called_once_with(
            model=azure_config.deployment,
            messages=[{"role": "user", "content": "test"}],
            temperature=0.5,
            max_tokens=100,
            stop=None,
        )


@pytest.mark.asyncio
async def test_azure_client_embeddings(azure_config):
    """Test text embeddings"""
    with patch("agenticfleet.llm.azure.AzureOpenAI") as mock_azure:
        # Setup mock response
        mock_response = MagicMock()
        mock_response.data = [
            MagicMock(embedding=[0.1, 0.2, 0.3]),
            MagicMock(embedding=[0.4, 0.5, 0.6]),
        ]
        mock_embeddings = AsyncMock()
        mock_embeddings.create = AsyncMock(return_value=mock_response)
        mock_instance = MagicMock()
        mock_instance.embeddings = mock_embeddings
        mock_azure.return_value = mock_instance

        # Create client and get embeddings
        client = AzureLLMClient(azure_config)
        embeddings = await client.get_embeddings(
            texts=["text1", "text2"],
            batch_size=2,
        )

        assert len(embeddings) == 2
        assert embeddings[0] == [0.1, 0.2, 0.3]
        assert embeddings[1] == [0.4, 0.5, 0.6]
        mock_embeddings.create.assert_called_once_with(
            model=azure_config.embedding_deployment,
            input=["text1", "text2"],
        )


def test_azure_client_global_instance(azure_config):
    """Test global client instance management"""
    # Test uninitialized client
    with pytest.raises(RuntimeError):
        get_azure_client()

    # Initialize client
    initialize_azure(azure_config)
    client = get_azure_client()
    assert isinstance(client, AzureLLMClient)
    assert client.config == azure_config


@pytest.mark.asyncio
async def test_azure_client_error_handling(azure_config):
    """Test error handling"""
    with patch("agenticfleet.llm.azure.AzureOpenAI") as mock_azure:
        # Setup mock to raise exception
        mock_chat = AsyncMock()
        mock_chat.completions.create = AsyncMock(
            side_effect=Exception("API Error")
        )
        mock_instance = MagicMock()
        mock_instance.chat = mock_chat
        mock_azure.return_value = mock_instance

        # Test generation error
        client = AzureLLMClient(azure_config)
        with pytest.raises(Exception) as exc_info:
            await client.generate([{"role": "user", "content": "test"}])
        assert str(exc_info.value) == "API Error"

        # Test embeddings without deployment
        azure_config.embedding_deployment = None
        with pytest.raises(ValueError) as exc_info:
            await client.get_embeddings(["test"])
        assert "Embedding deployment not configured" in str(exc_info.value) 