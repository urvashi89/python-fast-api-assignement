from src.summary import client
from src.summary.config import summary_settings
from src.summary.exceptions import (
    InvalidSummaryInputError,
)


async def create_summary(text: str) -> dict:

    if not text.strip():
        raise InvalidSummaryInputError("Text cannot be empty")

    if len(text) > summary_settings.max_text_length:
        raise InvalidSummaryInputError("Text exceeds maximum allowed length")

    summary = await client.generate_summary(text)

    return {"summary": summary}
