import os, sys
from pathlib import Path
from setuptools import setup, find_packages

setup(name="weatherconsoleapp",
        packages = find_packages("."),
        package_dir = {"" : "src"},
        entry_points={
        'console_scripts': [
            'weatherconsoleapp=weatherconsoleapp.main:main'
        ]
    },
        version="1.0.0")

app_directory = ".weatherconsoleapp"

try:
    user_directory = os.path.expanduser("~")
    user_app_directory = Path(user_directory, app_directory)
    if not os.path.isdir(user_app_directory):
        os.mkdir(user_app_directory)
except:
    print("Could not create 'weatherconsoleapp' directory.", file=sys.stderr)
