from enum import Enum
from typing import NamedTuple, List

class Units(Enum):
    """Enumeration for supported units:
    - METRIC
    - IMPERIAL
    """
    METRIC = 1
    IMPERIAL = 2

class Temperature(NamedTuple):
    """Temperature is an immutable domain value representing a temperature
    value in the given units: Units.Metric (Cº) or Units.Imperial(Fº).
    """
    value: float
    units: Units

    @staticmethod
    def _get_units_string(unit: Units):
        units_strings = {Units.IMPERIAL: "ºF", Units.METRIC: "ºC"}
        return units_strings[unit]

    @staticmethod
    def compute_average(temperatures: List["Temperature"]) -> "Temperature":
        is_empty = len(temperatures) == 0
        some_item_isnot_temperature = any([not isinstance(t, Temperature) for t in temperatures])
        not_all_units_are_equal = len(set([t.units for t in temperatures])) > 1

        if  is_empty or some_item_isnot_temperature or not_all_units_are_equal :
            raise ValueError("temperatures must be a non empty list of Temperature objects of same Units.")

        average_value = sum([t.value for t in temperatures])/len(temperatures)
        return Temperature(average_value, temperatures[0].units)

    def __str__(self):
        return f"{self.value:.2f} {Temperature._get_units_string(self.units)}"
