import httpx
import pytest_asyncio
from httpx import ASGITransport, AsyncClient, MockTransport

from src.core.dependencies import get_http_client
from src.main import app


@pytest_asyncio.fixture
async def client():

    def mock_external_api(request: httpx.Request):

        if "geocoding-api.open-meteo.com" in str(request.url):
            return httpx.Response(
                200,
                json={
                    "results": [
                        {
                            "name": "Delhi",
                            "latitude": 28.65,
                            "longitude": 77.23,
                        }
                    ]
                },
            )

        if "api.open-meteo.com" in str(request.url):
            return httpx.Response(
                200,
                json={
                    "current": {
                        "temperature_2m": 25.5,
                        "relative_humidity_2m": 60,
                        "weather_code": 1,
                    }
                },
            )

        if "official-joke-api.appspot.com" in str(request.url):
            return httpx.Response(
                200,
                json={
                    "setup": "Why do programmers prefer dark mode?",
                    "punchline": "Because light attracts bugs.",
                    "type": "programming",
                },
            )

        return httpx.Response(404)

    mock_http_client = httpx.AsyncClient(transport=MockTransport(mock_external_api))

    app.dependency_overrides[get_http_client] = lambda: mock_http_client

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    await mock_http_client.aclose()
