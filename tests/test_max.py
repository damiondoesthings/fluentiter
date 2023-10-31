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