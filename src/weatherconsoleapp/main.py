import logging
import argparse
import os, pathlib
import configparser
from weatherconsoleapp.connectors import AccuWeatherApiConnector
from weatherconsoleapp.commands import PrintCurrentWeatherCommand, PrintWeatherForecastCommand, CommandResultStatus

def get_config_dir():
    app_directory = ".weatherconsoleapp"
    user_directory = os.path.expanduser("~")    
    return pathlib.Path(user_directory, app_directory)    

logging.basicConfig(
    filename=pathlib.Path(get_config_dir(), 'weatherconsoleapp.log'),
    filemode='a',
    format="%(name)s: %(asctime)s - %(message)s",
    encoding='utf-8',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)

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

def get_api_key():
    try:
        config_dir = get_config_dir()        
        config_file_name = "config.ini"
        config_file_path = pathlib.Path(config_dir, config_file_name)    
        config = configparser.ConfigParser()
        config.read(config_file_path)
        apikey = config['Accuweather']['apikey']
        return apikey
    except Exception:
        logger.error("Could not find an apikey for Accuweather", exc_info=True)
        return None

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

    apikey = get_api_key()
    if apikey is None:
        print("Please set a valid apikey in Accuweather.apikey field from ~/.weatherconsoleapp/config.ini file.")

    if args.command == CURRENT_WEATHER_COMMAND:
        try_execute_print_current_weather(apikey, args.location, args.units)
    elif args.command == WEATHER_FORECAST_COMMAND:
        try_execute_print_weather_forecast(apikey, args.location, args.units, args.days)
    else:
        print(f"Invalid option: {args.command}")

if __name__ == "__main__":
    main()
