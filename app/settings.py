import pathlib

from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict

PREFIX = "GENTA_AI_AGENT_"


# Determine which .env file to load
def get_env_file() -> pathlib.Path:
    """Determine which .env file to load based on environment."""
    # Check if we're running locally (not in Docker)
    env_file = ".env"
    print(f"Loading environment variables from {env_file}...")
    print(pathlib.Path(__file__).parent.parent / env_file)

    return pathlib.Path(__file__).parent.parent / env_file


DOTENV = get_env_file()


class BaseSettings(PydanticBaseSettings):
    """Base settings."""

    model_config = SettingsConfigDict(
        env_file=str(DOTENV), env_file_encoding="utf-8", extra="ignore"
    )


class OpenAISettings(BaseSettings):
    """Configuration for OpenAI."""

    # OpenAI API configuration
    api_key: str = ""
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4000

    model_config = SettingsConfigDict(env_file=str(DOTENV), env_prefix=f"{PREFIX}OPENAI_")


class DataForSEOSettings(BaseSettings):
    """Configuration for DataForSEO."""

    # DataForSEO API configuration
    client_id: str = ""
    client_secret: str = ""
    base_url: str = "https://api.dataforseo.com"
    timeout: int = 30

    model_config = SettingsConfigDict(env_file=str(DOTENV), env_prefix=f"{PREFIX}DATAFORSEO_")


class Settings(BaseSettings):
    """Main settings for the Genta AI Agent application."""
    env: str = "local"
    host: str = "localhost"
    port: int = 8000
    workers: int = 1
    log_level: str = "info"
    reload: bool = False
    
    # OpenAI Configuration
    openai: OpenAISettings = OpenAISettings()
    
    # DataForSEO Configuration
    dataforseo: DataForSEOSettings = DataForSEOSettings()
    
    # MCP Server Configuration
    mcp_server_url: str = "http://localhost:3001"
    
    # CORS settings
    cors_origins: list[str] = ["http://localhost:3000", "https://genta-assessment.vercel.app"]

    model_config = SettingsConfigDict(
        env_file=str(DOTENV),
        env_file_encoding="utf-8",
    )


settings = Settings()
