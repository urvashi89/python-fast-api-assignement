from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query

from src.core.dependencies import get_http_client
from src.weather import service
from src.weather.exceptions import (
    CityNotFoundError,
    WeatherProviderError,
)
from src.weather.schemas import WeatherResponse

router = APIRouter(
    prefix="/weather",
    tags=["Weather"],
)


@router.get(
    "",
    response_model=WeatherResponse,
    summary="Get current weather for a city",
)
async def get_weather(
    http_client: Annotated[httpx.AsyncClient, Depends(get_http_client)],
    city: Annotated[str, Query(min_length=1)],
):
    if not city.strip():
        raise HTTPException(
            status_code=422,
            detail="City cannot be empty",
        )

    try:
        return await service.get_weather(
            http_client,
            city.strip(),
        )

    except CityNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        ) from exc

    except WeatherProviderError as exc:
        raise HTTPException(
            status_code=502,
            detail="Weather provider unavailable",
        ) from exc
