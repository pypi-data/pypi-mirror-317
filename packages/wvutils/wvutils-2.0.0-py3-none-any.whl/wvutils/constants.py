"""Constant values.

This module contains constants that are used throughout the package.
"""
from __future__ import annotations

from string import (
    ascii_lowercase,
    ascii_uppercase,
    digits,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final

__all__ = [
    "DEFAULT_SAFECHARS_ALLOWED_CHARS",
    "MAX_SIZE_32",
]

DEFAULT_SAFECHARS_ALLOWED_CHARS: frozenset[str] = frozenset("-_" + ascii_lowercase + ascii_uppercase + digits)

MAX_SIZE_32: Final[int] = 2**32
