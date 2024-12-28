import pytest

from wvutils.args import (
    integer_string,
    nonempty_string,
    safechars_string,
)


@pytest.mark.parametrize(
    "value, expected",
    [("a", "a"), (" a ", "a"), ("   a   ", "a")],
)
def test_nonempty_string_returns_on_nonempty_string(value, expected):
    name = "func_name"
    func = nonempty_string("func_name")
    actual = func(value)
    assert func.__name__ == name
    assert actual == expected


@pytest.mark.parametrize(
    "value",
    ["", " ", "   ", "\n", "\n\n\n", "\t", "\t\t\t"],
)
def test_empty_string_raises_on_empty_string(value):
    with pytest.raises(ValueError, match=r"^Must not be empty$"):
        nonempty_string("func_name")(value)


@pytest.mark.parametrize(
    "allowed_chars, value, expected",
    [
        (None, "a", "a"),
        ("abc", "a", "a"),
        (set("abc"), "a", "a"),
        (tuple("abc"), "a", "a"),
        (list("abc"), "a", "a"),
        (iter("abc"), "a", "a"),
    ],
)
def test_safechars_string_returns_on_valid_chars(allowed_chars, value, expected):
    name = "func_name"
    func = safechars_string(name, allowed_chars=allowed_chars)
    assert func.__name__ == name
    assert func(value) == expected


@pytest.mark.parametrize(
    "allowed_chars, value",
    [
        (None, "$"),
        ("abc", "d"),
        (set("abc"), "d"),
        (tuple("abc"), "d"),
        (list("abc"), "d"),
        (iter("abc"), "d"),
    ],
)
def test_safechars_string_raises_on_invalid_chars(allowed_chars, value):
    with pytest.raises(ValueError, match=r"^Must consist of characters \[.+\]$"):
        safechars_string("func_name", allowed_chars=allowed_chars)(value)


@pytest.mark.parametrize(
    "allowed_chars",
    [str(), set(), tuple(), list()],
)
def test_safechars_string_raises_on_zero_allowed_chars(allowed_chars):
    with pytest.raises(ValueError, match=r"^Must provide at least one character$"):
        safechars_string("func_name", allowed_chars=allowed_chars)


@pytest.mark.parametrize(
    "value, expected",
    [("-1", -1), (" 0 ", 0), ("1", 1)],
)
def test_integer_string(value, expected):
    name = "func_name"
    func = integer_string(name)
    assert func.__name__ == name
    assert func(value) == expected


@pytest.mark.parametrize(
    "value",
    ["", " ", "   ", "\n", "\n\n\n", "\t", "\t\t\t", "a", "-1.0", "1.0"],
)
def test_integer_string_raises_on_invalid_string(value):
    with pytest.raises(ValueError, match=r"^Must be an integer$"):
        integer_string("func_name")(value)


def test_integer_string_raises_on_min_value():
    with pytest.raises(ValueError, match=r"^Must be at least 0$"):
        integer_string("func_name", min_value=0)(" -1 ")


def test_integer_string_raises_on_max_value():
    with pytest.raises(ValueError, match=r"^Must be at most 0$"):
        integer_string("func_name", max_value=0)(" 1 ")
