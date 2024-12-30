"""
Core Fleet implementation for managing agents
"""

from typing import Dict, List, Optional, Any
from .config import Config
from .agent import Agent
from .exceptions import FleetError

class Fleet:
    """Manages a fleet of specialized agents."""

    def __init__(self, config: Config):
        """Initialize the fleet with configuration.
        
        Args:
            config: Fleet configuration
            
        Raises:
            FleetError: If initialization fails
        """
        try:
            self.config = config
            self.agents: Dict[str, Agent] = {}
            
        except Exception as e:
            raise FleetError(f"Fleet initialization failed: {str(e)}")

    async def process_message(self, message: str) -> str:
        """Process a message using the fleet's primary agent.
        
        Args:
            message: Message to process
            
        Returns:
            Response from the primary agent
            
        Raises:
            FleetError: If no agents or processing fails
        """
        try:
            if not self.agents:
                raise FleetError("No agents available in fleet")
                
            # Use first agent as primary for now
            primary_agent = next(iter(self.agents.values()))
            return await primary_agent.process(message)
            
        except Exception as e:
            raise FleetError(f"Message processing failed: {str(e)}")

    def add_agent(self, name: str, role: str, system_message: Optional[str] = None) -> None:
        """Add an agent to the fleet.
        
        Args:
            name: Agent name
            role: Agent role
            system_message: Optional system message
            
        Raises:
            FleetError: If agent creation fails
        """
        try:
            agent_config = self.config.create_agent_config(
                name=name,
                role=role
            )
            
            self.agents[name] = Agent(
                config=agent_config,
                system_message=system_message
            )
            
        except Exception as e:
            raise FleetError(f"Failed to add agent {name}: {str(e)}")

    def list_agents(self) -> List[str]:
        """List all agent names in the fleet.
        
        Returns:
            List of agent names
        """
        return list(self.agents.keys())

    async def broadcast(
        self,
        message: str,
        sender: str,
        exclude: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """Broadcast a message to all agents except excluded ones.
        
        Args:
            message: Message to broadcast
            sender: Sender name
            exclude: Optional list of agents to exclude
            
        Returns:
            Dictionary of agent responses
            
        Raises:
            FleetError: If broadcast fails
        """
        try:
            exclude = exclude or []
            sender_agent = self.agents.get(sender)
            if not sender_agent:
                raise FleetError(f"Sender agent {sender} not found")
                
            responses = {}
            for name, agent in self.agents.items():
                if name not in exclude and name != sender:
                    responses[name] = await agent.receive(message, sender_agent)
                    
            return responses
            
        except Exception as e:
            raise FleetError(f"Broadcast failed: {str(e)}")

    async def direct_message(
        self,
        message: str,
        sender: str,
        recipient: str
    ) -> str:
        """Send a direct message between agents.
        
        Args:
            message: Message content
            sender: Sender name
            recipient: Recipient name
            
        Returns:
            Recipient's response
            
        Raises:
            FleetError: If message delivery fails
        """
        try:
            sender_agent = self.agents.get(sender)
            recipient_agent = self.agents.get(recipient)
            
            if not sender_agent:
                raise FleetError(f"Sender agent {sender} not found")
            if not recipient_agent:
                raise FleetError(f"Recipient agent {recipient} not found")
                
            return await recipient_agent.receive(message, sender_agent)
            
        except Exception as e:
            raise FleetError(f"Direct message failed: {str(e)}")

    async def cleanup(self):
        """Cleanup all agents in the fleet."""
        for agent in self.agents.values():
            await agent.cleanup() 