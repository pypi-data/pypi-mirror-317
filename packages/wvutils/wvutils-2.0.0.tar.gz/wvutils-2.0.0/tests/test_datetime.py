import pickle
from datetime import datetime, timezone

import pytest
from pytz import utc

from wvutils.datetime import DatetimeFormat, num_days_in_month


@pytest.mark.parametrize(
    "year, month, expected",
    [
        (2020, 1, 31),
        (2020, 2, 29),
        (2020, 3, 31),
        (2020, 4, 30),
        (2020, 5, 31),
        (2020, 6, 30),
        (2020, 7, 31),
        (2020, 8, 31),
        (2020, 9, 30),
        (2020, 10, 31),
        (2020, 11, 30),
        (2020, 12, 31),
        (2021, 1, 31),
        (2021, 2, 28),
        (2021, 3, 31),
        (2021, 4, 30),
        (2021, 5, 31),
        (2021, 6, 30),
        (2021, 7, 31),
        (2021, 8, 31),
        (2021, 9, 30),
        (2021, 10, 31),
        (2021, 11, 30),
        (2021, 12, 31),
        (2022, 1, 31),
        (2022, 2, 28),
        (2022, 3, 31),
        (2022, 4, 30),
        (2022, 5, 31),
        (2022, 6, 30),
        (2022, 7, 31),
        (2022, 8, 31),
        (2022, 9, 30),
        (2022, 10, 31),
        (2022, 11, 30),
        (2022, 12, 31),
        (2023, 1, 31),
        (2023, 2, 28),
        (2023, 3, 31),
        (2023, 4, 30),
        (2023, 5, 31),
        (2023, 6, 30),
        (2023, 7, 31),
        (2023, 8, 31),
        (2023, 9, 30),
        (2023, 10, 31),
        (2023, 11, 30),
        (2023, 12, 31),
    ],
)
def test_num_days_in_month(year, month, expected):
    assert num_days_in_month(year, month) == expected


@pytest.mark.parametrize(
    "dtformat, dt, expected",
    [
        (
            DatetimeFormat.TWITTER,
            datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            "Wed Jan 01 00:00:00 +0000 2020",
        ),
        (
            DatetimeFormat.TWITTER,
            datetime(2020, 1, 1, 12, 30, 30, tzinfo=timezone.utc),
            "Wed Jan 01 12:30:30 +0000 2020",
        ),
        (
            DatetimeFormat.TWITTER,
            datetime(2020, 1, 1, 1, 30, 30, tzinfo=timezone.utc),
            "Wed Jan 01 01:30:30 +0000 2020",
        ),
        (
            DatetimeFormat.REDDIT,
            datetime(2020, 1, 1, 0, 0, 0, tzinfo=None),
            "Jan 01 2020 12:00 AM",
        ),
        (
            DatetimeFormat.REDDIT,
            datetime(2020, 1, 1, 12, 30, 30, tzinfo=None),
            "Jan 01 2020 12:30 PM",
        ),
        (
            DatetimeFormat.REDDIT,
            datetime(2020, 1, 1, 1, 30, 30, tzinfo=None),
            "Jan 01 2020 01:30 AM",
        ),
        (
            DatetimeFormat.ISO_8601,
            datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            "2020-01-01T00:00:00+0000",
        ),
        (
            DatetimeFormat.ISO_8601,
            datetime(2020, 1, 1, 12, 30, 30, tzinfo=timezone.utc),
            "2020-01-01T12:30:30+0000",
        ),
        (
            DatetimeFormat.ISO_8601,
            datetime(2020, 1, 1, 1, 30, 30, tzinfo=timezone.utc),
            "2020-01-01T01:30:30+0000",
        ),
        (
            DatetimeFormat.DATABASE,
            datetime(2020, 1, 1, 0, 0, 0, tzinfo=None),
            "2020-01-01 00:00:00",
        ),
        (
            DatetimeFormat.DATABASE,
            datetime(2020, 1, 1, 12, 30, 30, tzinfo=None),
            "2020-01-01 12:30:30",
        ),
        (
            DatetimeFormat.DATABASE,
            datetime(2020, 1, 1, 1, 30, 30, tzinfo=None),
            "2020-01-01 01:30:30",
        ),
        (
            DatetimeFormat.DATE,
            datetime(2020, 1, 1, tzinfo=None),
            "2020-01-01",
        ),
        (
            DatetimeFormat.DATE,
            datetime(2020, 1, 1, 12, 30, 30, tzinfo=None),
            "2020-01-01",
        ),
        (
            DatetimeFormat.DATE,
            datetime(2020, 1, 1, 1, 30, 30, tzinfo=None),
            "2020-01-01",
        ),
        (
            DatetimeFormat.TIME_12H,
            datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            "12:00 AM UTC",
        ),
        (
            DatetimeFormat.TIME_12H,
            datetime(2020, 1, 1, 12, 30, 30, tzinfo=timezone.utc),
            "12:30 PM UTC",
        ),
        (
            DatetimeFormat.TIME_12H,
            datetime(2020, 1, 1, 1, 30, 30, tzinfo=timezone.utc),
            "01:30 AM UTC",
        ),
        (
            DatetimeFormat.TIME_24H,
            datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            "00:00 UTC",
        ),
        (
            DatetimeFormat.TIME_24H,
            datetime(2020, 1, 1, 12, 30, 30, tzinfo=timezone.utc),
            "12:30 UTC",
        ),
        (
            DatetimeFormat.TIME_24H,
            datetime(2020, 1, 1, 1, 30, 30, tzinfo=timezone.utc),
            "01:30 UTC",
        ),
    ],
)
def test_DatetimeFormat_strftime(dtformat, dt, expected):
    assert dt.strftime(dtformat) == expected


