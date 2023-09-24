import itertools
from operator import length_hint
from typing import (
    Any,
    Callable,
    Generator,
    Iterable,
    Iterator,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

import fluentiter as fl
import fluentiter.exceptions as fle

Inner = TypeVar("Inner")
T = TypeVar("T")
U = TypeVar("U")
R = TypeVar("R")


class StepByIterator(fl.FluentIterator[T]):
    """
    Iterator which steps over elements with steps of size `n`.
    """

    __slots__ = ("_iterable",)

    def __init__(self, it: fl.FluentIterator[T], n: int) -> None:
        self._iterable = itertools.islice(it, None, None, n)


class ChainedIterator(fl.FluentIterator[Union[T, U]]):
    """
    Iterator which first yields all elements of
    A and then all elements of B
    """

    __slots__ = ("_iterable",)

    def __init__(
        self, first: fl.FluentIterator[T], other: fl.FluentIterator[U]
    ) -> None:
        self._iterable = itertools.chain(first, other)
        self._first = first
        self._other = other

    def size_hint(self) -> Union[int, None]:
        """
        Get an estimate of the number of elements in
        this iterator or `None` if the value can not be
        estimated.

        Returns
        -------
        Union[int, None]
            Length hint
        """
        hintfirst = length_hint(self._first, -1)
        hintsecond = length_hint(self._other, -1)
        if hintfirst == -1 or hintsecond == -1:
            return None
        return hintfirst + hintsecond


class ZippedIterator(fl.FluentIterator[Tuple[T, U]]):
    """
    Iterator which yields tuples of (T, U)
    """

    __slots__ = ("_iterable",)

    def __init__(self, it: fl.FluentIterator[T], other: fl.FluentIterator[U]) -> None:
        self._iterable = zip(it, other)


class MapIterator(fl.FluentIterator[R]):
    """
    Iterator which applies a function to every element
    """

    __slots__ = ("_iterable",)

    def __init__(self, it: fl.FluentIterator[T], func: Callable[[T], R]) -> None:
        self._iterable = map(func, it)


class FilterIterator(fl.FluentIterator[T]):
    """
    Iterator which filters using a given function
    """

    __slots__ = ("_iterable",)

    def __init__(self, it: fl.FluentIterator[T], func: Callable[[T], bool]) -> None:
        self._iterable = filter(func, it)


class FilterMapIterator(fl.FluentIterator[R]):
    """
    Iterator which filters and maps using a given function
    """

    __slots__ = ("_iterable",)

    def __init__(
        self, it: fl.FluentIterator[T], func: Callable[[T], Optional[R]]
    ) -> None:
        # for some reason .filter gets inferred ot -> FluentIterator | None here
        self._iterable = cast(
            fl.FluentIterator[R], it.map(func=func).filter(lambda x: x is not None)
        )


class EnumerateIterator(fl.FluentIterator[Tuple[int, T]]):
    """
    Iterator which yields tuples of (index, element)
    """

    __slots__ = ("_iterable",)

    def __init__(self, it: fl.FluentIterator[T]) -> None:
        self._iterable = enumerate(it)


class PeekIterator(fl.FluentIterator[T]):
    """
    Iterator which allows to peek the next element
    """

    __slots__ = ("_iterable",)

    def __init__(self, it: Iterator[T]) -> None:
        self._iterable = it
        self._sentinel = object()
        self._peeked = next(it)

    def __next__(self) -> T:
        next_val = self._peeked
        try:
            self._peeked = next(self._iterable)
        except StopIteration:
            self._peeked = self._sentinel  # type: ignore[assignment]

        if next_val is self._sentinel:
            raise StopIteration
        return next_val


class SkipWhileIterator(fl.FluentIterator[T]):
    """
    Iterator which skips elements as long as a predicate is true
    """

    __slots__ = ("_iterable",)

    def __init__(
        self, it: fl.FluentIterator[T], predicate: Callable[[T], bool]
    ) -> None:
        self._iterable = itertools.dropwhile(predicate, it)


class TakeWhileIterator(fl.FluentIterator[T]):
    """
    Iterator which yields elements as long as a predicate is true
    """

    __slots__ = ("_iterable",)

    def __init__(
        self, it: fl.FluentIterator[T], predicate: Callable[[T], bool]
    ) -> None:
        self._iterable = itertools.takewhile(predicate, it)


class MapWhileIterator(fl.FluentIterator[R]):
    """
    Iterator which applys a function to every element as long as that
    function does not return `None`
    """

    __slots__ = ("_iterable",)

    def __init__(
        self, it: fl.FluentIterator[T], func: Callable[[T], Union[R, None]]
    ) -> None:
        self._iterable = cast(
            TakeWhileIterator[R], it.map(func).take_while(lambda x: x is not None)
        )


class SkipNIterator(fl.FluentIterator[T]):
    """
    Iterator which skips its first `N` elements
    """

    __slots__ = ("_iterable",)

    def __init__(self, it: fl.FluentIterator[T], n: int) -> None:
        self._iterable = itertools.islice(it, n, None)


class TakeNIterator(fl.FluentIterator[T]):
    """
    Iterator which only returns its first `N` elements
    """

    __slots__ = ("_iterable",)

    def __init__(self, it: fl.FluentIterator[T], n: int) -> None:
        self._iterable = itertools.islice(it, None, n)


class ScanIterator(fl.FluentIterator[R]):
    """
    Iterator which holds some state and applies a function using
    that state to every element.
    """

    __slots__ = ("_iterable",)
    S = TypeVar("S")

    def __init__(
        self,
        it: fl.FluentIterator[T],
        initial_state: S,
        func: Callable[[S, T], Tuple[S, R]],
    ) -> None:
        self._iterable = self._scan(it, initial_state, func)

    def _scan(
        self,
        it: fl.FluentIterator[T],
        initial_state: S,
        func: Callable[[S, T], Tuple[S, R]],
    ) -> Generator[R, None, None]:
        state = initial_state
        for x in it:
            try:
                state, val = func(state, x)
                yield val
            except fle.StopScan:
                return


class FlatMapIterator(fl.FluentIterator[R]):
    """
    Iterator which maps flattens elements
    """

    __slots__ = ("_iterable",)

    def __init__(
        self,
        it: fl.FluentIterator[T],
        func: Callable[[T], Union[R, Iterable[R]]],
        exclude: Tuple[Type, ...],
    ) -> None:
        self._iterable = it.map(func).flatten(exclude=exclude)


class FlattenIterator(fl.FluentIterator[T]):
    """
    Iterator which flattens elements
    """

    __slots__ = ("_iterable",)

    def __init__(
        self, it: fl.FluentIterator[Union[T, Iterable[T]]], exclude: Tuple[Type, ...]
    ) -> None:
        self._iterable = self._flatten(it)
        self._exclude = exclude

    def _flatten(
        self, it: fl.FluentIterator[Union[T, Iterable[T]]]
    ) -> Generator[T, None, None]:
        for elem in it:
            if isinstance(elem, Iterable) and not isinstance(elem, self._exclude):
                yield from elem
            else:
                yield cast(T, elem)


class InspectIterator(fl.FluentIterator[T]):
    """
    Iterator which applies a function to every element
    but yields the original elements
    """

    __slots__ = ("_iterable",)

    def __init__(self, it: fl.FluentIterator[T], func: Callable[[T], Any]) -> None:
        self._iterable = self._scan(it, func)

    def _scan(
        self, it: fl.FluentIterator[T], func: Callable[[T], Any]
    ) -> Generator[T, None, None]:
        for x in it:
            func(x)
            yield x


class CycleIterator(fl.FluentIterator[T]):
    """
    Iterator which keeps one copy of every element
    and cycles through them forever
    """

    __slots__ = ("_iterable",)

    def __init__(self, it: fl.FluentIterator[T]) -> None:
        self._iterable = itertools.cycle(it)
