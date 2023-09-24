from fluentiter import iterator


def test_partition():
    my_iter = iterator(range(10))

    evens, odds = my_iter.partition(lambda x: bool(x & 1))
    assert list(odds) == [1, 3, 5, 7, 9]
    assert list(evens) == [0, 2, 4, 6, 8]
