from pydantic import BaseModel, Field


class JokeResponse(BaseModel):
    joke: str = Field(min_length=1)
    category: str = Field(min_length=1)
