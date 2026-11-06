from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from src.core.config import settings
from src.joke.router import router as joke_router
from src.summary.router import router as summary_router
from src.weather.router import router as weather_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(timeout=httpx.Timeout(10.0))

    yield

    await app.state.http_client.aclose()


app = FastAPI(
    title=settings.app_name,
    description="Weather, Joke and LLM Summary Microservice",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(weather_router)
app.include_router(joke_router)
app.include_router(summary_router)


@app.get("/", tags=["Health check"])
async def health_check():
    return {"status": "healthy"}
