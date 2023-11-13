import pytest

from fluentiter import iterator


def test_tumbling_simple():
    my_iter = iterator(range(9)).tumbling_window(3)
    assert list(my_iter) == [(0, 1, 2), (3, 4, 5), (6, 7, 8)]


def test_tumbling_too_short():
    my_iter = iterator(range(8)).tumbling_window(3)
    assert list(my_iter) == [(0, 1, 2), (3, 4, 5), (6, 7)]

    my_iter = iterator(range(2)).tumbling_window(3)
    assert list(my_iter) == [
        (
            0,
            1,
        )
    ]


def test_raises_min_size():
    with pytest.raises(ValueError):
        iterator(range(8)).tumbling_window(-1)
    with pytest.raises(ValueError):
        iterator(range(8)).tumbling_window(0)
