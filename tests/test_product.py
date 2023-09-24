import math

import hypothesis.strategies as st
import pytest
from hypothesis import given

from fluentiter import iterator
from fluentiter.exceptions import EmptyIteratorError


@given(st.lists(st.integers(), min_size=1))
def test_product(numberlist: list):
    true_prod = 1
    for x in numberlist:
        true_prod *= x
    assert iterator(numberlist).product() == true_prod


def test_product_empty():
    with pytest.raises(EmptyIteratorError):
        iterator([]).product()


def test_product_inf():
    assert math.isnan(iterator([float("inf"), 0]).product())
