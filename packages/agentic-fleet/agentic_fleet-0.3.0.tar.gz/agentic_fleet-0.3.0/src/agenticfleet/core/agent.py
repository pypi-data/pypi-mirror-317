"""
Base Agent implementation for AgenticFleet
"""

from typing import Optional, Dict, Any, List
from autogen_agentchat import Agent as AutoGenAgent
from .config import AgentConfig, LLMConfig


class Agent:
    """Base agent class that wraps AutoGen functionality"""

    def __init__(
        self,
        config: AgentConfig,
        *,
        system_message: Optional[str] = None,
        tools: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the agent with configuration

        Args:
            config: Agent configuration
            system_message: Optional system message override
            tools: Optional tools override
        """
        self.config = config
        self._system_message = system_message or self._default_system_message()
        self._tools = tools or config.tools or {}
        self._agent: Optional[AutoGenAgent] = None

    def _default_system_message(self) -> str:
        """Generate default system message based on role"""
        return f"You are {self.config.name}, a {self.config.role}."

    @property
    def name(self) -> str:
        """Get agent name"""
        return self.config.name

    @property
    def role(self) -> str:
        """Get agent role"""
        return self.config.role

    @property
    def llm_config(self) -> LLMConfig:
        """Get LLM configuration"""
        return self.config.llm_config

    def get_tools(self) -> Dict[str, Any]:
        """Get available tools"""
        return self._tools

    def add_tool(self, name: str, tool: Any) -> None:
        """Add a new tool

        Args:
            name: Tool name
            tool: Tool implementation
        """
        self._tools[name] = tool

    def remove_tool(self, name: str) -> None:
        """Remove a tool by name

        Args:
            name: Tool name to remove
        """
        self._tools.pop(name, None)

    def _create_agent(self) -> AutoGenAgent:
        """Create AutoGen agent instance"""
        return AutoGenAgent(
            name=self.name,
            system_message=self._system_message,
            llm_config=self.llm_config.dict(),
            tools=list(self._tools.values()),
        )

    def initialize(self) -> None:
        """Initialize the agent"""
        if self._agent is None:
            self._agent = self._create_agent()

    async def send(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Send a message to the agent

        Args:
            message: Input message
            context: Optional context information

        Returns:
            Agent's response
        """
        self.initialize()
        response = await self._agent.send(message, context or {})
        return response

    async def receive(self, message: str, sender: "Agent") -> str:
        """Receive a message from another agent

        Args:
            message: Input message
            sender: Sending agent

        Returns:
            Agent's response
        """
        self.initialize()
        return await self._agent.receive(message, sender._agent) 