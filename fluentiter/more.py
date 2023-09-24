from typing import Tuple, TypeVar

import fluentiter as fl
from fluentiter.exceptions import RequiresExtraError

T = TypeVar("T")

try:
    import more_itertools as miter
except ImportError as e:  # pragma: no cover
    raise RequiresExtraError(
        "This feature requires extra `more` "
        "Install with `pip install 'fluentiter[more]'`"
    ) from e


class RollingWindowIterator(fl.FluentIterator[Tuple[T, ...]]):
    """
    Iterator which returns overlapping tuples of size
    `n` containing the iterators elements.
    """

    __slots__ = ("_iterable",)

    def __init__(self, it: fl.FluentIterator[T], size: int) -> None:
        self._iterable = miter.sliding_window(it, size)
