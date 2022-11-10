from enum import Enum
from abc import ABC, abstractmethod
from typing import Tuple, List, Dict
from .connectors import WeatherApiConnector, WeatherConnectorTimeout
from .domain import Location, Units
from . import Utils

class CommandResultStatus(Enum):
    Success = 0
    Error = 1
    Timeout = 2

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
    def validate_arguments(cls, **kwargs) -> Tuple[List[str], Dict]:
        """Validate all the arguments for the command.
        Returns a tuple with 2 items:
        1. A list with the validation error messages (if any).
        2. A dictionary with the correct arguments for the command if the
            input arguments were valid.
        """

    @classmethod
    def validate_units_argument(cls, units: str) -> Tuple[str, Units]:
        trimmed_unit = units.strip()
        if trimmed_unit == cls.METRIC or trimmed_unit == "":
            return (None, Units.METRIC)
        elif trimmed_unit == cls.IMPERIAL:
            return (None, Units.METRIC)
        else:
            return ("Units must be 'metric' (default) or 'imperial'.", None)

    @classmethod
    def validate_location_argument(cls, location: str = None) -> Tuple[str, Location]:        
        substrings = Utils.parse_location_string(location)

        if (len(substrings) != 2 
            or not substrings[1].isupper()
            or substrings[1] != substrings[1].strip()):
            return ("Location argument must have this format: Cityname,COUNTRYCODE.", None)
        else:
            return (None, Location(substrings[0], substrings[1]))

class PrintCurrentWeatherCommand(WeatherCommand):
    def __init__(self,
        connector: WeatherApiConnector,
        location: Location = None,
        units: Units = None):
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
            return CommandResultStatus.Success
        except WeatherConnectorTimeout:
            return CommandResultStatus.Timeout
        except Exception:
            return CommandResultStatus.Error

    @classmethod
    def validate_arguments(cls, location: str = None, units: str = "metric") -> Tuple[List[str], Dict]:
        validations_error_messages = []
        validated_input = {}

        location_validation_message, validated_location = cls.validate_location_argument(location)
        units_validation_message, validated_units = cls.validate_units_argument(units)

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
        location: Location = None,
        units: Units = None,
        days: int = 5):
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
            return CommandResultStatus.Success
        except WeatherConnectorTimeout:
            return CommandResultStatus.Timeout
        except Exception:
            return CommandResultStatus.Error
    
    @classmethod
    def validate_days_argument(cls, days: str):
        is_integer, value = Utils.try_parse_string_to_int(days)

        if not is_integer or value < 1 or value > cls.MAX_NUMBER_OF_DAYS:
            return ("Input 'days' argument must be an integer in the range 1-5.", None)
        else:
            return (None, value)

    @classmethod
    def validate_arguments(cls, location: str = None, units: str = "metric", days: str = "5") -> Tuple[List[str], Dict]:
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
