"""
Tests for configuration system
"""

import pytest
from pydantic import ValidationError
from agenticfleet.core.config import Config, LLMConfig, AgentConfig, AzureConfig

def test_llm_config_defaults():
    """Test LLMConfig default values"""
    config = LLMConfig()
    assert config.model == "gpt-4"
    assert config.temperature == 0.7
    assert config.max_tokens == 1000
    assert config.stop_sequences == []

def test_llm_config_validation():
    """Test LLMConfig validation"""
    # Test valid temperature
    config = LLMConfig(temperature=0.5)
    assert config.temperature == 0.5

    # Test invalid temperature
    with pytest.raises(ValidationError):
        LLMConfig(temperature=2.5)

    # Test invalid max_tokens
    with pytest.raises(ValidationError):
        LLMConfig(max_tokens=0)

def test_agent_config():
    """Test AgentConfig creation and validation"""
    config = AgentConfig(
        name="test_agent",
        role="test role",
        llm_config=LLMConfig(),
        tools=[],
    )
    assert config.name == "test_agent"
    assert config.role == "test role"
    assert isinstance(config.llm_config, LLMConfig)
    assert config.tools == []

def test_main_config():
    """Test main Config creation and validation"""
    azure_config = AzureConfig(deployment="test_deployment", api_key="test_key", endpoint="test_endpoint", api_version="test_version")
    config = Config(
        project_id="test_project",
        azure_config=azure_config,
        default_llm_config=LLMConfig(),
    )
    assert config.project_id == "test_project"
    assert config.azure_config.deployment == "test_deployment"
    assert config.azure_config.api_key == "test_key"
    assert config.azure_config.endpoint == "test_endpoint"
    assert config.azure_config.api_version == "test_version"
    assert isinstance(config.default_llm_config, LLMConfig)

def test_config_with_agents():
    """Test Config with agent configurations"""
    azure_config = AzureConfig(deployment="test_deployment", api_key="test_key", endpoint="test_endpoint", api_version="test_version")
    agent_config = AgentConfig(
        name="test_agent",
        role="test role",
        llm_config=LLMConfig(),
    )

    config = Config(
        project_id="test_project",
        azure_config=azure_config,
        default_llm_config=LLMConfig(),
        agent_configs={"test_agent": agent_config},
    )

    assert "test_agent" in config.agent_configs
    assert config.agent_configs["test_agent"].name == "test_agent"

def test_config_validation():
    """Test Config validation"""
    azure_config = AzureConfig(deployment="test_deployment", api_key="test_key", endpoint="test_endpoint", api_version="test_version")
    llm_config = LLMConfig()
    agent_config = AgentConfig(name="test_agent", role="test role", llm_config=llm_config)

    # Test missing required field
    with pytest.raises(ValidationError):
        Config(project_id="test_project", azure_config=azure_config, default_llm_config=llm_config)

    # Test invalid project_id
    with pytest.raises(ValidationError):
        Config(project_id="", azure_config=azure_config, default_llm_config=llm_config)

    # Test missing azure_config
    with pytest.raises(ValidationError):
        Config(project_id="test_project", azure_config=AzureConfig(deployment="test_deployment", api_key="test_key", endpoint="test_endpoint", api_version="test_version"), default_llm_config=llm_config)

    # Test missing default_llm_config
    with pytest.raises(ValidationError):
        Config(project_id="test_project", azure_config=azure_config)

    # Test config with all parameters
    config_all_params = Config(project_id="test_project", azure_config=azure_config, default_llm_config=llm_config, agent_configs={"test_agent": agent_config})
    assert config_all_params.project_id == "test_project"
    assert config_all_params.azure_config.deployment == "test_deployment"
    assert config_all_params.azure_config.api_key == "test_key"
    assert config_all_params.azure_config.endpoint == "test_endpoint"
    assert config_all_params.azure_config.api_version == "test_version"
    assert config_all_params.default_llm_config == llm_config
    assert config_all_params.agent_configs == {"test_agent": agent_config}
