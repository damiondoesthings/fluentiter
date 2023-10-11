import functools
import itertools
from operator import length_hint
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    List,
    Literal,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

if TYPE_CHECKING:
    from fluentiter import more  # pragma: no cover
    from fluentiter.itertypes import (  # pragma: no cover
        ChainedIterator,
        CycleIterator,
        EnumerateIterator,
        FilterIterator,
        FilterMapIterator,
        FlatMapIterator,
        FlattenIterator,
        InspectIterator,
        MapIterator,
        MapWhileIterator,
        ScanIterator,
        SkipNIterator,
        SkipWhileIterator,
        StepByIterator,
        TakeNIterator,
        TakeWhileIterator,
        ZippedIterator,
    )

ITER_STOP = object()
Inner = TypeVar("Inner", covariant=True)
T = TypeVar("T", covariant=True)
U = TypeVar("U")
R = TypeVar("R")


class FluentIterator(Generic[T], Iterator[T]):
    """
    Easy to use container for iterables
    """

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iterable = iter(iterable)

    def _infallible_next(self) -> Union[T, object]:
        try:
            return next(self._iterable)
        except StopIteration:
            return ITER_STOP

    def next(self) -> T:
        """
        Advances the iterator and returns the next value.

        Will return `None` the iterator is exhausted

        Returns
        -------
        Optional[T]
            Next element or None if iterator is exhausted

        Raises
        ------
        StopIteration
            If there is no next element
        """
        return next(self)

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
        hint = length_hint(self._iterable, -1)
        if hint == -1:
            return None
        return hint

    def count(self) -> int:
        """
        Count the elements in this iterator.
        This will consume the iterator.

        Returns
        -------
        int
            Count of items

        Examples
        --------
        >>> iterator(range(5)).count()
            5
        """
        i = 0
        for _ in self:
            i += 1
        return i

    def last(self) -> Optional[T]:
        """
        Return the last element in this iterator.
        If the iterator does not contain any elements,
        this returns None.

        This consumes the iterator.

        Returns
        -------
        Optional[T]
            Last element or None

        Raises
        ------
        EmptyIteratorError
            If the iterator has no elements

        Examples
        --------
        >>> iterator(["foo", "bar", "baz"]).last()
            "baz"
        >>> iterator([]).last()
            None
        """
        from fluentiter.exceptions import EmptyIteratorError

        has_elems = False
        for y in self:
            has_elems = True
            x = y
        if has_elems:
            return x
        raise EmptyIteratorError

    def nth(self, index: int) -> Optional[T]:
        """
        Returns the nth element of the iterator.
        The index starts at `0`, i.e. `nth(0)` returns the first element.
        If the index is greater than or equal to the length of the iterator, this will return None.

        Notes
        -----
        This method consumes the iterator up to and including `index`.

        Parameters
        ----------
        index : int
            The index to return

        Raises
        ------
        IndexError
            If the iterator has less than `index + 1` items

        Returns
        -------
        Optional[T]
            Value at the index or `None` if index is >= iterator length

        Examples
        --------
        >>> iterator(["n", "t", "h"]).nth(1)
            "t"
        """
        try:
            if index < 0:
                raise ValueError("Index must be positive")
            return self.skip(index).next()
        except StopIteration:
            raise IndexError

    def step_by(self, size: int) -> "StepByIterator[T]":
        """
        Steps over the iterator with steps of size `size`.
        The first element of the iterator is always returned,
        subsequent items are only returned if there index is a
        multiple of `size`.


        Parameters
        ----------
        size : int
            Size of the step.

        Returns
        -------
        FluentIterator[T]
            Stepping iterator

        Examples
        --------
        >>> iterator([1,2,3,4,5]).step_by(2).to_list()
            [1, 3, 5]
        >>> iterator([1,2,3,4,5]).step_by(1).to_list()
            [1, 2, 3, 4, 5]
        """
        from fluentiter.itertypes import StepByIterator

        return StepByIterator(self, size)

    def chain(self, other: Iterable[U]) -> "ChainedIterator[T, U]":
        """
        Chain another iterable to the end of this iterator.
        The returned iterator will first yield all items of `self` and then
        yield all items of `other`.

        Parameters
        ----------
        other : Iterable[U]
            Iterable to chain to this one.

        Returns
        -------
        FluentIterator[Union[T, U]]
            Chained iterator

        Examples
        --------
        >>> iterator(["We", "didn't"]).chain(["start", "the", "fire"]).to_list()
            ["We", "didn't", "start", "the", "fire"]
        """
        from fluentiter import iterator
        from fluentiter.itertypes import ChainedIterator

        return ChainedIterator(self, iterator(other))

    def zip(self, other: Iterable[U]) -> "ZippedIterator[T, U]":
        """
        Zip this iterator with another iterable, yielding 2-element tuples
        where the first element is an element from this iterator and the
        second element is an element of `other`.

        The iteration stops, as soon as one of the iterators is exhausted.

        Parameters
        ----------
        other : Iterable[U]
            An Iterable to zip this iterator with

        Returns
        -------
        FluentIterator[Tuple[T, U]]
            Zipped iterator

        Examples
        --------
        >>> iterator(["ping", "ping"]).zip(["pong", "pong"]).to_list()
            [("ping", "pong"), ("ping", "pong")]
        """
        from fluentiter import iterator
        from fluentiter.itertypes import ZippedIterator

        return ZippedIterator(self, iterator(other))

    def map(self, func: Callable[[T], R]) -> "MapIterator[R]":
        """
        Apply a given function `func` to every element of the iterator,
        and return an iterator yielding the results of those function calls.

        Keep in mind, the function is not applied immediatly
        but as items are yielded from the iterator.

        Parameters
        ----------
        func : Callable[[T], R]
            Function to apply to every element.

        Returns
        -------
        FluentIterator[R]
            Iterator yielding the function call results

        Examples
        --------
        >>> iterator(["don't", "panic"]).map(lambda x: x.upper()).to_list()
            ["DON'T", "PANIC"]
        """
        from fluentiter.itertypes import MapIterator

        return MapIterator(self, func)

    def filter(self, func: Callable[[T], bool]) -> "FilterIterator[T]":
        """
        Create a filtered iterator by applying a function to every element
        to evaluate whether or not it should be yielded.

        If the given function returns `True` the item will be yielded.
        If the function returns `False` the iterator will skip the item.

        Parameters
        ----------
        func : Callable[[T], bool]
            Function to apply as a filter.

        Returns
        -------
        FluentIterator[T]
            Filtered iterator

        Examples
        --------
        >>> iterator([1.0, 1.5, 2.0]).filter(lambda x: x.is_integer()).to_list()
            [1.0, 2.0]
        """
        from fluentiter.itertypes import FilterIterator

        return FilterIterator(self, func)

    def filter_map(self, func: Callable[[T], Optional[R]]) -> "FilterMapIterator[R]":
        """
        A combination of `.map` and `.filter`. Apply a given function to every
        element of the iterator and return the result only if it is not `None`.

        Parameters
        ----------
        func : Callable[[T], Optional[R]]
            Function to apply, returns `None` for elements to be filtered out.

        Returns
        -------
        FluentIterator[R]
            Iterator of mapped values.

        Examples
        --------
        >>> (iterator([{"food": "cake"}, {"beverage": "coffee"}])
        >>>     .filter_map(lambda x: x.get("food", None))
        >>>     .to_list()
        >>> )
            ["cake"]
        """
        from fluentiter.itertypes import FilterMapIterator

        return FilterMapIterator(self, func)

    def enumerate(self) -> "EnumerateIterator[Tuple[int, T]]":
        """
        Create an iterator which yields tuples of `(index, value)`.


        Returns
        -------
        FluentIterator[Tuple[int, T]]
            Iterator of index, value tuples

        Examples
        -------
        >>> iterator(["zero", "one", "two"]).enumerate().to_list()
            [(0, "zero"), (1, "one"), (2, "two")]
        """
        from fluentiter.itertypes import EnumerateIterator

        return EnumerateIterator(self)  # type: ignore[arg-type]

    def peek(self) -> T:
        """
        Return the next element of the iterator, **without** advancing it.

        Notes
        -----
        Calling peek multiple times consecutively always returns
        the same element

        Returns
        -------
        T
            The next element in the iterator

        Raises
        ------
        StopIteration
            If there is no next element to peek

        Examples
        --------
        >>> myiter = iterator(["p", "e", "e", "k"])
        >>> myiter.peek()
            p
        >>> myiter.peek()
            p
            myiter.to_list()
            ["p", "e", "e", "k"]
        """
        from fluentiter.itertypes import PeekIterator

        if not isinstance(self, PeekIterator):
            self._iterable = PeekIterator(self._iterable)
        self._iterable = cast(PeekIterator[T], self._iterable)
        return self._iterable._peeked

    def skip_while(self, func: Callable[[T], bool]) -> "SkipWhileIterator[T]":
        """
        Skip elements of this iterator by applying the given function to every
        element while it returns `True`. After the function has returned `False`,
        it will not be applied anymore and all subsequent items are yielded.

        The first element where the function returns `False` is also yielded.

        Parameters
        ----------
        func : Callable[[T], bool]
            Function to apply to every element

        Returns
        -------
        SkipWhileIterator[T]
            Iterator which skips elements while `func` returns `True`

        Examples
        --------
        >>> week = ["Thursday", "Friday", "Saturday", "Sunday"]
        >>> iterator(week).skip_while(lambda x: x != "Saturday").to_list()
            ["Saturday", "Sunday"]
        """
        from fluentiter.itertypes import SkipWhileIterator

        return SkipWhileIterator(self, predicate=func)

    def take_while(self, func: Callable[[T], bool]) -> "TakeWhileIterator[T]":
        """
        Apply a given function to every element of the iterator and only
        yield elements while this function returns `True`. Once the function
        returns `False` the iterator will be exhausted and not yield any
        further items.

        Parameters
        ----------
        func : Callable[[T], bool]
            Function to apply to every element

        Returns
        -------
        TakeWhileIterator[T]
            Iterator which yields elements until `func` returns `False`

        Examples
        -------
        >>> week = ["Saturday, "Sunday", "Monday", "Tuesday", "Wednesday"]
        >>> iterator(week).take_while(lambda x: x in {"Saturday", "Sunday"}).to_list()
            ["Monday", "Tuesday", "Wednesday"]
        """
        from fluentiter.itertypes import TakeWhileIterator

        return TakeWhileIterator(self, predicate=func)

    def map_while(self, func: Callable[[T], Union[R, None]]) -> "MapWhileIterator[R]":
        """
        A combination of `map` and `take_while`. Applies the given function to
        all elements of the iterator and yields the results. Once the function returns
        `None` the iterator will be exhausted and not yield any further items.

        Parameters
        ----------
        func : Callable[[T], Union[R, None]]
            Function to apply to every element

        Returns
        -------
        FluentIterator[R]
            Iterator which yields mapped elements until `func` returns `None`

        Examples
        --------
        >>> me = [{"state": "napping"}, {"state": "eating"}, {"state": None}, {"state": "napping"}]
        >>> iterator(me).map_while(lambda x: x.get("state", None)).to_list()
            ["napping", "eating"]
        """
        from fluentiter.itertypes import MapWhileIterator

        return MapWhileIterator(self, func)

    def skip(self, n: int) -> "SkipNIterator[T]":
        """
        Skip the first `n` elements of this iterator.
        After `n` elements have been skipped, all subsequent elements
        are yielded.

        Parameters
        ----------
        n : int
            Number of elements to skip

        Returns
        -------
        FluentIterator[T]
            Iterator which skips its first `n` elements

        Examples
        --------
        >>> iterator(["do", "not", "pet", "the", "dog"]).skip(2).to_list()
            ["pet", "the", "dog"]

        """
        from fluentiter.itertypes import SkipNIterator

        return SkipNIterator(self, n)

    def take(self, n: int) -> "TakeNIterator[T]":
        """
        Only yield the first `n` items of the iterator.
        After `n` elements have been yielded, the iterator
        will be exhausted.

        Parameters
        ----------
        n : int
            Number of items to yield

        Returns
        -------
        FluentIterator[T]
            Iterator which yields the first `n` items

        Examples
        --------
        >>> music = ["on me", "me out", "that"]
        >>> iterator(music).take(2).to_list()
            ["on me", "me out"]
        """
        from fluentiter.itertypes import TakeNIterator

        return TakeNIterator(self, n)

    S = TypeVar("S")

    def scan(
        self, initial_state: S, func: Callable[[S, T], Tuple[S, R]]
    ) -> "ScanIterator[R]":
        """
        Create an iterator which holds some internal state and applies some function
        using that state to every element, returning a tuple of the new state
        and a mapped element. The new state may then be used by the next iteration.

        Notes
        -----
        - To end the iteration, the function should raise `StopScan`.

        - For the curious: The state is returned instead of mutated directly,
          as many elements in Python (e.g. integers) are immutable and need to be reassigned.

        Parameters
        ----------
        initial_state : S
            Inital value of the state
        func : Callable[[S, T], Tuple[S, R]]
            Function to recieve the state and element as arguments

        Returns
        -------
        FluentIterator[R]
            Mapped iterator

        Examples
        --------
        >>> iterator(range(10)).scan(
        >>>     initial_state=(0, 0), func=lambda s, x: ((s[1], sum(s) or x), sum(s) or x)
        >>> )
            [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        """
        from fluentiter.itertypes import ScanIterator

        return ScanIterator(self, initial_state, func)

    def flat_map(
        self: "FluentIterator[T]",
        func: Callable[[T], Union[R, Iterable[R]]],
        exclude: Tuple[Type, ...] = (str, bytes),
    ) -> "FlatMapIterator[R]":
        """
        Create an iterator which maps a function `func` across all elements,
        but also flattens the results if they are iterables.

        Notes
        -----
        By default `str` and `bytes` will not be flattened. You can control this via the
        `exclude` parameter

        Parameters
        ----------
        func : Callable[[T], Union[R, Iterable[R]]]
            Function to apply to all elements
        exclude : Tuple[Type, ...]
            Types which shall not be flattened, by default (str, bytes)

        Returns
        -------
        FluentIterator[R]
            Iterator of flattened results

        Examples
        --------
        >>> dolphins = ["So long", "and thanks", "for all the fish"]
        >>> iterator(dolphins).flat_map(lamba x: x.split()).to_list()
            ["So", "long", "and", "thanks", "for", "all", "the", "fish"]
        """
        from fluentiter.itertypes import FlatMapIterator

        return FlatMapIterator(self, func, exclude)

    def flatten(
        self: "FluentIterator[Union[Inner, Iterable[Inner]]]",
        exclude: Tuple[Type, ...] = (str, bytes),
    ) -> "FlattenIterator[Inner]":
        """
        Make an iterator which which flattens all elements of this
        iterator.

        Notes
        -----
        By default `str` and `bytes` will not be flattened. You can control this via the
        `exclude` parameter

        Parameters
        ----------
        exclude : Tuple[Type, ...]
            Types which shall not be flattened, by default (str, bytes)

        Returns
        -------
        FluentIterator[T]
            Iterator of flattened elements

        Examples
        --------
        >>> iterator([("tire", "earth"), ["screen"]]).flatten().to_list()
            ["tire", "earth", "screen"]
        """
        from fluentiter.itertypes import FlattenIterator

        return FlattenIterator(self, exclude)

    def inspect(self, func: Callable[[T], Any]) -> "InspectIterator[T]":
        """
        Return an iterator which applies `func` to every element, but
        still yields the original elements.
        This is useful if the function has some side effect like logging
        or printing.

        Notes
        -----
        If the elements are mutable, `func` can still mutate them.
        Keep this in mind.

        Parameters
        ----------
        func : Callable[[T], Any]
            Function to apply to every element.

        Returns
        -------
        FluentIterator[T]
            Iterator of the original elements.

        Examples
        --------
        >>> lengths = []
        >>> iterator(["hot", "dog", "bun"]).inspect(lambda x: lengths.append(len(x))).to_list()
            ["hot", "dog", "bun"]
        >>> lengths
            [3, 3, 3]
        """
        from fluentiter.itertypes import InspectIterator

        return InspectIterator(self, func)

    def to_list(self) -> List[T]:
        """
        Collect this iterator into a list, completely consuming it.
        This is just a convenience method for `list()`.

        Returns
        -------
        List[T]
            Collected iterator

        Examples
        --------
        >>> iterator(["bucket", "to-do", "wish"]).to_list()
            ["bucket", "to-do", "wish"]
        """
        return list(self)

    def partition(
        self, func: Callable[[T], bool]
    ) -> Tuple["FluentIterator[T]", "FluentIterator[T]"]:
        """
        Create two iterators from this one, by applying `func` to every element.
        All elements for which `func(element) == False` will become part of the
        first iterator, all those for which it returns `True` wil become part
        of the second iterator

        Parameters
        ----------
        func : Callable[[T], bool]
            Function to apply to sort elements into partitions

        Returns
        -------
        Tuple["FluentIterator[T]", "FluentIterator[T]"]
            Two iterators, made from elements of this iterator

        Examples
        --------
        >>> odds, evens = iterator(range(10)).partition(lambda i: bool(i & 1))
        >>> odds.to_list()
            [0, 2, 4, 6, 8]
        >>> evens.to_list()
            [1, 3, 5, 7, 9]
        """
        from fluentiter import iterator
        from fluentiter.more import miter

        a, b = miter.partition(func, self)
        return iterator(a), iterator(b)

    A = TypeVar("A")

    def fold(self, initial_value: A, func: Callable[[A, T], A]) -> A:
        """
        Fold every element of this iterator into a single value by repeatedly
        applying `func`.
        The given function must takes two parameters, an accumulator `A`
        and an element of the iterator `T` and return the new accumulator `A` to be used
        on the next iteration.

        For an empty iterator this returns the initial value.

        Notes
        -----
        - To return the elements instead of the accumulator, use `.scan`.
        - To use the first element as `initial_value`, use `.reduce`.

        Parameters
        ----------
        initial_value: A
            Initial value of the accumulator
        func : Callable[[S, T], A]
            Folding function

        Returns
        -------
        A
            Folded value

        Examples
        --------
        >>> iterator(["hot", "dog", "bun"]).fold(1, lambda a, x: a + len(x))
            10
        """
        acc = initial_value
        for x in self:
            acc = func(acc, x)
        return acc

    def reduce(self, func: Callable[[T, R], R]) -> Union[T, R]:
        """
        Reduce all elements into a single element by repeatedly applying `func`.

        The given function must take two parameters, the returned value
        of the previous iteration and the element of this iteration.
        For the first iteration this will be the
        first and second element of this iterator resepctively.

        Notes
        -----
        - To return the elements instead of the reduction, use `.scan`.
        - To specify an `initial_value`, use `.fold`.

        Parameters
        ----------
        func : Callable[[T, R], R]
            Reducing function

        Returns
        -------
        Union[T, R]
            Reduced element or first element of the iterator if it only has one.

        Raises
        ------
        EmptyIteratorError
            If called on an empty iterator


        Examples
        --------
        >>> iterator(["reduce", "reuse", "recycle"]).reduce(lambda x, y: f"{x} {y}")
            "reduce reuse recycle"
        """
        from fluentiter.exceptions import EmptyIteratorError

        try:
            return functools.reduce(func, self)  # type: ignore[arg-type]
        except TypeError:
            raise EmptyIteratorError("Cannot reduce an empty iterator")

    def any(self, func: Callable[[T], bool] = bool) -> bool:
        """
        Return `True` if the given function returns `True` for any element
        of this iterator, otherwise return `False`.

        For an empty iterator this is always `False`.

        Parameters
        ----------
        func : Callable[[T], bool], optional
            Function to evaluate elements, by default bool

        Returns
        -------
        bool
            Whether any element of this iterator matches the predicate

        Examples
        --------
        >>> iterator(["one", "2", "three"]).any(lambda x: x.is_digit())
        True
        >>> iterator([]).any()
        False
        """
        for x in self:
            if func(x):
                return True
        return False

    def find(self, func: Callable[[T], bool]) -> T:
        """
        Find and return the first element for which the given function
        returns `True`.

        If no element matches or the iterator is empty, this raises
        `NotFoundError`.

        Parameters
        ----------
        func : Callable[[T], bool]
            Function to test elements

        Returns
        -------
        T
            First element which matches the predicate

        Raises
        ------
        NotFoundError
            If no element matches

        Examples
        --------
        >>> iterator(["bert", "waldo", "ernie"]).find(lambda x: x.startswith("w"))
            "waldo"
        """
        from fluentiter.exceptions import NotFoundError

        for x in self:
            if func(x):
                return x
        raise NotFoundError("No element matching the given predicate")

    def position(self, func: Callable[[T], bool]) -> Union[int, Literal[-1]]:
        """
        Find the index of the first element for which `func(element) == True`.

        If no item matches or the iterator is empty, returns `-1`, this
        behaviour aligns with Pythons `str.find`.

        Parameters
        ----------
        func : Callable[[T], bool]
            Predicate to evaluta elements

        Returns
        -------
        int
            Index of the first element matching the predicate or -1

        Examples
        --------
        >>> iterator(["bert", "waldo", "ernie"]).position(lambda x: x == "waldo")
            1
        """
        for i, e in enumerate(self):
            if func(e):
                return i
        return -1

    def max(self, key: Optional[Callable[[T], Any]] = None) -> T:
        """
        Return the maximum element in this iterator.

        If a key is given, the results of `key(element)` will
        be compared instead of the elements themselves.

        Parameters
        ----------
        key : Optional[Callable[T], Any], optional
            Key to use for comparison, by default None

        Returns
        -------
        T
            Maximum value

        Raises
        ------
        EmptyIteratorError
            If the iterator is empty

        Examples
        --------
        >>> iterator([42, 1337]).max()
            1337
        """
        from fluentiter.exceptions import EmptyIteratorError

        try:
            return max(self)  # type: ignore[type-var]
        except ValueError:
            raise EmptyIteratorError("Can not get `max` of empty iterator")

    def min(self, key: Optional[Callable[[T], Any]] = None) -> T:
        """
        Return the minimum element in this iterator.

        If a key is given, the results of `key(element)` will
        be compared instead of the elements themselves.

        Parameters
        ----------
        key : Optional[Callable[T], Any], optional
            Key to use for comparison, by default None

        Returns
        -------
        T
            Minimum value

        Raises
        ------
        EmptyIteratorError
            If the iterator is empty

        Examples
        --------
        >>> iterator([42, 1337]).min()
            42
        """
        from fluentiter.exceptions import EmptyIteratorError

        try:
            return min(self)  # type: ignore[type-var]
        except ValueError:
            raise EmptyIteratorError("Can not get `min` of empty iterator")

    def unzip(
        self: "FluentIterator[Tuple[T, U]]",
    ) -> Tuple["FluentIterator[T]", "FluentIterator[U]"]:
        """
        Unzip an iterator of tuples into two iterators, by building the first one from all first
        elements of each tuple, and the second from all other elements of the tuples.

        Returns
        -------
        Tuple[FluentIterator[T], FluentIterator[U]]
            Two new iterators

        Examples
        --------
        >>> morning, evening = iterator([("coffee", "beer"), ("pancake", "pizza")]).unzip()
        >>> morning.to_list()
            ["coffee", "pancake"]
        >>> evening.to_list()
            ["beer", "pizza"]
        """
        from fluentiter import iterator

        a, b = itertools.tee(self)
        return (
            iterator((x[0] for x in a)),
            iterator((x[1] if len(x) == 2 else x[1:] for x in b)),  # type: ignore[misc]
        )

    def cycle(self) -> "CycleIterator[T]":
        """
        Make an infinite iterator by repeating the values from this one forever.
        It just goes round and round....

        Notes
        -----
        Do not try to collect an infinite iterator

        Returns
        -------
        CycleIterator[T]
            Infite cycling iterator

        Examples
        --------
        >>> never_ends = iterator("carousel", "wheels on the bus").cycle()
        >>> never_ends.next()
            "carousel"
        >>> never_ends.next()
            "wheels on the bus"
        >>> never_ends.next()
            "carousel"
        >>> never_ends.next()
            "wheels on the bus"
        """
        from fluentiter.itertypes import CycleIterator

        return CycleIterator(self)

    def sum(self) -> Optional[T]:
        """
        Sum up all elements in this iterator

        Returns
        -------
        Optional[T]
            The sum of all elements or `None` if iterator is empty

        Examples
        --------
        >>> iterator([8, 14, 22]).sum()
            42
        >>> iterator(["a", "b", "c"]).sum()
            "abc"
        >>> iterator([]).sum()
            None
        """
        # built in sum cant work with str
        sum_ = None
        for x in self:
            if sum_ is None:
                sum_ = x
                continue
            sum_ += x
        return sum_

    def product(self) -> T:
        """
        Return the product of all elements in this iterator.

        Returns
        -------
        T
            The product of all elements

        Raises
        ------
        EmptyIteratorError
            If called on an empty iterator

        Examples
        --------
        >>> iterator([2, 3, 4]).product()
            24
        """
        from fluentiter.exceptions import EmptyIteratorError

        is_empty = True
        prod = 1
        for x in self:
            is_empty = False
            prod *= x  # type: ignore[operator]
        if is_empty:
            raise EmptyIteratorError("Can not calculate product of an empty iterator")
        return cast(T, prod)

    def rolling_window(self, size: int) -> "more.RollingWindowIterator[T]":
        """
        Create an iterator of overlapping windows of size `size`.

        The windows will be yielded as tuples containing the original
        iterators elements

        Notes
        -----
        Requires extra `more`

        Parameters
        ----------
        size : int
            Size of the windows

        Returns
        -------
        RollingWindowIterator[T]
            An iterator of overlapping windows

        Raises
        ------
        ValueError
            If `size` is <= 0


        Examples
        --------
        >>> iterator([2, 3, 4, 5]).rolling_window(2).to_list()
            [(2, 3), (3, 4), (4, 5)]
        """
        from fluentiter.more import RollingWindowIterator

        if size <= 0:
            raise ValueError(f"Size must be an integer >0. Got {size}")
        return RollingWindowIterator(self, size)

    def into(self, into: Callable[["FluentIterator[T]"], R]) -> R:
        """
        Turn this iterator into something else, by calling
        a function on it.

        This is very useful for collecting the iterator into
        a different kind of container, e.g. `set` or `tuple`

        Notes
        -----
        This method consumes the iterator.

        Parameters
        ----------
        into : Callable[[FluentIterator[T]], R]
            Function or type to call on this iterator

        Returns
        -------
        R
            Return value of the given function or instance
            of the given type

        Examples
        --------
        >>> iterator([2, 3, 3, 4, 5, 5]).into(set)
            {2, 3, 4, 5}
        """
        return into(self)

    def __iter__(self) -> "FluentIterator[T]":
        return self

    def __next__(self) -> T:
        x = self._infallible_next()
        if x is ITER_STOP:
            raise StopIteration
        return cast(T, x)

    def __length_hint__(self) -> int:
        size_hint = self.size_hint()
        if size_hint is not None:
            return size_hint
        return NotImplemented
