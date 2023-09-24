from fluentiter import iterator


def test_take_while():
    my_iter = iterator([-1, 0, 2, -2]).take_while(lambda x: x < 2)
    assert list(my_iter) == [-1, 0]
