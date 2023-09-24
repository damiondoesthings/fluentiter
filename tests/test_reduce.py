import pytest

from fluentiter import iterator
from fluentiter.exceptions import EmptyIteratorError


def test_reduce():
    """
    Sum up all numbers
    """
    inp = range(10)
    result = iterator(inp).reduce(lambda x, y: x + y)
    assert result == sum(inp)


def test_reduce_empty():
    with pytest.raises(EmptyIteratorError):
        iterator([]).reduce(lambda x, y: x + y)
