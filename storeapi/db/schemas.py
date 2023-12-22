from datetime import date, datetime
from typing import List

from pydantic import BaseModel


class WeatherIn(BaseModel):
    """
    Pydantic schema for incoming weather data.
    """
    date: datetime
    temp: float
    temp_fahr: float
    owner_city: int


class Weather(WeatherIn):
    """
    Pydantic schema for displaying weather data.
    """
    id: int

    class Config:
        orm_mode = True


class CityIn(BaseModel):
    """
    Pydantic schema for incoming city data.
    """
    name: str


class City(CityIn):
    """
    Pydantic schema for displaying city data.
    """
    id: int
    weathers: List[Weather] = []

    class Config:
        orm_mode = True


class ForecastIn(BaseModel):
    """
    Pydantic schema for incoming forecast data.
    """
    date: date
    temp_day: float
    temp_fahr_day: float
    owner_city: int


class Forecast(ForecastIn):
    """
    Pydantic schema for displaying forecast data.
    """
    id: int

    class Config:
        orm_mode = True


class HistoryIn(BaseModel):
    """
    Pydantic schema for incoming historical weather data.
    """
    date: datetime
    temp: float
    temp_fahr: float
    owner_city: int


class History(HistoryIn):
    """
    Pydantic schema for displaying historical weather data.
    """
    id: int

    class Config:
        orm_mode = True
