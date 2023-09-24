from fluentiter import iterator


def test_zip():
    list_a = [1, 3, 5, 7]
    list_b = [2, 4, 6, 8]
    expected = zip(list_a, list_b)
    result = iterator(list_a).zip(list_b)
    assert list(expected) == list(result)

    # reverse
    list_a = [1, 3, 5, 7]
    list_b = [2, 4, 6, 8]
    expected = zip(list_b, list_a)
    result = iterator(list_b).zip(list_a)
    assert list(expected) == list(result)
