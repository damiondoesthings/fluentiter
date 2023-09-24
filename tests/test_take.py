from fluentiter import iterator


def test_take():
    my_iter = iterator([-1, 0, 2, -2]).take(2)
    assert list(my_iter) == [-1, 0]
