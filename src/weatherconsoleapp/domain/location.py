from typing import NamedTuple

class Location(NamedTuple):
    """Location is an immutable domain value representing a city of a given country.
    """
    city: str
    country_code: str

    def __str__(self):
        return f"{str.capitalize(self.city)}, ({self.country_code})"
