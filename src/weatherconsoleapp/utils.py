from typing import List
from .domain import WeatherInfo, Location

class Utils:
    @staticmethod
    def print_weather_forecast(weather_forecast: WeatherInfo):
        formatted_weather = weather_forecast.weather_description.lower().capitalize()
        weather_description = Utils.ensure_string_ends_with_dot(formatted_weather)
        print(weather_forecast.date)
        print(f"> Weather: {weather_description}")
        print(f"> Temperature: {weather_forecast.temperature}")

    @staticmethod
    def ensure_string_ends_with_dot(string: str):
        if(len(string) > 0 and string[-1] != '.'):
            return f"{string}."
        return string

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

