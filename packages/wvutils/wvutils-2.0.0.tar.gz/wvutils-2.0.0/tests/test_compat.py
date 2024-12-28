import sys
import time
from unittest import mock

import pytest

from wvutils.constants import MAX_SIZE_32


def preferred_clock_win32():
    with mock.patch("sys.platform", "win32"):
        try:
            from wvutils.compat import preferred_clock

            assert (
                preferred_clock is time.perf_counter
            ), f"Expected preferred_clock to be time.perf_counter, but got {preferred_clock}"
        finally:
            if "wvutils.compat" in sys.modules:
                del sys.modules["wvutils.compat"]


def preferred_clock_other():
    with mock.patch("sys.platform", "other"):
        try:
            from wvutils.compat import preferred_clock

            assert (
                preferred_clock is time.time
            ), f"Expected preferred_clock to be time.time, but got {preferred_clock}"
        finally:
            if "wvutils.compat" in sys.modules:
                del sys.modules["wvutils.compat"]


@pytest.mark.parametrize(
    "max_size, expected",
    [
        (MAX_SIZE_32 - 1, False),
        (MAX_SIZE_32, False),
        (MAX_SIZE_32 + 1, True),
    ],
)
def test_is_64_bit(max_size, expected):
    with mock.patch("sys.maxsize", max_size):
        try:
            from wvutils.compat import IS_64_BIT

            assert (
                IS_64_BIT is expected
            ), f"Expected IS_64_BIT for max size {max_size} to be {expected}, but got {IS_64_BIT}"
        finally:
            if "wvutils.compat" in sys.modules:
                del sys.modules["wvutils.compat"]
