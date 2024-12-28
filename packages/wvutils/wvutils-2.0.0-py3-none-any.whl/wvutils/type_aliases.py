"""Custom type aliases and type variables.

This module contains custom type aliases and type variables used throughout the package.
"""
from __future__ import annotations

import collections
import io
import os
from collections.abc import Hashable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypeAlias

__all__ = [
    "FileObject",
    "FilePath",
    "JSONSerializable",
    "MD5Hashable",
    "Mask",
    "Masks",
    "PickleSerializable",
    "Span",
    "Spans",
]


# Python types
# DictKey: TypeAlias = str | int | float | bool | object | None
FilePath: TypeAlias = str | os.PathLike[str]
# FileObject: TypeAlias = io.IOBase | io.RawIOBase | io.BufferedIOBase | io.TextIOBase
FileObject: TypeAlias = io.TextIOBase | io.BytesIO

# Spans and masks
Span: TypeAlias = list[int] | tuple[int, int]
Spans: TypeAlias = list[Span] | collections.deque[Span]
Mask: TypeAlias = str
Masks: TypeAlias = list[Mask] | collections.deque[Mask]

# Serialization
JSONSerializable: TypeAlias = str | int | float | bool | list | dict | None
PickleSerializable: TypeAlias = object
MD5Hashable: TypeAlias = JSONSerializable | tuple | Hashable
