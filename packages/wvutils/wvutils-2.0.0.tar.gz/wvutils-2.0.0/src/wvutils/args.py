"""Utilities for parsing arguments from the command line.

This module provides utilities for parsing arguments from the command line.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from wvutils.constants import DEFAULT_SAFECHARS_ALLOWED_CHARS

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

__all__ = [
    "integer_string",
    "nonempty_string",
    "safechars_string",
]

logger: logging.Logger = logging.getLogger(__name__)


def nonempty_string(name: str) -> Callable[[str], str]:
    """Return a function that ensures a string is not empty.

    Args:
        name (str): Name of the function.

    Returns:
        Callable[[str], str]: Decorated function.
    """

    def func(text: str):
        text = text.strip()
        if not text:
            raise ValueError("Must not be empty")
        return text

    func.__name__ = name
    return func


def integer_string(name: str, min_value: int | None = None, max_value: int | None = None) -> Callable[[str], int]:
    """Return a function that ensures a string can be converted to an integer.

    Args:
        name (str): Name of the function.
        min_value (int | None, optional): Minimum value for the integer. Defaults to None.
        max_value (int | None, optional): Maximum value for the integer. Defaults to None.

    Returns:
        Callable[[str], int]: Decorated function.
    """

    def func(text: str):
        text = text.strip()
        try:
            value = int(text)
        except ValueError:
            raise ValueError("Must be an integer")
        if min_value is not None and value < min_value:
            raise ValueError(f"Must be at least {min_value}")
        if max_value is not None and value > max_value:
            raise ValueError(f"Must be at most {max_value}")
        return value

    func.__name__ = name
    return func


def safechars_string(name: str, allowed_chars: Iterable[str] | None = None) -> Callable[[str], str]:
    """Return a function that ensures a string consists of allowed characters.

    Args:
        name (str): Name of the function.
        allowed_chars (Iterable[str] | None, optional): Custom characters used to validate the function name. Defaults to None.

    Returns:
        Callable[[str], str]: Decorated function.

    Raises:
        ValueError: If empty collection of allowed characters is provided.
    """
    if allowed_chars is None:
        allowed_chars = DEFAULT_SAFECHARS_ALLOWED_CHARS
    else:
        allowed_chars = frozenset(allowed_chars)

    if len(allowed_chars) == 0:
        raise ValueError("Must provide at least one character")

    def func(text):
        text = text.strip()
        for char in text:
            if char not in allowed_chars:
                raise ValueError("Must consist of characters ['" + "', '".join(allowed_chars) + "']")
        return text

    func.__name__ = name
    return func
