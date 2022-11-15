# Python weather console app
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/santimontaner/weather-console-app/tree/develop.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/santimontaner/weather-console-app/tree/develop)

## Install
To install this CLI applicaton follow these steps:
1. Install the requirements:
```bash
pip install -r requirements.txt
```
2. Run this command from your favourite command line.
```bash
> python setup.py install
```

## Configuration

When the application is installed, a `.weatherconsoleapp` folder is created in your user folder (the `~/` folder in Linux, the `C:\Users\SantiMontaner` folder in Windows 10). Inside there should be a *config.ini* file
with this information:
```
[accuweather]
apikey=XXXXX
```
where `XXXXX` is a valid Accuweather API key. You can obtain an Accuweather API key by registering in the Accuweather developers [website](https://developer.accuweather.com/).

## Using

### Current weather
Returns current weather at the specified location (format must be **City,COUNTRYCODE** with the specified units (**metric** or **imperial**, default is **metric**).

When executing this command:
```
> weatherconsoleapp current Teruel,ES --units=metric
```
The output in the console is:
```
TERUEL (ES)
Nov 15, 2022
> Weather: Mostly cloudy.
> Temperature: 10.80 ºC
```

### Weather forecast
Returns the weather for next 5 days starting from current date. Accepts optional **units** and **days** (between 1 and 5) arguments.

When executing this command:
```
> weatherconsoleapp forecast Clermont-Ferrand,FR --units=imperial --days=3
```
The output in the console is:
```
CLERMONT-FERRAND (FR)
Nov 15, 2022
> Weather: Mostly cloudy w/ showers.
> Temperature: 11.50 ºC
Nov 16, 2022
> Weather: Intermittent clouds.
> Temperature: 9.85 ºC
Nov 17, 2022
> Weather: Showers.
> Temperature: 8.65 ºC
```