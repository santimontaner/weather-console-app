from typing import NamedTuple
from datetime import date
from . import Temperature, Location

class WeatherInfo(NamedTuple):
    """Weather is an immutable domain value representing a weather temperature ad
    description.
    """
    date: date
    location: Location
    temperature: Temperature
    weather_description: str

