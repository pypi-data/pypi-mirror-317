"""
Configuration management using environment variables
"""

from typing import List, Optional
from pydantic import BaseSettings, AnyHttpUrl, validator
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Azure OpenAI Configuration
    azure_openai_api_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_api_version: str = "2024-02-15-preview"
    azure_openai_gpt4_deployment: str = "gpt-4"
    azure_openai_embedding_deployment: str = "text-embedding-large"

    # Azure Authentication
    azure_tenant_id: Optional[str] = None
    azure_client_id: Optional[str] = None
    azure_client_secret: Optional[str] = None

    # Application Configuration
    app_env: str = "development"
    log_level: str = "INFO"
    debug: bool = False

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    api_timeout: int = 60

    # Rate Limiting
    rate_limit_tokens_per_minute: int = 90000
    rate_limit_requests_per_minute: int = 1000

    # Observability
    enable_prompt_tracking: bool = True
    enable_telemetry: bool = True
    max_prompt_history: int = 1000

    # Security
    api_key_header: str = "X-API-Key"
    api_key: Optional[str] = None
    cors_origins: List[str] = ["http://localhost:3000"]

    # Cache Configuration
    cache_type: str = "memory"
    redis_url: Optional[str] = None

    # Documentation
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string if necessary"""
        if isinstance(v, str):
            return json.loads(v)
        return v

    @validator("cache_type")
    def validate_cache_type(cls, v):
        """Validate cache type"""
        if v not in ["memory", "redis"]:
            raise ValueError("cache_type must be either 'memory' or 'redis'")
        return v

    @validator("app_env")
    def validate_app_env(cls, v):
        """Validate application environment"""
        if v not in ["development", "staging", "production"]:
            raise ValueError("app_env must be one of: development, staging, production")
        return v

    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of: {', '.join(valid_levels)}")
        return v.upper()

    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get global settings instance

    Returns:
        Application settings
    """
    return settings 