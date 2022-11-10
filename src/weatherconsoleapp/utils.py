from typing import List
from .domain import WeatherInfo, Location

class Utils:
    @staticmethod
    def print_weather_forecast(weather_forecast: WeatherInfo):
        print(weather_forecast.date)
        print(f"> Weather: {weather_forecast.weather_description.lower().capitalize()}")
        print(f"> Temperature: {weather_forecast.temperature}")

    @staticmethod
    def print_location(location: Location):
        print(f"{location.city.upper()} ({location.country_code.upper()})")

    @staticmethod
    def parse_location_string(location: str) -> List[str]:
        return location.split(",")

    @staticmethod
    def try_parse_string_to_int(int_string: str):
        try:
            return (True, int(int_string))
        except Exception:
            return (False, None)

