"""Compatibility variables and functions.

This module contains variables and functions that are used to provide
compatibility across different Python versions and operating systems.
"""
from __future__ import annotations

import logging
import sys
import time
from typing import TYPE_CHECKING

from wvutils.constants import MAX_SIZE_32

if TYPE_CHECKING:
    from typing import Final

__all__ = [
    "preferred_clock",
    "IS_64_BIT",
]

logger: logging.Logger = logging.getLogger(__name__)


# Preferred clock, based on which one is more accurate on a given system
if sys.platform == "win32":
    preferred_clock = time.perf_counter
else:
    preferred_clock = time.time


IS_64_BIT: Final[bool] = sys.maxsize > MAX_SIZE_32
