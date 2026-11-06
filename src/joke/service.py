import httpx

from src.joke import client
from src.joke.exceptions import JokeProviderError


async def get_random_joke(
    http_client: httpx.AsyncClient,
) -> dict:

    try:
        data = await client.fetch_random_joke(http_client)

        setup = data["setup"]
        punchline = data["punchline"]
        category = data["type"]

        return {
            "joke": f"{setup} {punchline}",
            "category": category,
        }

    except (KeyError, TypeError, ValueError) as exc:
        raise JokeProviderError() from exc
