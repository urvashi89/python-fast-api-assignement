import httpx

from src.weather.constants import (
    GEOCODING_URL,
    WEATHER_URL,
)
from src.weather.exceptions import WeatherProviderError


async def get_city_coordinates(
    client: httpx.AsyncClient,
    city: str,
) -> dict:

    try:
        response = await client.get(
            GEOCODING_URL,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json",
            },
        )

        response.raise_for_status()
        return response.json()

    except (httpx.HTTPError, ValueError) as exc:
        raise WeatherProviderError() from exc


async def get_weather_data(
    client: httpx.AsyncClient,
    latitude: float,
    longitude: float,
) -> dict:

    try:
        response = await client.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": ("temperature_2m,relative_humidity_2m,weather_code"),
                "timezone": "auto",
            },
        )

        response.raise_for_status()
        return response.json()

    except (httpx.HTTPError, ValueError) as exc:
        raise WeatherProviderError() from exc
