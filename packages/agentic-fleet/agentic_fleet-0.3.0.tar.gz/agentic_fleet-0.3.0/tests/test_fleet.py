"""
Tests for Fleet class
"""

import pytest
from unittest.mock import AsyncMock, patch
from agenticfleet.core import Fleet, Config, LLMConfig, Agent


@pytest.fixture
def fleet_config():
    """Create a test fleet configuration"""
    return Config(
        project_id="test_project",
        azure_deployment="test_deployment",
        default_llm_config=LLMConfig(),
    )


@pytest.fixture
def fleet(fleet_config):
    """Create a test fleet"""
    return Fleet(fleet_config)


def test_fleet_initialization(fleet_config):
    """Test fleet initialization"""
    fleet = Fleet(fleet_config)
    assert fleet.config == fleet_config
    assert isinstance(fleet._agents, dict)
    assert len(fleet._agents) == 0


def test_fleet_add_agent(fleet):
    """Test adding agents to fleet"""
    # Add agent
    agent = fleet.add_agent("test_agent", "test role")
    assert isinstance(agent, Agent)
    assert agent.name == "test_agent"
    assert agent.role == "test role"

    # Verify agent is in fleet
    assert "test_agent" in fleet._agents
    assert fleet._agents["test_agent"] == agent


def test_fleet_get_agent(fleet):
    """Test getting agents from fleet"""
    # Add agent
    agent = fleet.add_agent("test_agent", "test role")

    # Get agent
    retrieved = fleet.get_agent("test_agent")
    assert retrieved == agent

    # Get non-existent agent
    assert fleet.get_agent("non_existent") is None


def test_fleet_remove_agent(fleet):
    """Test removing agents from fleet"""
    # Add agent
    fleet.add_agent("test_agent", "test role")

    # Remove agent
    fleet.remove_agent("test_agent")
    assert "test_agent" not in fleet._agents

    # Remove non-existent agent (should not raise)
    fleet.remove_agent("non_existent")


def test_fleet_list_agents(fleet):
    """Test listing agents in fleet"""
    # Add agents
    fleet.add_agent("agent1", "role1")
    fleet.add_agent("agent2", "role2")

    # List agents
    agents = fleet.list_agents()
    assert isinstance(agents, list)
    assert "agent1" in agents
    assert "agent2" in agents
    assert len(agents) == 2


@pytest.mark.asyncio
async def test_fleet_broadcast(fleet):
    """Test broadcasting messages to agents"""
    # Add agents with mocked receive method
    agent1 = fleet.add_agent("agent1", "role1")
    agent2 = fleet.add_agent("agent2", "role2")
    agent3 = fleet.add_agent("agent3", "role3")

    # Mock receive methods
    agent1.receive = AsyncMock(return_value="response1")
    agent2.receive = AsyncMock(return_value="response2")
    agent3.receive = AsyncMock(return_value="response3")

    # Broadcast message
    responses = await fleet.broadcast(
        "test message",
        sender="agent1",
        exclude=["agent3"]
    )

    # Verify responses
    assert "agent2" in responses
    assert responses["agent2"] == "response2"
    assert "agent1" not in responses  # sender excluded
    assert "agent3" not in responses  # explicitly excluded


@pytest.mark.asyncio
async def test_fleet_direct_message(fleet):
    """Test direct messaging between agents"""
    # Add agents
    sender = fleet.add_agent("sender", "sender_role")
    recipient = fleet.add_agent("recipient", "recipient_role")

    # Mock receive method
    recipient.receive = AsyncMock(return_value="response")

    # Send direct message
    response = await fleet.direct_message(
        "test message",
        sender="sender",
        recipient="recipient"
    )

    assert response == "response"
    recipient.receive.assert_called_once()


@pytest.mark.asyncio
async def test_fleet_error_handling(fleet):
    """Test fleet error handling"""
    # Test invalid sender
    with pytest.raises(ValueError) as exc_info:
        await fleet.broadcast("test", "invalid_sender")
    assert "Sender agent 'invalid_sender' not found" in str(exc_info.value)

    # Test invalid recipient
    with pytest.raises(ValueError) as exc_info:
        await fleet.direct_message("test", "sender", "invalid_recipient")
    assert "Recipient agent 'invalid_recipient' not found" in str(exc_info.value)


def test_fleet_agent_configuration(fleet):
    """Test agent configuration in fleet"""
    # Add agent with custom system message and tools
    custom_message = "Custom system message"
    custom_tools = {"tool1": lambda x: x}

    agent = fleet.add_agent(
        "test_agent",
        "test role",
        system_message=custom_message,
        tools=custom_tools
    )

    assert agent._system_message == custom_message
    assert "tool1" in agent.get_tools()
    assert agent.get_tools()["tool1"] == custom_tools["tool1"] 