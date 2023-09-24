from typing import Iterable, TypeVar

from fluentiter.core import FluentIterator

T = TypeVar("T")


def iterator(iterable: Iterable[T]) -> "FluentIterator[T]":
    return FluentIterator(iterable=iterable)


__all__ = ["iterator", "FluentIterator"]
