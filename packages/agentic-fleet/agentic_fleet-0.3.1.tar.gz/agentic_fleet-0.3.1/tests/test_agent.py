"""
Tests for base Agent class
"""

import pytest
from unittest.mock import AsyncMock, patch
from agenticfleet.core import Agent, AgentConfig, LLMConfig


@pytest.fixture
def agent_config():
    """Create a test agent configuration"""
    return AgentConfig(
        name="test_agent",
        role="test role",
        llm_config=LLMConfig(),
    )


@pytest.fixture
def agent(agent_config):
    """Create a test agent"""
    return Agent(agent_config)


def test_agent_initialization(agent_config):
    """Test agent initialization"""
    agent = Agent(agent_config)
    assert agent.name == "test_agent"
    assert agent.role == "test role"
    assert isinstance(agent.llm_config, LLMConfig)


def test_agent_custom_system_message(agent_config):
    """Test agent with custom system message"""
    custom_message = "Custom system message"
    agent = Agent(agent_config, system_message=custom_message)
    assert agent._system_message == custom_message


def test_agent_default_system_message(agent):
    """Test agent default system message"""
    expected = f"You are {agent.name}, a {agent.role}."
    assert agent._default_system_message() == expected


def test_agent_tool_management(agent):
    """Test agent tool management"""
    # Test adding a tool
    test_tool = lambda x: x
    agent.add_tool("test_tool", test_tool)
    assert "test_tool" in agent.get_tools()
    assert agent.get_tools()["test_tool"] == test_tool

    # Test removing a tool
    agent.remove_tool("test_tool")
    assert "test_tool" not in agent.get_tools()


@pytest.mark.asyncio
async def test_agent_send_message(agent):
    """Test agent send message"""
    with patch("agenticfleet.core.agent.AutoGenAgent") as mock_autogen:
        # Setup mock
        mock_instance = AsyncMock()
        mock_instance.send.return_value = "test response"
        mock_autogen.return_value = mock_instance

        # Initialize agent
        agent.initialize()

        # Test send
        response = await agent.send("test message")
        assert response == "test response"
        mock_instance.send.assert_called_once_with("test message", {})


@pytest.mark.asyncio
async def test_agent_receive_message(agent):
    """Test agent receive message"""
    with patch("agenticfleet.core.agent.AutoGenAgent") as mock_autogen:
        # Setup mocks
        mock_instance = AsyncMock()
        mock_instance.receive.return_value = "test response"
        mock_autogen.return_value = mock_instance

        # Create sender agent
        sender_config = AgentConfig(
            name="sender",
            role="sender role",
            llm_config=LLMConfig(),
        )
        sender = Agent(sender_config)
        sender._agent = AsyncMock()

        # Initialize agent
        agent.initialize()

        # Test receive
        response = await agent.receive("test message", sender)
        assert response == "test response"
        mock_instance.receive.assert_called_once_with("test message", sender._agent)


def test_agent_initialization_lazy(agent_config):
    """Test agent lazy initialization"""
    agent = Agent(agent_config)
    assert agent._agent is None

    # Initialize
    agent.initialize()
    assert agent._agent is not None


@pytest.mark.asyncio
async def test_agent_error_handling(agent):
    """Test agent error handling"""
    with patch("agenticfleet.core.agent.AutoGenAgent") as mock_autogen:
        # Setup mock to raise an exception
        mock_instance = AsyncMock()
        mock_instance.send.side_effect = Exception("Test error")
        mock_autogen.return_value = mock_instance

        # Initialize agent
        agent.initialize()

        # Test error handling
        with pytest.raises(Exception) as exc_info:
            await agent.send("test message")
        assert str(exc_info.value) == "Test error" 