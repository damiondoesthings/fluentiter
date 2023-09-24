from unittest.mock import MagicMock

from fluentiter import iterator


def test_map_simple():
    my_list = [False] * 10
    my_iter = iterator(my_list).map(lambda x: not x)
    assert all(my_iter)


def test_map_is_lazy():
    my_gen = MagicMock()
    my_list = [my_gen] * 3
    my_iter = iterator(my_list).map(lambda x: x())

    my_gen.assert_not_called()
    for _ in my_iter:
        break
    my_gen.assert_called_once()
