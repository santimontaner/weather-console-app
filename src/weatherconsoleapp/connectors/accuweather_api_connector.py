from abc import ABC, abstractmethod
from typing import List, Dict
from collections import namedtuple
from logging import getLogger
from datetime import datetime
import requests
from . import WeatherApiConnector
from . import WeatherConnectorTimeout
from ..domain import Location, WeatherInfo, Units, Temperature, Date

logger = getLogger(__name__)

class Request(ABC):
    api_url = "http://dataservice.accuweather.com"
    api_version = 1

    def make_request(self) -> dict:
        response = self._get_response_with_log()
        return response.json()

    @abstractmethod
    def _get_url(self) -> str:
        pass

    def _get_params(self) -> Dict[str, str]:
        return {}

    def _get_response_with_log(self):
        try:
            response = requests.get(self._get_url(), params= self._get_params())
        except requests.exceptions.Timeout:
            raise WeatherConnectorTimeout("AccuweatheConnector timed out.")
        logger.info("Response status code: %s %s", response.status_code, response.reason)
        return response

    @staticmethod
    def _convert_unit_to_key(unit: Units) -> str:
        return unit.name.lower().capitalize()

    @staticmethod
    def parse_datetime_string(datetime_string):
        return datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S%z").date()

class LocationKey(namedtuple('LocationKey', 'location key_code')):
    __slots__ = ()
    def __new__(cls, location: Location, key_code: str):
        return super(LocationKey, cls).__new__(cls, location, key_code)

class LocationKeyRequest(Request):
    request_url = "locations/v1/cities"

    def __init__(self, location: Location, apikey: str):
        self._location = location
        self._apikey = apikey

    def get_result(self) -> LocationKey:
        logger.info("Sending LocationKeyRequest: %s %s.", self._location.city, self._location.country_code)
        response = self.make_request()
        return self._get_location_key_from_response_json(response)

    def _get_url(self) -> str:
        return f"{self.api_url}/{self.request_url}/{self._location.country_code}/search"

    def _get_params(self):
        return {"apikey" : self._apikey, "q": self._location.city }

    def _get_location_key_from_response_json(self, response: dict) -> LocationKey:
        return LocationKey(self._location, response[0]["Key"])

class CurrentWeatherRequest(Request):
    request_url = "currentconditions/v1"

    def __init__(self, location_key: LocationKey, units: Units, apikey: str):
        self._location_key = location_key
        self._units = units
        self._apikey = apikey

    def get_result(self) -> WeatherInfo:
        logger.info("Sending CurrentWeatherRequest: %s %s.", self._location_key, self._units.name)
        response = self.make_request()
        return self._get_weather_from_response_json(response)

    def _get_url(self) -> str:
        return f"{self.api_url}/{self.request_url}/{self._location_key.key_code}"

    def _get_params(self):
        return {"apikey" : self._apikey, "details" : False}

    def _get_weather_from_response_json(self, response: dict) -> WeatherInfo:
        data = response[0]
        date = Date(self.parse_datetime_string(data["LocalObservationDateTime"]))
        weather_description = data["WeatherText"]
        unit_str = Request._convert_unit_to_key(self._units)
        temperature_value = data["Temperature"][unit_str]["Value"]
        temperature = Temperature(temperature_value, self._units)
        location = self._location_key.location
        return WeatherInfo(date, location, temperature, weather_description)

class WeatherForecastRequest(Request):
    request_url = "forecasts/v1/daily/5day"

    def __init__(self, location_key: LocationKey, units: Units, days: int, apikey: str):
        self._location_key = location_key
        self._apikey = apikey
        self._units = units
        self._days = days

    def get_result(self) -> List[WeatherInfo]:
        logger.info("Sending WeatherForecastRequest: %s %s %s.", self._location_key, self._units.name, self._days)
        response = self.make_request()
        return self._get_weather_from_response_json(response)

    def _get_url(self) -> str:
        return f"{self.api_url}/{self.request_url}/{self._location_key.key_code}"

    def _get_params(self):
        params = {"apikey" : self._apikey, "details" : False}
        if self._units == Units.METRIC:
            params["metric"] = "true"
        return params

    def _get_weather_from_response_json(self, response: dict) -> List[WeatherInfo]:
        daily_forecasts = response["DailyForecasts"]
        indices =  range(self._days)
        filtered_forecasts = [daily_forecasts[i] for i in indices]
        return [self._parse_raw_forecast(f) for f in filtered_forecasts]

    def _parse_raw_forecast(self, raw_forecast) -> WeatherInfo:
        date = Date(self.parse_datetime_string(raw_forecast["Date"]))
        weather_description = raw_forecast["Day"]["IconPhrase"]
        min_temperature_value = raw_forecast["Temperature"]["Minimum"]["Value"]
        max_temperature_value = raw_forecast["Temperature"]["Maximum"]["Value"]
        min_temperature = Temperature(min_temperature_value, self._units)
        max_temperature = Temperature(max_temperature_value, self._units)
        average_temperature = Temperature.compute_average([min_temperature, max_temperature])
        location = self._location_key.location
        return WeatherInfo(date, location, average_temperature, weather_description)

class AccuWeatherApiConnector(WeatherApiConnector):
    """Connector for the Accuweather API https://developer.accuweather.com/
    """
    def __init__(self, apikey):
        self._apikey = apikey

    def get_current_weather_for_location(
        self,
        location: Location,
        unit: Units) -> WeatherInfo:
        location_key = LocationKeyRequest(location, self._apikey).get_result()
        return CurrentWeatherRequest(location_key, unit, self._apikey).get_result()

    def get_weather_forecast_for_location(
        self,
        location: Location,
        unit: Units,
        days: int = 5) -> List[WeatherInfo]:
        location_key = LocationKeyRequest(location, self._apikey).get_result()
        return WeatherForecastRequest(location_key, unit, days, self._apikey).get_result()
