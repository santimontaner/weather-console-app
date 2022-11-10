from unittest import TestCase, main
from typing import List
from datetime import date, timedelta
from weatherconsoleapp.connectors import WeatherApiConnector
from weatherconsoleapp.domain import Location, Units, WeatherInfo, Temperature
from weatherconsoleapp.commands import PrintCurrentWeatherCommand, PrintWeatherForecastCommand, CommandResultStatus

class WeatherApiConnectorMock(WeatherApiConnector):

    def __init__(self,
        date: date,
        weather_description: str,
        default_temperature_value: float):
        self._date = date
        self._weather_description = weather_description
        self._default_temperature_value = default_temperature_value

    def get_current_weather_for_location(self, location: Location, units: Units) -> WeatherInfo:
        temperature = Temperature(self._default_temperature_value, units)
        return WeatherInfo(self._date, location, temperature, self._weather_description)

    def get_weather_forecast_for_location(
        self,
        location: Location,
        units: Units,
        days: int = 5) -> List[WeatherInfo]:
        dates = [self._date + timedelta(days=i) for i in range(days)]
        temperature = Temperature(self._default_temperature_value, units)
        return [WeatherInfo(date, location, temperature, self._weather_description) for date in dates]

class BaseWeatherTestCase:

    class BaseWeatherTest(TestCase):

        command_class = None

        def test_given_correct_input_when_validating_data_then_data_is_valid(self):
            location = Location("Bilbao", "ES")
            units = Units.METRIC
            validation_error_message, validated_input = self.command_class.validate_arguments("Bilbao,ES", "metric")
            self.assertEqual(len(validation_error_message), 0)
            self.assertEqual(validated_input[self.command_class.LOCATION], location)
            self.assertEqual(validated_input[self.command_class.UNITS], units)

        def test_given_location_input_with_spaces_when_validating_data_then_one_validation_message_returned(self):
            validation_error_message, _ = self.command_class.validate_arguments("Bilbao, ES", "metric")
            self.assertEqual(len(validation_error_message), 1)

        def test_given_location_input_with_multiple_commas_when_validating_data_then_one_validation_message_returned(self):
            validation_error_message, _ = self.command_class.validate_arguments("Bilbao,ES,", "metric")
            self.assertEqual(len(validation_error_message), 1)

        def test_given_incorrect_units_input_when_validating_data_then_then_one_validation_message_returned(self):
            validation_error_message, _ = self.command_class.validate_arguments("Bilbao,ES", "metricimperial")
            self.assertEqual(len(validation_error_message), 1)
        
class CurrentWeatherCommandTestCase(BaseWeatherTestCase.BaseWeatherTest):

    def setUp(self):
        initial_date = date(2022, 1, 1)
        self._connector = WeatherApiConnectorMock(initial_date, "Sunny", 5)
        self.command_class = PrintCurrentWeatherCommand
            
    def test_given_correct_input_when_command_is_executed_then_result_is_success(self):
        location = Location("Bilbao", "ES")
        units = Units.METRIC
        command = PrintCurrentWeatherCommand(self._connector, location, units)
        result= command.execute()
        self.assertEqual(result, CommandResultStatus.Success)
    
class WeatherForecastCommandTestCase(BaseWeatherTestCase.BaseWeatherTest):

    def setUp(self):
        initial_date = date(2022, 1, 1)
        self._connector = WeatherApiConnectorMock(initial_date, "Sunny", 5)
        self.command_class = PrintWeatherForecastCommand
            
    def test_given_correct_input_when_validating_data_then_data_is_valid(self):
        location = Location("Bilbao", "ES")
        units = Units.METRIC
        days = 3
        validation_error_message, validated_input = self.command_class.validate_arguments("Bilbao,ES", "metric", "3")
        self.assertEqual(len(validation_error_message), 0)
        self.assertEqual(validated_input[self.command_class.LOCATION], location)
        self.assertEqual(validated_input[self.command_class.UNITS], units)
        self.assertEqual(validated_input[self.command_class.DAYS], days)
    
    def test_given_zeros_days_input_when_validating_data_then_one_validation_message_returned(self):        
        validation_error_message, _ = self.command_class.validate_arguments("Bilbao,ES", "metric", "0")
        self.assertEqual(len(validation_error_message), 1)
    
    def test_given_six_days_input_when_validating_data_then_one_validation_message_returned(self):        
        validation_error_message, _ = self.command_class.validate_arguments("Bilbao,ES", "metric", "6")
        self.assertEqual(len(validation_error_message), 1)
    
    def test_given_correct_input_when_command_is_executed_then_result_is_success(self):
        location = Location("Bilbao", "ES")
        units = Units.METRIC
        command = PrintWeatherForecastCommand(self._connector, location, units, days=3)
        result= command.execute()
        self.assertEqual(result, CommandResultStatus.Success)

if __name__ == "__main__":
    main()
