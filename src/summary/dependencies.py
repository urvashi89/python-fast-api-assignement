import secrets

from fastapi import Header, HTTPException, status

from src.summary.config import summary_settings


async def verify_api_key(
    x_api_key: str | None = Header(default=None),
) -> None:
    valid_keys = [
        key
        for key in (
            summary_settings.api_key,
            summary_settings.claude_api_key,
            summary_settings.anthropic_api_key,
            summary_settings.openai_api_key,
        )
        if key
    ]

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key missing",
        )

    if not any(secrets.compare_digest(x_api_key, key) for key in valid_keys):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
