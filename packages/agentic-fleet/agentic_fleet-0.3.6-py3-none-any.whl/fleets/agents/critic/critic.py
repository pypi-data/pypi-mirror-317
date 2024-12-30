"""
Critic Agent implementation for evaluation and feedback
"""

from typing import Optional, Dict, Any, List, Union
from ...core import Agent
from ...core.config import AgentConfig
import asyncio


class CriticAgent(Agent):
    """Specialized agent for evaluation and feedback"""

    name = "critic"  # Add explicit name property

    DEFAULT_SYSTEM_MESSAGE = """You are an evaluation specialist focused on providing constructive feedback and analysis.
Your responsibilities include:
1. Evaluating results against objectives
2. Identifying strengths and weaknesses
3. Providing actionable feedback
4. Suggesting improvements
5. Maintaining objective assessment standards

Always provide balanced, constructive feedback with specific examples and recommendations.
When using tools, provide clear reasoning for your evaluations and document your analysis process."""

    def __init__(self, config: AgentConfig):
        super().__init__(config, system_message=self.DEFAULT_SYSTEM_MESSAGE)
        
    async def evaluate(self, result: Dict[str, Any], criteria: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Evaluate results against criteria"""
        # Use the agent's process method from base class
        response = await self.process(f"Evaluate this result: {result} against criteria: {criteria}")
        return {"response": response}
