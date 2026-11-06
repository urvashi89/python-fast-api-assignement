
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SummaryConfig(BaseSettings):
    # Optional key to protect your FastAPI endpoint
    api_key: str | None = None

    # Claude credentials
    claude_api_key: str | None = None

    # Claude model
    claude_model: str = "claude-3-5-sonnet-20241022"

    # Input validation
    max_text_length: int = 10000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


summary_settings = SummaryConfig()
