import sys

import hypothesis.strategies as st
import pytest
from hypothesis import given

from fluentiter import iterator

from .fuzz import st_iterables


def test_rolling_window():
    rolled = list(iterator(range(5)).rolling_window(2))
    assert rolled == [(0, 1), (1, 2), (2, 3), (3, 4)]


@given(st_iterables, st.integers(min_value=1, max_value=sys.maxsize))
def test_rolling_window_fuzz(it, size):
    collected = []
    for x in iterator(it).rolling_window(size):
        assert isinstance(x, tuple)
        assert len(x) == size
        collected.append(x)


def test_rolling_window_valueerror():
    with pytest.raises(ValueError):
        iterator(range(5)).rolling_window(0)
    with pytest.raises(ValueError):
        iterator(range(5)).rolling_window(-1)
