import hypothesis.strategies as st
import pytest
from hypothesis import given

from fluentiter import iterator
from fluentiter.exceptions import EmptyIteratorError


@given(st.lists(st.floats(allow_nan=False) | st.integers(), min_size=1))
def test_max(numberlist: list):
    true_max = max(numberlist)
    assert iterator(numberlist).max() == true_max


def test_max_empty():
    with pytest.raises(EmptyIteratorError):
        iterator([]).max()


@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1))
def test_max_key(numberlist: list):
    true_max = max(numberlist, key=lambda x: x[1])
    assert iterator(numberlist).max(key=lambda x: x[1]) == true_max
