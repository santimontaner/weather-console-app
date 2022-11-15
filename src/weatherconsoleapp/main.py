import logging
import argparse
from weatherconsoleapp.connectors import AccuWeatherApiConnector
from weatherconsoleapp.commands import PrintCurrentWeatherCommand, PrintWeatherForecastCommand, CommandResultStatus

logging.basicConfig(
    filename='weatherconsoleapp.log',
    filemode='a',
    format="%(asctime)s - %(message)s",
    encoding='utf-8',
    level=logging.DEBUG)

def print_command_result_status(command_result_status: CommandResultStatus):
    if command_result_status == CommandResultStatus.Error:
        print("An unexpected error happened.")
    elif command_result_status == CommandResultStatus.Timeout:
        print("Request timedout while requesting weather information.")

def execute_command(command_builder, apikey, validation_error_messages, validated_input):
    if len(validation_error_messages) > 0:
        for message in validation_error_messages:
            print(message)
        return
    else:
        connector = AccuWeatherApiConnector(apikey)
        command = command_builder(connector, **validated_input)
        result_status = command.execute()
        print_command_result_status(result_status)

def try_execute_print_current_weather(apikey: str, location: str, units: str):
    validation_error_messages, validated_input = PrintCurrentWeatherCommand.validate_arguments(location, units)
    execute_command(PrintCurrentWeatherCommand, apikey, validation_error_messages, validated_input)

def try_execute_print_weather_forecast(apikey: str, location: str, units: str, days: str):
    validation_error_messages, validated_input = PrintWeatherForecastCommand.validate_arguments(location, units, days)
    execute_command(PrintWeatherForecastCommand, apikey, validation_error_messages, validated_input)    

CURRENT_WEATHER_COMMAND = "current"
WEATHER_FORECAST_COMMAND = "forecast"

def main():
    parser = argparse.ArgumentParser(
                    prog = "WeatherConsoleApp",
                    description = "A simple console application for worldwide weather forecasts.",
                    epilog = 'Text at the bottom of help')
    parser.add_argument("command")
    parser.add_argument("location")
    parser.add_argument("--units", default="metric")
    parser.add_argument("--days", default="5")
    args = parser.parse_args()

    if args.command == CURRENT_WEATHER_COMMAND:
        try_execute_print_current_weather(apikey, args.location, args.units)
    elif args.command == WEATHER_FORECAST_COMMAND:
        try_execute_print_weather_forecast(apikey, args.location, args.units, args.days)
    else:
        print(f"Invalid option: {args.command}")

if __name__ == "__main__":
    main()
