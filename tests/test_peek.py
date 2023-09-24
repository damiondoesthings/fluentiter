import pytest

from fluentiter import iterator


def test_peek_range():
    """
    Test we can peek an element without consuming it with a range
    """
    my_iter = iterator(range(5))
    assert my_iter.peek() == 0
    # must work multiple times
    assert my_iter.peek() == 0
    assert list(my_iter) == list(range(5))


def test_peek_list():
    """
    Test we can peek an element without consuming it with a list
    """
    my_list = list(range(5))
    my_iter = iterator(my_list)
    assert my_iter.peek() == 0
    # must work multiple times
    assert my_iter.peek() == 0
    assert list(my_iter) == list(my_list)


def test_peek_raise():
    """
    Test peek raises StopIteration
    """
    my_list = list(range(5))
    my_iter = iterator(my_list)
    _ = list(my_iter)
    with pytest.raises(StopIteration):
        my_iter.peek()
