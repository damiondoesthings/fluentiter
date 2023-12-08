import hypothesis.strategies as st
import pytest
from hypothesis import given

from fluentiter import iterator
from fluentiter.exceptions import EmptyIteratorError


@given(st.lists(st.floats(allow_nan=False) | st.integers(), min_size=1))
def test_max(numberlist: list):
    true_min = min(numberlist)
    assert iterator(numberlist).min() == true_min


def test_min_empty():
    with pytest.raises(EmptyIteratorError):
        iterator([]).min()


@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1))
def test_min_key(numberlist: list):
    true_min = min(numberlist, key=lambda x: x[1])
    assert iterator(numberlist).min(key=lambda x: x[1]) == true_min
