import secrets

from fastapi import Header, HTTPException, status

from src.summary.config import summary_settings


async def verify_api_key(
    x_api_key: str | None = Header(default=None),
) -> None:

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key missing",
        )

    if not secrets.compare_digest(
        x_api_key,
        summary_settings.api_key,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