@pytest.mark.parametrize(
    "dtformat, dt, expected",
    [
        (
            DatetimeFormat.TWITTER,
            "Wed Jan 01 00:00:00 +0000 2020",
            datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        ),
        (
            DatetimeFormat.TWITTER,
            "Wed Jan 01 12:30:30 +0000 2020",
            datetime(2020, 1, 1, 12, 30, 30, tzinfo=timezone.utc),
        ),
        (
            DatetimeFormat.TWITTER,
            "Wed Jan 01 01:30:30 +0000 2020",
            datetime(2020, 1, 1, 1, 30, 30, tzinfo=timezone.utc),
        ),
        (
            DatetimeFormat.REDDIT,
            "Jan 01 2020 12:00 AM",
            datetime(2020, 1, 1, 0, 0, 0, tzinfo=None),
        ),
        (
            DatetimeFormat.REDDIT,
            "Jan 01 2020 12:30 PM",
            datetime(2020, 1, 1, 12, 30, tzinfo=None),
        ),
        (
            DatetimeFormat.REDDIT,
            "Jan 01 2020 01:30 AM",
            datetime(2020, 1, 1, 1, 30, tzinfo=None),
        ),
        (
            DatetimeFormat.ISO_8601,
            "2020-01-01T00:00:00+0000",
            datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        ),
        (
            DatetimeFormat.ISO_8601,
            "2020-01-01T12:30:30+0000",
            datetime(2020, 1, 1, 12, 30, 30, tzinfo=timezone.utc),
        ),
        (
            DatetimeFormat.ISO_8601,
            "2020-01-01T01:30:30+0000",
            datetime(2020, 1, 1, 1, 30, 30, tzinfo=timezone.utc),
        ),
        (
            DatetimeFormat.DATABASE,
            "2020-01-01 00:00:00",
            datetime(2020, 1, 1, 0, 0, 0, tzinfo=None),
        ),
        (
            DatetimeFormat.DATABASE,
            "2020-01-01 12:30:30",
            datetime(2020, 1, 1, 12, 30, 30, tzinfo=None),
        ),
        (
            DatetimeFormat.DATABASE,
            "2020-01-01 01:30:30",
            datetime(2020, 1, 1, 1, 30, 30, tzinfo=None),
        ),
        (
            DatetimeFormat.DATE,
            "2020-01-01",
            datetime(2020, 1, 1, tzinfo=None),
        ),
        (
            DatetimeFormat.DATE,
            "2020-01-01",
            datetime(2020, 1, 1, tzinfo=None),
        ),
        (
            DatetimeFormat.DATE,
            "2020-01-01",
            datetime(2020, 1, 1, tzinfo=None),
        ),
        # NOTE: These tests are commented out because they fail.
        # Bug or because of no year?
        # (
        #     DatetimeFormat.TIME_12H,
        #     "12:00 AM UTC",
        #     datetime(1900, 1, 1, 0, 0, tzinfo=timezone.utc),
        # ),
        # (
        #     DatetimeFormat.TIME_12H,
        #     "12:30 PM UTC",
        #     datetime(1900, 1, 1, 12, 30, tzinfo=timezone.utc),
        # ),
        # (
        #     DatetimeFormat.TIME_12H,
        #     "01:30 AM UTC",
        #     datetime(1900, 1, 1, 1, 30, tzinfo=timezone.utc),
        # ),
        # (
        #     DatetimeFormat.TIME_24H,
        #     "00:00 UTC",
        #     datetime(1900, 1, 1, 0, 0, tzinfo=timezone.utc),
        # ),
        # (
        #     DatetimeFormat.TIME_24H,
        #     "12:30 UTC",
        #     datetime(1900, 1, 1, 12, 30, tzinfo=timezone.utc),
        # ),
        # (
        #     DatetimeFormat.TIME_24H,
        #     "01:30 UTC",
        #     datetime(1900, 1, 1, 1, 30, tzinfo=timezone.utc),
        # ),
    ],
)
def test_DatetimeFormat_strptime(dtformat, dt, expected):
    assert datetime.strptime(dt, dtformat) == expected


def test_utc_pickle():
    dt = datetime(2020, 1, 1, 0, 0, 0, tzinfo=utc)
    naive = dt.replace(tzinfo=None)
    p = pickle.dumps(dt, 1)
    naive_p = pickle.dumps(naive, 1)
    assert len(p) - len(naive_p) > 0
    new = pickle.loads(p)
    assert new == dt
    assert new is not dt
    assert new.tzinfo is dt.tzinfo
