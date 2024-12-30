"""
Tests for AutoGen integration
"""

import pytest
# TODO: Update to autogen-core and autogen-agentchat when 0.4.0.dev12 is officially released
from autogen import Agent, GroupChat, GroupChatManager
from agenticfleet.core.fleet import Fleet
from agenticfleet.core.config import FleetConfig, LLMConfig
from agenticfleet.agents import CriticAgent, PlannerAgent

@pytest.fixture
def fleet_config():
    """Create test fleet configuration"""
    return FleetConfig(
        project_id="test",
        llm_config=LLMConfig(
            temperature=0.7,
            model="gpt-4o",
            max_tokens=2000
        )
    )

@pytest.mark.asyncio
async def test_group_chat_integration(fleet_config):
    """Test AutoGen GroupChat integration"""
    fleet = Fleet(config=fleet_config)
    
    # Add agents
    planner = PlannerAgent(config=fleet_config.create_agent_config(
        name="planner",
        role="planning specialist"
    ))
    critic = CriticAgent(config=fleet_config.create_agent_config(
        name="critic",
        role="evaluation specialist"
    ))
    
    fleet.add_agent(planner.name, planner.config.role)
    fleet.add_agent(critic.name, critic.config.role)
    
    # Initialize fleet
    assert len(fleet.agents) == 2

@pytest.mark.asyncio
async def test_agent_function_calling(fleet_config):
    """Test AutoGen function calling"""
    critic = CriticAgent(config=fleet_config.create_agent_config(
        name="critic",
        role="evaluation specialist"
    ))
    
    result = await critic.evaluate(
        {"test_data": "example"},
        {"criteria": "accuracy"}
    )
    
    assert isinstance(result, dict)
    assert "response" in result 