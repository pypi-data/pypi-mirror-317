"""
Tests for base Agent class
"""

from unittest.mock import AsyncMock, patch, MagicMock
import pytest
from agenticfleet.core import Agent, AgentConfig, LLMConfig
from agenticfleet.core.exceptions import AgentError, MessageError

@pytest.fixture
def default_config():
    """Create a default test configuration"""
    llm_config = LLMConfig()
    agent_configs = {
        "executor": AgentConfig(name="executor", role="Executor agent.", llm_config=llm_config),
        "planner": AgentConfig(name="planner", role="Planner agent.", llm_config=llm_config),
    }
    return MagicMock(agent_configs=agent_configs, default_llm_config=llm_config)

def test_agent_creation(default_config):
    """Test basic agent creation"""
    agent = Agent(config=default_config.agent_configs["executor"])
    assert agent.config.name == "executor"
    assert agent.config.role == "Executor agent."
    assert agent.config.llm_config == default_config.default_llm_config

def test_agent_system_message(default_config):
    """Test agent system message"""
    agent = Agent(config=default_config.agent_configs["executor"])
    assert agent.system_message == "Executor agent."

async def test_agent_process(default_config):
    """Test agent message processing"""
    agent = Agent(config=default_config.agent_configs["executor"])
    with patch.object(agent.agent, 'send', new_callable=AsyncMock) as mock_send:
        mock_send.return_value = MagicMock(content="Test response")
        response = await agent.process("Hello")
        assert response == "Test response"

async def test_agent_receive(default_config):
    """Test agent receiving messages"""
    agent1 = Agent(config=default_config.agent_configs["executor"])
    agent2 = Agent(config=default_config.agent_configs["planner"])
    
    # Mock the generate_response method instead of receive
    with patch.object(agent1.agent, 'generate_response', new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = MagicMock(content="Test response")
        response = await agent1.receive("Hello", agent2)
        assert response == "Test response"
        mock_generate.assert_called_once()

async def test_agent_cleanup(default_config):
    """Test agent cleanup method"""
    agent = Agent(config=default_config.agent_configs["executor"])
    await agent.cleanup()
    assert not agent.state.is_active

async def test_agent_session(default_config):
    """Test agent session context manager"""
    agent = Agent(config=default_config.agent_configs["executor"])
    async with agent.session():
        assert agent.state.is_active
    assert not agent.state.is_active

def test_agent_direct_message(default_config):
    """Test direct message sending via AutoGen agent"""
    agent = Agent(config=default_config.agent_configs["executor"])
    mock_recipient = MagicMock()
    with patch.object(agent.agent, 'send', new_callable=AsyncMock) as mock_send:
        agent.agent.send(message="Test message", recipient=mock_recipient)
        mock_send.assert_called_once_with(message="Test message", recipient=mock_recipient)

def test_agent_update_system_message(default_config):
    """Test updating the agent's system message"""
    agent = Agent(config=default_config.agent_configs["executor"])
    new_message = "Updated system message."
    agent.agent.update_system_message(new_message)
    assert agent.agent.system_message == new_message

async def test_agent_initiate_chat(default_config):
    """Test initiating a chat with another agent"""
    agent1 = Agent(config=default_config.agent_configs["executor"])
    agent2 = Agent(config=default_config.agent_configs["planner"])
    with patch.object(agent1.agent, 'initiate_chat', new_callable=AsyncMock) as mock_initiate_chat:
        await agent1.agent.initiate_chat(recipient=agent2.agent, message="Start chat")
    mock_initiate_chat.assert_called_once_with(agent2.agent, message="Start chat")

async def test_agent_reset(default_config):
    """Test resetting the AutoGen agent"""
    agent = Agent(config=default_config.agent_configs["executor"])
    with patch.object(agent.agent, 'reset', new_callable=AsyncMock) as mock_reset:
        await agent.agent.reset()
    mock_reset.assert_called_once()

async def test_agent_serialization(default_config):
    """Test agent state serialization"""
    agent = Agent(config=default_config.agent_configs["executor"])
    assert agent.serialize() is not None

async def test_agent_load_serialization(default_config):
    """Test loading agent from serialized state"""
    agent = Agent(config=default_config.agent_configs["executor"])
    serialized = agent.serialize()
    loaded_agent = Agent.load(serialized)
    assert loaded_agent.config.name == agent.config.name

def test_agent_add_tool(default_config):
    """Test adding a tool to the agent"""
    agent = Agent(config=default_config.agent_configs["executor"])
    
    def dummy_tool(arg1):
        return f"Tool called with {arg1}"
    
    agent.tools.add_tool("test_tool", dummy_tool)
    assert "test_tool" in agent.tools.get_tools()
    assert agent.tools.get_tools()["test_tool"]("test_arg") == "Tool called with test_arg"

def test_agent_remove_tool(default_config):
    """Test removing a tool from the agent"""
    agent = Agent(config=default_config.agent_configs["executor"])
    agent.tools.remove_tool("test_tool")
    assert "test_tool" not in agent.tools.get_tools()

def test_agent_toggle_activity(default_config):
    """Test toggling the agent's active state"""
    agent = Agent(config=default_config.agent_configs["executor"])
    agent.state.toggle_active()
    assert not agent.state.is_active
    agent.state.toggle_active()
    assert agent.state.is_active

def test_set_llm_config(default_config):
    """Test setting a new LLM config for the agent"""
    agent = Agent(config=default_config.agent_configs["executor"])
    new_llm_config = LLMConfig(temperature=0.9)
    agent.config.set_llm_config(new_llm_config)
    assert agent.config.llm_config.temperature == 0.9

def test_agent_initialization_failure():
    """Test agent initialization failure"""
    with pytest.raises(AgentError):
        Agent(config=MagicMock())  # Simulate a failure scenario

async def test_agent_message_processing_failure(default_config):
    """Test failure during message processing"""
    agent = Agent(config=default_config.agent_configs["executor"])
    with patch.object(agent.agent, 'send', side_effect=Exception("Test error")) as mock_send:
        with pytest.raises(MessageError):
            await agent.process("Test message")
    mock_send.assert_called_once_with("Test message", {})
