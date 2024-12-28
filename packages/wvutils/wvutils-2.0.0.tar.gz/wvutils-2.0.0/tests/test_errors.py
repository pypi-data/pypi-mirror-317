import pytest

from wvutils.errors import (
    HashEncodeError,
    HashError,
    JSONDecodeError,
    JSONEncodeError,
    JSONError,
    PickleDecodeError,
    PickleEncodeError,
    PickleError,
    WVUtilsError,
)


@pytest.mark.parametrize("cls", [Exception, BaseException])
def test_WVUtilsError(cls):
    assert issubclass(WVUtilsError, cls)
    assert isinstance(WVUtilsError(), cls)


@pytest.mark.parametrize("cls", [Exception, BaseException])
def test_JSONError(cls):
    assert issubclass(JSONError, cls)
    assert isinstance(JSONError(), cls)


@pytest.mark.parametrize("cls", [JSONError, TypeError, Exception, BaseException])
def test_JSONEncodeError(cls):
    assert issubclass(JSONEncodeError, cls)
    assert isinstance(JSONEncodeError(), cls)


@pytest.mark.parametrize("cls", [JSONError, ValueError, Exception, BaseException])
def test_JSONDecodeError(cls):
    assert issubclass(JSONDecodeError, cls)
    assert isinstance(JSONDecodeError(), cls)


@pytest.mark.parametrize("cls", [Exception, BaseException])
def test_PickleError(cls):
    assert issubclass(PickleError, cls)
    assert isinstance(PickleError(), cls)


@pytest.mark.parametrize("cls", [PickleError, TypeError, Exception, BaseException])
def test_PickleEncodeError(cls):
    assert issubclass(PickleEncodeError, cls)
    assert isinstance(PickleEncodeError(), cls)


@pytest.mark.parametrize("cls", [PickleError, ValueError, Exception, BaseException])
def test_PickleDecodeError(cls):
    assert issubclass(PickleDecodeError, cls)
    assert isinstance(PickleDecodeError(), cls)


@pytest.mark.parametrize("cls", [Exception, BaseException])
def test_HashError(cls):
    assert issubclass(HashError, cls)
    assert isinstance(HashError(), cls)


@pytest.mark.parametrize("cls", [HashError, TypeError, Exception, BaseException])
def test_HashEncodeError(cls):
    assert issubclass(HashEncodeError, cls)
    assert isinstance(HashEncodeError(), cls)
