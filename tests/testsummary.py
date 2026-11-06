import pytest
from httpx import AsyncClient

from src.main import app
from src.summary import client as summary_client
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
