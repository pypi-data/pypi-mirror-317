"""Core configuration classes."""

import os
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict
from dotenv import load_dotenv
from autogen_agentchat.groupchat import GroupChat, GroupChatManager



# Load environment variables
load_dotenv()

class APIConfig(BaseModel):
    """API configuration."""
    model_config = ConfigDict(extra='allow')
    api_key: str = Field(default_factory=lambda: os.getenv("API_KEY", ""))
    x_api_key: str = Field(default_factory=lambda: os.getenv("API_KEY", ""))  # Using API_KEY as fallback
    x_key_name: str = Field(default_factory=lambda: os.getenv("X_KEY_NAME", "X-API-Key"))

class ServerConfig(BaseModel):
    """Server configuration."""
    model_config = ConfigDict(extra='allow')
    host: str = Field(default_factory=lambda: os.getenv("HOST", "127.0.0.1"))
    port: int = Field(default_factory=lambda: int(os.getenv("PORT", "8000")))
    debug: bool = Field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

class LLMConfig(BaseModel):
    """LLM configuration."""
    model_config = ConfigDict(extra='allow')
    model: str = Field(..., description="Model identifier")
    temperature: float = Field(0.7, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(None, gt=0)
    azure_deployment: Optional[str] = None
    
    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary with AutoGen format."""
        config = {
            "config_list": [{
                "model": self.model,
                "api_type": "azure",
                "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
                "api_key": os.getenv("AZURE_OPENAI_API_KEY", ""),
                "base_url": os.getenv("AZURE_OPENAI_ENDPOINT", ""),
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "top_p": 0.95,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "seed": 42,  # For reproducibility
                "request_timeout": 120,
                "functions": [],  # Will be populated by agent functions
                "tools": []  # Will be populated by agent tools
            }],
            "timeout": 120,
            "cache_seed": 42,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "use_cache": True
        }
        
        return config

class AzureConfig(BaseModel):
    """Azure OpenAI configuration."""
    model_config = ConfigDict(extra='allow')
    api_key: str = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_API_KEY", ""))
    endpoint: str = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_ENDPOINT", ""))
    api_version: str = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"))
    deployment: str = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_GPT4o_MINI_DEPLOYMENT", "gpt-4o-mini"))

def create_default_llm_config() -> LLMConfig:
    """Create a default LLM configuration."""
    return LLMConfig(
        model=os.getenv("AZURE_OPENAI_GPT4o_MINI_DEPLOYMENT", "gpt-4o-mini"),
        temperature=0.7,
        max_tokens=2000
    )

class AgentConfig(BaseModel):
    """Agent configuration."""
    model_config = ConfigDict(extra='allow')
    name: str
    role: str
    llm_config: LLMConfig = Field(default_factory=create_default_llm_config)
    tools: Optional[Dict[str, Any]] = None
    functions: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    description: Optional[str] = None
    
    def set_llm_config(self, llm_config: LLMConfig):
        """Set new LLM configuration"""
        self.llm_config = llm_config
        
    def add_function(self, function: Dict[str, Any]):
        """Add a function to the agent"""
        if self.functions is None:
            self.functions = []
        self.functions.append(function)

class FleetConfig(BaseModel):
    """Fleet configuration with enhanced features."""
    model_config = ConfigDict(extra='allow')
    project_id: str
    llm_config: LLMConfig
    agent_configs: Dict[str, Dict] = Field(default_factory=dict)
    use_azure: bool = True
    max_round: int = Field(default=10, description="Maximum conversation rounds")
    max_group_chat_round: int = Field(default=12, description="Maximum group chat rounds")
    system_message: Optional[str] = None
    
    def create_agent_config(self, name: str, role: str) -> AgentConfig:
        """Create a new agent configuration"""
        return AgentConfig(
            name=name,
            role=role,
            llm_config=self.llm_config,
            description=f"{role} specialized in {name}"
        )

class AgenticFleet:
    """Enhanced fleet management with latest AutoGen features."""
    def __init__(self, config: FleetConfig):
        self.config = config
        self.agents: Dict[str, Agent] = {}
        self.group_chat: Optional[GroupChat] = None
        self.manager: Optional[GroupChatManager] = None
        
    def initialize_group_chat(self, system_message: Optional[str] = None):
        """Initialize group chat with enhanced features"""
        agent_list = list(self.agents.values())
        self.group_chat = GroupChat(
            agents=agent_list,
            messages=[],
            max_round=self.config.max_group_chat_round
        )
        
        self.manager = GroupChatManager(
            groupchat=self.group_chat,
            llm_config=self.config.llm_config.dict(),
            system_message=system_message or "I help manage and coordinate the group chat.",
            is_termination_msg=lambda x: "TERMINATE" in str(x).upper()
        )
        
    def get_status(self) -> Dict[str, Any]:
        """Get fleet status"""
        return {
            "project_id": self.config.project_id,
            "agent_count": len(self.agents),
            "has_group_chat": self.group_chat is not None,
            "has_manager": self.manager is not None,
            "max_round": self.config.max_round,
            "use_azure": self.config.use_azure
        }
