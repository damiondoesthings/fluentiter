from fluentiter import iterator


def test_skip():
    my_iter = iterator([-1, 0, 2, -2]).skip(2)
    assert list(my_iter) == [2, -2]
