from typing import NamedTuple
from datetime import date

class Date(NamedTuple):
    """Date is an immutable domain value representing a date.
    """
    date: date

    def __str__(self):
        return self.date.strftime("{%b} {%d}, %Y")
