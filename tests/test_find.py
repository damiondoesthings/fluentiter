import pytest

from fluentiter import iterator
from fluentiter.exceptions import NotFoundError


def test_find():
    """
    Check find returns the first match
    """
    assert iterator(range(10)).find(lambda x: x > 2) == 3


def test_find_no_match():
    """
    Check NotFoundError is raised if no element matches
    """
    with pytest.raises(NotFoundError):
        assert iterator(range(10)).find(lambda _: False)
    with pytest.raises(NotFoundError):
        assert iterator([]).find(lambda _: False)
    with pytest.raises(NotFoundError):
        assert iterator([]).find(lambda _: True)
