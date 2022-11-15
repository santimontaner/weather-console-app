from typing import NamedTuple
from . import Temperature, Location, Date

class WeatherInfo(NamedTuple):
    """Weather is an immutable domain value representing a weather temperature ad
    description.
    """
    date: Date
    location: Location
    temperature: Temperature
    weather_description: str
