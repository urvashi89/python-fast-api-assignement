import httpx

from src.weather import client
from src.weather.constants import WEATHER_CODES
from src.weather.exceptions import (
    CityNotFoundError,
    WeatherProviderError,
)


async def get_weather(
    http_client: httpx.AsyncClient,
    city: str,
) -> dict:

    try:
        geo_data = await client.get_city_coordinates(
            http_client,
            city,
        )

        locations = geo_data.get("results")

        if not locations:
            raise CityNotFoundError()

        location = locations[0]

        weather_data = await client.get_weather_data(
            http_client,
            location["latitude"],
            location["longitude"],
        )

        current = weather_data["current"]

        return {
            "city": location["name"],
            "temperature": current["temperature_2m"],
            "condition": WEATHER_CODES.get(
                current["weather_code"],
                "Unknown",
            ),
            "humidity": current["relative_humidity_2m"],
        }

    except (KeyError, TypeError, ValueError) as exc:
        raise WeatherProviderError() from exc
