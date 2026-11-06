from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException

from src.core.dependencies import get_http_client
from src.joke import service
from src.joke.exceptions import JokeProviderError
from src.joke.schemas import JokeResponse

router = APIRouter(
    prefix="/joke",
    tags=["Joke"],
)

 
@router.get(
    "",
    response_model=JokeResponse,
    summary="Get a random joke",
)
async def get_joke(
    http_client: Annotated[httpx.AsyncClient, Depends(get_http_client)],
):
    try:
        return await service.get_random_joke(http_client)

    except JokeProviderError as exc:
        raise HTTPException(
            status_code=502,
            detail="Joke provider unavailable",
        ) from exc
