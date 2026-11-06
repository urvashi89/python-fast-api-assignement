import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_weather(client: AsyncClient):

    response = await client.get(
        "/weather",
        params={"city": "Delhi"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["city"] == "Delhi"
    assert data["temperature"] == 25.5
    assert data["condition"] == "Mainly clear"
    assert data["humidity"] == 60


@pytest.mark.asyncio
async def test_weather_missing_city(client: AsyncClient):

    response = await client.get("/weather")

    assert response.status_code == 422
