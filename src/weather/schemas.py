from pydantic import BaseModel, Field


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    condition: str
    humidity: int = Field(ge=0, le=100)
