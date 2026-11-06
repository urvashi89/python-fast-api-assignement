try:
    from anthropic import APIError, AsyncAnthropic
except ImportError:  # pragma: no cover - handled at runtime when dependency is absent
    APIError = Exception
    AsyncAnthropic = None

from src.summary.config import summary_settings
from src.summary.exceptions import LLMProviderError


async def generate_summary(text: str) -> str:
    api_key = summary_settings.llm_api_key
    if not api_key or AsyncAnthropic is None:
        raise LLMProviderError()

    try:
        async with AsyncAnthropic(api_key=api_key, timeout=30.0) as client:
            response = await client.messages.create(
                model=summary_settings.llm_model,
                max_tokens=250,
                messages=[
                    {
                        "role": "user",
                        "content": (
                            "You are a professional summarization assistant. "
                            "Summarize the input in clear, concise language. "
                            "Preserve important facts and key points. "
                            "Write approximately 3-5 sentences.\n\n"
                            f"{text}"
                        ),
                    }
                ],
            )

        summary = "".join(
            block.text
            for block in getattr(response, "content", [])
            if getattr(block, "type", None) == "text"
        ).strip()

        if not summary:
            raise LLMProviderError()

        return summary

    except APIError as exc:
        raise LLMProviderError() from exc
