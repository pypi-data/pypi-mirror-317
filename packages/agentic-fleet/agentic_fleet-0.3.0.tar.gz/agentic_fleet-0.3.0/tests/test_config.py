"""
Tests for configuration system
"""

import pytest
from pydantic import ValidationError
from agenticfleet.core.config import Config, LLMConfig, AgentConfig


def test_llm_config_defaults():
    """Test LLMConfig default values"""
    config = LLMConfig()
    assert config.model == "gpt-4"
    assert config.temperature == 0.7
    assert config.max_tokens == 1000
    assert config.stop_sequences is None


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
    )
    assert config.name == "test_agent"
    assert config.role == "test role"
    assert isinstance(config.llm_config, LLMConfig)
    assert config.tools is None


def test_main_config():
    """Test main Config creation and validation"""
    config = Config(
        project_id="test_project",
        azure_deployment="test_deployment",
        default_llm_config=LLMConfig(),
    )
    assert config.project_id == "test_project"
    assert config.azure_deployment == "test_deployment"
    assert isinstance(config.default_llm_config, LLMConfig)
    assert isinstance(config.agent_configs, dict)


def test_config_with_agents():
    """Test Config with agent configurations"""
    agent_config = AgentConfig(
        name="test_agent",
        role="test role",
        llm_config=LLMConfig(),
    )

    config = Config(
        project_id="test_project",
        default_llm_config=LLMConfig(),
        agent_configs={"test_agent": agent_config},
    )

    assert "test_agent" in config.agent_configs
    assert config.agent_configs["test_agent"].name == "test_agent"


def test_config_validation():
    """Test Config validation"""
    # Test missing required field
    with pytest.raises(ValidationError):
        Config()

    # Test invalid project_id
    with pytest.raises(ValidationError):
        Config(project_id="", default_llm_config=LLMConfig()) 