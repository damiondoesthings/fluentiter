import math

import hypothesis.strategies as st
from hypothesis import given

from fluentiter import iterator


@given(
    st.lists(
        st.floats(allow_nan=False, allow_infinity=False) | st.integers(), min_size=1
    )
)
def test_sum(numberlist: list):
    true_sum = sum(numberlist)
    assert iterator(numberlist).sum() == true_sum


def test_sum_empty():
    iterator([]).sum() is None


def test_sum_inf():
    assert math.isnan(iterator([float("inf"), float("-inf")]).sum())


@given(st.lists(st.text(), min_size=1))
def test_sum_str(strlist):
    true_sum = "".join(strlist)
    iterator(strlist).sum() == true_sum
