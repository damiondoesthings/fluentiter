from fluentiter import iterator


def test_skip_while():
    my_iter = iterator([-1, 0, 2, -2]).skip_while(lambda x: x < 0)
    assert list(my_iter) == [0, 2, -2]
