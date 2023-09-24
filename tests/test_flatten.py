from typing import List, Union

from fluentiter import iterator


def test_flatten():
    my_list: List[Union[int, List[int]]] = [1, 2, [3, 4, 5]]

    my_iter = iterator(my_list)
    flattened = my_iter.flatten()
    assert list(flattened) == [1, 2, 3, 4, 5]


def test_flatten_str():
    my_list = ["hello"]

    my_iter = iterator(my_list)
    flattened = my_iter.flatten(exclude=())
    assert list(flattened) == ["h", "e", "l", "l", "o"]


def test_flatten_str_exclude():
    my_list = ["hello"]

    my_iter = iterator(my_list)
    flattened = my_iter.flatten()
    assert list(flattened) == ["hello"]
