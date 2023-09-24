from fluentiter import iterator


def test_filter():
    my_list = [1, 2, 3, 4, 5]

    def is_odd(i):
        return bool(i & 1)

    my_iter = iterator(my_list).filter(is_odd)
    assert list(my_iter) == [1, 3, 5]


def test_chain_filter():
    my_list = [1, 2, 3, 4, 5]

    def is_odd(i):
        return bool(i & 1)

    my_iter = iterator(my_list).chain([6, 7, 8, 9]).filter(is_odd)
    assert list(my_iter) == [1, 3, 5, 7, 9]
