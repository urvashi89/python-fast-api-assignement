from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SummaryConfig(BaseSettings):
    api_key: str = "change-this-development-key"
    claude_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "CLAUDE_API_KEY",
            "claude_api_key",
            "ANTHROPIC_API_KEY",
            "anthropic_api_key",
            "OPENAI_API_KEY",
            "openai_api_key",
        ),
    )
    anthropic_api_key: str | None = None
    openai_api_key: str | None = None
    claude_model: str = "claude-3-5-sonnet-20241022"
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    openai_model: str = "gpt-4.1-mini"
    max_text_length: int = 10000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    @property
    def llm_api_key(self) -> str | None:
        return (
            self.claude_api_key
            or self.anthropic_api_key
            or self.openai_api_key
        )

    @property
    def llm_model(self) -> str:
        return self.claude_model or self.anthropic_model or self.openai_model


summary_settings = SummaryConfig()
