"""
Configuration management for AgenticFleet
"""

from typing import Dict, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class AzureConfig(BaseModel):
    """Azure OpenAI configuration."""
    api_key: str = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_API_KEY", ""))
    api_base: str = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_ENDPOINT", ""))
    api_version: str = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"))
    gpt4_deployment: str = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_GPT4_DEPLOYMENT", "gpt-4"))
    embedding_deployment: str = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-large"))

class RedisConfig(BaseModel):
    """Redis configuration."""
    host: str = Field(default_factory=lambda: os.getenv("REDIS_HOST", "localhost"))
    port: int = Field(default_factory=lambda: int(os.getenv("REDIS_PORT", "6379")))
    password: Optional[str] = Field(default_factory=lambda: os.getenv("REDIS_PASSWORD"))
    db: int = Field(default_factory=lambda: int(os.getenv("REDIS_DB", "0")))

class Settings(BaseModel):
    """Application settings."""
    azure: AzureConfig = Field(default_factory=AzureConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    debug: bool = Field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    environment: str = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False 