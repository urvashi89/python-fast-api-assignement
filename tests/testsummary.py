import pytest
from httpx import AsyncClient

from src.main import app
from src.summary import client as summary_client
from src.summary.config import summary_settings
from src.summary.dependencies import verify_api_key


@pytest.mark.asyncio
async def test_create_summary(client: AsyncClient, monkeypatch):

    async def fake_summary(text: str):
        return "This is a test summary."

    async def fake_auth():
        return None

    app.dependency_overrides[verify_api_key] = fake_auth

    monkeypatch.setattr(
        summary_client,
        "generate_summary",
        fake_summary,
    )

    response = await client.post(
        "/summary",
        json={"text": "This is a long text to summarize."},
    )

    assert response.status_code == 200
    assert response.json() == {"summary": "This is a test summary."}

    app.dependency_overrides.pop(verify_api_key, None)


@pytest.mark.asyncio
async def test_create_summary_without_api_key_when_unconfigured(client: AsyncClient, monkeypatch):
    original_api_key = summary_settings.api_key
    summary_settings.api_key = None

    async def fake_summary(text: str):
        return "This is a test summary."

    monkeypatch.setattr(
        summary_client,
        "generate_summary",
        fake_summary,
    )

    try:
        response = await client.post(
            "/summary",
            json={"text": "This is a long text to summarize."},
        )

        assert response.status_code == 200
        assert response.json() == {"summary": "This is a test summary."}
    finally:
        summary_settings.api_key = original_api_key


@pytest.mark.asyncio
async def test_create_summary_accepts_claude_key(client: AsyncClient, monkeypatch):
    original_api_key = summary_settings.api_key
    original_claude_key = summary_settings.claude_api_key

    summary_settings.api_key = "app-secret"
    summary_settings.claude_api_key = "claude-secret"

    async def fake_summary(text: str):
        return "This is a test summary."

    monkeypatch.setattr(
        summary_client,
        "generate_summary",
        fake_summary,
    )

    try:
        response = await client.post(
            "/summary",
            json={"text": "This is a long text to summarize."},
            headers={"X-API-Key": "claude-secret"},
        )

        assert response.status_code == 200
        assert response.json() == {"summary": "This is a test summary."}
    finally:
        summary_settings.api_key = original_api_key
        summary_settings.claude_api_key = original_claude_key
