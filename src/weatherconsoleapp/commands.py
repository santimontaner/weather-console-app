from enum import Enum
from abc import ABC, abstractmethod
from typing import Tuple, List, Dict, Union, Optional, Any
import logging
from .connectors import WeatherApiConnector, WeatherConnectorTimeout
from .domain import Location, Units
from . import Utils

logger = logging.getLogger(__name__)

class CommandResultStatus(Enum):
    SUCCESS = 0
    ERROR = 1
    TIMEOUT = 2

class WeatherCommand(ABC):

    IMPERIAL = Units.IMPERIAL.name.lower()
    METRIC = Units.METRIC.name.lower()
    UNITS = "units"
    LOCATION = "location"
    DAYS = "days"

    @abstractmethod
    def execute(self):
        """Execute the logic for the command.
        """
    
    @classmethod
    def validate_units_argument(cls, units: str) -> Tuple[str, Union[Units, None]]:
        trimmed_unit = units.strip()
        if trimmed_unit == cls.METRIC:
            return ("", Units.METRIC)
        if trimmed_unit == cls.IMPERIAL:
            return ("", Units.IMPERIAL)
        return ("Units must be 'metric' (default) or 'imperial'.", None)

    @classmethod
    def validate_location_argument(cls, location: str) -> Tuple[str, Union[Location, None]]:
        substrings = Utils.parse_location_string(location)

        if (len(substrings) != 2
            or not substrings[1].isupper()
            or substrings[1] != substrings[1].strip()):
            return ("Location argument must have this format: Cityname,COUNTRYCODE.", None)
        return ("", Location(substrings[0], substrings[1]))

class PrintCurrentWeatherCommand(WeatherCommand):
    def __init__(self,
        connector: WeatherApiConnector,
        location: Optional[Location] = None,
        units: Units = Units.METRIC):
        self._connector = connector
        self._location = location
        self._units = units

    def execute(self):
        try:
            current_weather_info = self._connector.get_current_weather_for_location(
                self._location,
                self._units)
            Utils.print_location(current_weather_info.location)
            Utils.print_weather_forecast(current_weather_info)
            return CommandResultStatus.SUCCESS
        except WeatherConnectorTimeout:
            return CommandResultStatus.Timeout
        except Exception:
            logger.error("Exception raised while executing command", exc_info=True)
            return CommandResultStatus.ERROR

    @classmethod
    def validate_arguments(cls, location: str, units: str) -> Tuple[List[str], Dict[str, Any]]:
        validations_error_messages = []
        validated_input = {}

        location_validation_message, validated_location = cls.validate_location_argument(location)
        units_validation_message, validated_units = super().validate_units_argument(units)

        if not validated_location is None:
            validated_input[cls.LOCATION]  = validated_location
        else:
            validations_error_messages.append(location_validation_message)

        if not validated_units is None:
            validated_input[cls.UNITS] = validated_units
        else:
            validations_error_messages.append(units_validation_message)

        return (validations_error_messages, validated_input)

class PrintWeatherForecastCommand(WeatherCommand):

    MAX_NUMBER_OF_DAYS = 5

    def __init__(self,
        connector: WeatherApiConnector,
        location: Optional[Location] = None,
        units: Optional[Units] = Units.METRIC,
        days: Optional[int] = 5):
        self._connector = connector
        self._location = location
        self._units = units
        self._days = days

    def execute(self):
        try:
            weather_forecast_infos = self._connector.get_weather_forecast_for_location(
                self._location,
                self._units,
                self._days)
            Utils.print_location(self._location)
            for weather_info in weather_forecast_infos:
                Utils.print_weather_forecast(weather_info)
            return CommandResultStatus.SUCCESS
        except WeatherConnectorTimeout:
            return CommandResultStatus.Timeout
        except Exception:
            logger.error("Exception raised while executing command", exc_info=True)
            return CommandResultStatus.ERROR

    @classmethod
    def validate_days_argument(cls, days: str):
        is_integer, value = Utils.try_parse_string_to_int(days)

        if not is_integer or value < 1 or value > cls.MAX_NUMBER_OF_DAYS:
            return ("Input 'days' argument must be an integer in the range 1-5.", None)
        return (None, value)

    @classmethod
    def validate_arguments(cls, location: str, units: str, days: str) -> Tuple[List[str], Dict[str, Any]]:
        validations_error_messages = []
        validated_input = {}

        location_validation_message, validated_location = cls.validate_location_argument(location)
        units_validation_message, validated_units = cls.validate_units_argument(units)
        days_validation_message, validated_days = cls.validate_days_argument(days)

        if validated_location is None:
            validations_error_messages.append(location_validation_message)
        else:
            validated_input[cls.LOCATION]  = validated_location

        if validated_units is None:
            validations_error_messages.append(units_validation_message)
        else:
            validated_input[cls.UNITS] = validated_units

        if validated_days is None:
            validations_error_messages.append(days_validation_message)
        else:
            validated_input[cls.DAYS] = validated_days

        return (validations_error_messages, validated_input)
