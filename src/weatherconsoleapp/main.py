import logging
import argparse
import os
import sys
import pathlib
import shutil
import configparser
import importlib.resources as resources
from weatherconsoleapp.connectors import AccuWeatherApiConnector
from weatherconsoleapp.commands import PrintCurrentWeatherCommand, PrintWeatherForecastCommand, CommandResultStatus
import weatherconsoleapp

CONFIG_FILENAME = "config.ini"
CURRENT_WEATHER_COMMAND = "current"
WEATHER_FORECAST_COMMAND = "forecast"

logger = logging.getLogger(__name__)

def config_logging():
    logging.basicConfig(
        filename=pathlib.Path(get_config_dirname(), 'weatherconsoleapp.log'),
        filemode='a',
        format="%(name)s: %(asctime)s - %(message)s",
        encoding='utf-8',
        level=logging.DEBUG)   

def get_config_dirname():
    app_directory = ".weatherconsoleapp"
    user_directory = os.path.expanduser("~")
    return pathlib.Path(user_directory, app_directory)

def get_config_filepath():
    return pathlib.Path(get_config_dirname(), CONFIG_FILENAME)

def create_config_dir() -> bool:
    """Returns True if the config dir did not exist and was created.
    """
    try:
        config_dir = get_config_dirname()
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)
            return True
    except:
        print("Could not create 'weatherconsoleapp' directory.", file=sys.stderr)
    return False

def create_config_file() -> bool:
    """Returns True if the config file did not exist and was created.
    """
    with resources.as_file(resources.files(weatherconsoleapp).joinpath(CONFIG_FILENAME)) as config_file:
        target_path = get_config_filepath()
        if not os.path.isfile(target_path):
            shutil.copy(config_file, target_path)
            return True
    return False

def create_config() -> bool:
    """Returns True if any of the config dir or file were created.
    """
    return create_config_dir() or create_config_file()

def get_api_key():
    try:
        config = configparser.ConfigParser()
        config.read(get_config_filepath())
        apikey = config['accuweather']['apikey']
        return apikey
    except Exception:
        logger.error("Could not find an apikey for Accuweather", exc_info=True)
        return None

def print_command_result_status(command_result_status: CommandResultStatus):
    if command_result_status == CommandResultStatus.ERROR:
        print(f"An unexpected error happened. Please check whether the configured apikey is valid ({get_config_filepath()}).")
    elif command_result_status == CommandResultStatus.TIMEOUT:
        print("Request timedout while requesting weather information.")

def execute_command(command_builder, apikey, validation_error_messages, validated_input):
    if len(validation_error_messages) > 0:
        for message in validation_error_messages:
            print(message)
        return

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

def main():
    if create_config():
        print(f"Please configure your Accuweather apikey in the {get_config_filepath()} file.")
        return
    config_logging()

    parser = argparse.ArgumentParser(
                    prog = "WeatherConsoleApp",
                    description = "A simple console application for worldwide weather forecasts. More info and examples at github.com/santimontaner/weather-console-app.",                    
                    epilog = 'Text at the bottom of help')
    parser.add_argument("command", help="Possible values are : 'current' and 'forecast'.")
    parser.add_argument("location", help="Location for the requested weather information. Format must be City,COUNTRYCODE. Example: Paris,FR.")
    parser.add_argument("--units", default="metric", help="Options are 'metric' (default) and 'imperial'.")
    parser.add_argument("--days", default="5", help="Number of days for the forecast. Maximum is 5 (default).")
    args = parser.parse_args()

    apikey = get_api_key()
    if apikey is None:
        print(f"Please set a valid apikey in {get_config_filepath()}.")
        return

    if args.command == CURRENT_WEATHER_COMMAND:
        try_execute_print_current_weather(apikey, args.location, args.units)
    elif args.command == WEATHER_FORECAST_COMMAND:
        try_execute_print_weather_forecast(apikey, args.location, args.units, args.days)
    else:
        print(f"{args.command} is not a valid option")

if __name__ == "__main__":
    main()
