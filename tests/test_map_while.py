from fluentiter import iterator


def test_map_while():
    my_iter = iterator([-1, 0, 2, -2]).map_while(lambda x: x if x < 2 else None)
    assert list(my_iter) == [-1, 0]
