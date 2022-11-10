from setuptools import setup, find_packages

setup(name="weatherconsoleapp",
        packages = find_packages("."),
        package_dir = {"" : "."},
        entry_points={
        'console_scripts': [
            'weatherconsoleapp=weatherconsoleapp.main:main'
        ]
    },
        version="1.0.0")