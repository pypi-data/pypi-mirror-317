"""
Custom exceptions for the agent system
"""

class AgenticFleetError(Exception):
    """Base exception for all agent-related errors"""
    pass

class AgentError(AgenticFleetError):
    """Exception raised for errors in agent operations"""
    pass

class MessageError(AgenticFleetError):
    """Exception raised for errors in message handling"""
    pass

class ConfigError(AgenticFleetError):
    """Exception raised for configuration errors"""
    pass

class LLMError(AgenticFleetError):
    """Exception raised for LLM-related errors"""
    pass

class FleetError(AgenticFleetError):
    """Exception raised for fleet management errors"""
    pass 