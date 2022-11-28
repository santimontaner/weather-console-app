from typing import Optional
from unittest import TestCase, main
import json
import importlib.resources as resources
from pathlib import Path
from datetime import date
from weatherconsoleapp.connectors.requests_factories import RequestsFactory
from weatherconsoleapp.connectors.accuweather_requests import LocationKey, LocationKeyRequest, CurrentWeatherRequest, WeatherForecastRequest
from weatherconsoleapp.domain import Location, Units, Date
from tests import resources as test_resources

class LocationKeyRequestsFactoryMock(RequestsFactory):
    
    def get(self, url: str, params: Optional[dict] = None) -> dict:
        json_str = resources.read_text(test_resources, "location_key_without_details.json")
        return json.loads(json_str)
    
class CurrentWeatherFactoryMock(RequestsFactory):
    
    def get(self, url: str, params: Optional[dict] = None) -> dict:
        json_str = resources.read_text(test_resources, "current_weather_without_details.json")
        return json.loads(json_str)

class WeatherForecastFactoryMock(RequestsFactory):
    
    def get(self, url: str, params: Optional[dict] = None) -> dict:
        json_str = resources.read_text(test_resources, "weather_forecast_in_metric_without_details.json")
        return json.loads(json_str)

class LocationKeyRequestTest(TestCase):
    
    def setUp(self):
        self._requests_factory = LocationKeyRequestsFactoryMock()
    
    def test_get_result(self):
        request = LocationKeyRequest(self._requests_factory, Location("Bilbao", "ES"), "")
        location_key = request.get_result()
        self.assertTupleEqual(location_key, LocationKey(Location("Bilbao","ES"), "309382"))

class CurrentWeatherRequestTest(TestCase):
    
    def setUp(self):
        self._requests_factory = CurrentWeatherFactoryMock()
    
    def test_get_result(self):
        request = CurrentWeatherRequest(self._requests_factory, LocationKey("Bilbao", "309382"), Units.METRIC, "")
        current_weather = request.get_result()
        self.assertEqual(current_weather.date, Date(date(2022, 11,19)))
        self.assertEqual(current_weather.weather_description, "Light rain")

class WeatherForecastRequestTest(TestCase):
    
    def setUp(self):
        self._requests_factory = WeatherForecastFactoryMock()
    
    def test_get_result(self):
        request = WeatherForecastRequest(self._requests_factory, LocationKey("Bilbao", "309382"), Units.METRIC, 5,  "")
        weather_forecast = request.get_result()
        self.assertEqual(len(weather_forecast), 5)

if __name__ == "__main__":
    main()
