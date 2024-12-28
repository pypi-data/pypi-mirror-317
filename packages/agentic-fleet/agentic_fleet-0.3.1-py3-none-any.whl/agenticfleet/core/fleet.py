"""
Core Fleet implementation for managing agents
"""

from typing import Dict, List, Optional, Any
from .config import Settings
from ..agents.planner import PlannerAgent
from ..agents.executor import ExecutorAgent
from ..agents.critic import CriticAgent
from ..agents.researcher import ResearchAgent

class Fleet:
    """Manages a fleet of specialized agents."""

    def __init__(self, settings: Settings):
        """Initialize the fleet with settings."""
        self.settings = settings
        self.agents: Dict[str, Any] = {}
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize the specialized agents."""
        self.agents["planner"] = PlannerAgent(self.settings)
        self.agents["executor"] = ExecutorAgent(self.settings)
        self.agents["critic"] = CriticAgent(self.settings)
        self.agents["researcher"] = ResearchAgent(self.settings)

    async def process_message(self, content: str) -> str:
        """Process a message through the agent fleet.
        
        Args:
            content: The message content to process
            
        Returns:
            The processed response
        """
        try:
            # Route message to appropriate agent(s)
            if any(kw in content.lower() for kw in ["research", "find", "search", "analyze"]):
                response = await self.agents["researcher"].process(content)
            elif any(kw in content.lower() for kw in ["plan", "organize", "structure"]):
                response = await self.agents["planner"].process(content)
            elif any(kw in content.lower() for kw in ["execute", "run", "implement"]):
                response = await self.agents["executor"].process(content)
            elif any(kw in content.lower() for kw in ["evaluate", "review", "assess"]):
                response = await self.agents["critic"].process(content)
            else:
                # Default to researcher for general queries
                response = await self.agents["researcher"].process(content)
            
            return response
        except Exception as e:
            return f"Error processing message: {str(e)}" 