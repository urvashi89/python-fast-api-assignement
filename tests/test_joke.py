import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_joke(client: AsyncClient):

    response = await client.get("/joke")

    assert response.status_code == 200

    data = response.json()

    assert "joke" in data
    assert data["category"] == "programming"
