from fluentiter import iterator


def test_unzip():
    odds, evens = iterator(
        [
            (
                1,
                2,
            ),
            (3, 4),
            (5, 6),
        ]
    ).unzip()
    assert list(odds) == [1, 3, 5]
    assert list(evens) == [2, 4, 6]


def test_unequal_length():
    odds, evens = iterator([(1, 2, 4), (3, 6), (5, 8, 10, 12)]).unzip()
    assert list(odds) == [1, 3, 5]
    assert list(evens) == [(2, 4), 6, (8, 10, 12)]
