import sys

import hypothesis.strategies as st
import pytest
from hypothesis import given

from fluentiter import iterator

from .fuzz import st_iterables


@given(st_iterables, st.integers(min_value=0, max_value=sys.maxsize))
def test_nth_fuzz(iterable, index):
    try:
        iterator(iterable).nth(index)
    except IndexError:
        pass


def test_nth_negative():
    with pytest.raises(ValueError):
        iterator([1, 2, 3]).nth(-1)


def test_nth_no_rewind():
    my_iter = iterator(list(range(3)))

    assert my_iter.nth(0) == 0
    assert my_iter.nth(0) == 1
    assert my_iter.nth(0) == 2
    with pytest.raises(IndexError):
        my_iter.nth(0)


def test_nth_out_of_range():
    with pytest.raises(IndexError):
        iterator([1, 2, 3]).nth(3)
