import hypothesis.strategies as st
import pytest
from hypothesis import given

from fluentiter import iterator
from fluentiter.exceptions import EmptyIteratorError


def test_last_list():
    assert iterator([1, 2, 3, 4, 5]).last() == 5


def test_last_generator():
    assert iterator(range(6)).last() == 5


def test_last_empty():
    with pytest.raises(EmptyIteratorError):
        iterator([]).last()


@given(st.iterables(st.integers(), min_size=1))
def test_last_fuzz(iterable):
    my_iter = iterator(iterable)
    my_iter.last()
