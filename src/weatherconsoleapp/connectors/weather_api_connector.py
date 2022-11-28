from abc import ABC, abstractmethod
from typing import List
from ..domain import Location, WeatherInfo, Units

class WeatherApiConnector(ABC):
    """Base weather APIs connector. Specific connector implementations should inherit from this class.
    """
    @abstractmethod
    def get_current_weather_for_location(self, location: Location, unit: Units) -> WeatherInfo:
        """Retrieves the current weather for a given location.
        """

    @abstractmethod
    def get_weather_forecast_for_location(
        self,
        location: Location,
        unit: Units,
        days: int = 5) -> List[WeatherInfo]:
        """Retrieves the 5 days weather forecast for a given location.
        """
