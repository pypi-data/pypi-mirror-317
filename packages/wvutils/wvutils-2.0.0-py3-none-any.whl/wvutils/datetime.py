"""Datetime utilities.

This module contains functions and classes that are used to work with datetimes.
"""

from calendar import monthrange
from enum import Enum

__all__ = [
    "ALL_DATETIME_FORMATS",
    "DatetimeFormat",
    "num_days_in_month",
]


class DatetimeFormat(str, Enum):
    TWITTER = "%a %b %d %H:%M:%S %z %Y"
    REDDIT = "%b %d %Y %I:%M %p"
    ISO_8601 = "%Y-%m-%dT%H:%M:%S%z"
    DATABASE = "%Y-%m-%d %H:%M:%S"
    DATE = "%Y-%m-%d"
    TIME_12H = "%I:%M %p %Z"
    TIME_24H = "%H:%M %Z"


ALL_DATETIME_FORMATS: list[DatetimeFormat] = [
    DatetimeFormat.TWITTER,
    DatetimeFormat.REDDIT,
    DatetimeFormat.ISO_8601,
    DatetimeFormat.DATABASE,
    DatetimeFormat.DATE,
    DatetimeFormat.TIME_12H,
    DatetimeFormat.TIME_24H,
]


def num_days_in_month(year: int, month: int) -> int:
    """Determine the number of days in a month.

    Args:
        year (int): Year to check.
        month (int): Month to check.

    Returns:
        int: Number of days in the month.
    """
    return monthrange(year, month)[1]
