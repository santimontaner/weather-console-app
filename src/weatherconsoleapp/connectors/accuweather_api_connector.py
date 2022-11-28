from typing import List
from logging import getLogger
from . import WeatherApiConnector
from ..domain import Location, WeatherInfo, Units
from .accuweather_requests import LocationKeyRequest, CurrentWeatherRequest, WeatherForecastRequest
from.requests_factories import BaseRequestsFactory

class AccuWeatherApiConnector(WeatherApiConnector):
    """Connector for the Accuweather API https://developer.accuweather.com/
    """
    def __init__(self, apikey, requests_factory: BaseRequestsFactory):
        self._apikey = apikey
        self._requests_factory = requests_factory

    def get_current_weather_for_location(
        self,
        location: Location,
        unit: Units) -> WeatherInfo:
        location_key = LocationKeyRequest(self._requests_factory, location, self._apikey).get_result()
        return CurrentWeatherRequest(self._requests_factory, location_key, unit, self._apikey).get_result()

    def get_weather_forecast_for_location(
        self,
        location: Location,
        unit: Units,
        days: int = 5) -> List[WeatherInfo]:
        location_key = LocationKeyRequest(self._requests_factory, location, self._apikey).get_result()
        return WeatherForecastRequest(self._requests_factory, location_key, unit, days, self._apikey).get_result()
