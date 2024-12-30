"""Core agent functionality."""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any, Callable, Dict, List, Optional, Protocol, Union
from pydantic import BaseModel, Field

from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import BaseTool 
from autogen_agentchat.oai import OpenAIWrapper

from .config import AgentConfig
from .exceptions import AgentError, MessageError

logger = logging.getLogger(__name__)

class AgentLike(Protocol):
    """Protocol for agent-like objects"""
    name: str
    agent: Optional[AssistantAgent]
    config: Optional[AgentConfig]

class AgentState(BaseModel):
    """Agent state model"""
    name: str
    role: str
    is_active: bool = True
    message_count: int = 0
    last_error: Optional[str] = None
    functions: List[str] = []

    def toggle_active(self):
        """Toggle the active state"""
        self.is_active = not self.is_active

class Agent:
    """Base agent class with enhanced features"""
    name: str
    agent: AssistantAgent
    config: AgentConfig

    def __init__(
        self, 
        config: AgentConfig, 
        system_message: Optional[str] = None, 
        tools: Optional[Dict[str, Callable]] = None,
        functions: Optional[List[Dict[str, Any]]] = None
    ):
        """Initialize the agent with configuration"""
        try:
            self.config = config
            self.name = config.name
            self.system_message = system_message or config.role
            self.tools = tools or {}
            self.functions = functions or []
            
            self.state = AgentState(
                name=config.name,
                role=config.role,
                functions=[fn["name"] for fn in self.functions] if self.functions else []
            )
            
            # Updated AutoGen agent initialization with latest features
            self.agent = AssistantAgent(
                name=config.name,
                system_message=self.system_message,
                model_client=OpenAIWrapper(**config.llm_config.dict()),
                function_map=self.tools,
                human_input_mode="NEVER",
                max_consecutive_auto_reply=3,
                code_execution_config={"use_docker": False},
                is_termination_msg=lambda x: "TERMINATE" in str(x).upper(),
                description=f"{config.role} specialized in {config.name}"
            )
            
            # Register functions if provided
            if self.functions:
                for function in self.functions:
                    register_function(self.agent, function)
            
            # Register default message handlers
            self._register_default_handlers()
            
            logger.info(f"Agent {config.name} initialized successfully with {len(self.functions)} functions")
            
        except Exception as e:
            logger.error(f"Failed to initialize agent {config.name}: {str(e)}")
            raise AgentError(f"Agent initialization failed: {str(e)}")
            
    def _register_default_handlers(self):
        """Register default message handlers"""
        try:
            # Register error handler
            self.agent.register_reply(
                trigger=lambda x: "error" in str(x).lower(),
                reply_func=self._handle_error
            )
            
            # Register termination handler
            self.agent.register_reply(
                trigger=lambda x: "terminate" in str(x).lower(),
                reply_func=self._handle_termination
            )
            
        except Exception as e:
            logger.error(f"Failed to register handlers: {str(e)}")
            
    async def _handle_error(self, message: str, sender: Optional[ConversableAgent] = None) -> str:
        """Handle error messages"""
        error_msg = f"Error encountered: {message}"
        self.state.last_error = error_msg
        logger.error(error_msg)
        return "Error handled and logged"
        
    async def _handle_termination(self, message: str, sender: Optional[ConversableAgent] = None) -> str:
        """Handle termination messages"""
        logger.info(f"Termination requested for {self.name}")
        await self.cleanup()
        return "Agent terminated"

    @asynccontextmanager
    async def session(self):
        """Context manager for agent sessions"""
        try:
            yield self
        finally:
            await self.cleanup()

    async def process(self, message: str) -> str:
        """Process a message and return a response"""
        if not self.state.is_active:
            raise AgentError("Agent is not active")
            
        try:
            logger.debug(f"Processing message for {self.config.name}: {message[:100]}...")
            
            # Updated to use AutoGen's new chat completion interface
            response = await asyncio.to_thread(
                self.agent.generate_reply,
                messages=[{
                    "role": "user",
                    "content": message
                }],
                sender=None
            )
            
            self.state.message_count += 1
            return str(response) if response is not None else ""
            
        except Exception as e:
            self.state.last_error = str(e)
            logger.error(f"Message processing failed for {self.config.name}: {str(e)}")
            raise MessageError(f"Failed to process message: {str(e)}")
    
    async def receive(self, message: str, sender: 'Agent') -> str:
        """Receive a message from another agent"""
        try:
            logger.info(f"Received message from {sender.name} to {self.name}")
            
            response = await asyncio.to_thread(
                self.agent.generate_reply,
                messages=[{
                    "role": "user", 
                    "content": f"Message from {sender.name}: {message}"
                }],
                sender=sender.agent
            )
            return str(response) if response is not None else ""
            
        except Exception as e:
            logger.error(f"Message handling failed: {str(e)}")
            raise MessageError(f"Failed to handle message: {str(e)}")

    async def cleanup(self):
        """Cleanup agent resources"""
        try:
            self.state.is_active = False
            # Reset conversation if needed
            if hasattr(self.agent, 'reset'):
                self.agent.reset()
            logger.info(f"Agent {self.config.name} cleaned up successfully")
            
        except Exception as e:
            logger.error(f"Cleanup failed for {self.config.name}: {str(e)}")
            raise AgentError(f"Cleanup failed: {str(e)}")
            
    def __repr__(self) -> str:
        return f"Agent(name={self.config.name}, role={self.config.role}, active={self.state.is_active})"

    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the agent."""
        return {
            "name": self.name,
            "role": self.config.role,
            "is_active": self.state.is_active,
            "message_count": self.state.message_count,
            "last_error": self.state.last_error,
            "functions": self.state.functions
        }
        
    async def reset(self):
        """Reset the agent's state."""
        self.state = AgentState(
            name=self.config.name,
            role=self.config.role,
            functions=[fn["name"] for fn in self.functions] if self.functions else []
        )
        if hasattr(self.agent, 'reset'):
            self.agent.reset()
        logger.info(f"Agent {self.name} reset successfully")

    def serialize(self) -> Dict[str, Any]:
        """Serialize agent state"""
        return {
            "name": self.name,
            "config": self.config.dict(),
            "state": self.state.dict(),
            "functions": self.functions
        }

    @classmethod
    def load(cls, data: Dict[str, Any]) -> 'Agent':
        """Load agent from serialized state"""
        config = AgentConfig(**data["config"])
        agent = cls(config=config)
        agent.state = AgentState(**data["state"])
        return agent
