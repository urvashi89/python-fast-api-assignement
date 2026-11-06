import httpx

from src.joke.constants import JOKE_API_URL
from src.joke.exceptions import JokeProviderError


async def fetch_random_joke(
    client: httpx.AsyncClient,
) -> dict:

    try:
        response = await client.get(JOKE_API_URL)
        response.raise_for_status()

        return response.json()

    except (httpx.HTTPError, ValueError) as exc:
        raise JokeProviderError() from exc
