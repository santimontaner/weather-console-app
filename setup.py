import os, sys
from pathlib import Path
from setuptools import setup, find_packages

setup(name="weatherconsoleapp",
        packages = find_packages("src"),
        package_dir = {"" : "src"},
        package_data={'weatherconsoleapp': ['config.ini']},
        entry_points={
        'console_scripts': [
            'weatherconsoleapp=weatherconsoleapp.main:main'
        ]
    },
        version="1.0.0")
