from fluentiter import iterator


def test_enumerate():
    my_list = [1, 2, 3, 4, 5]
    result = list(iterator(my_list).enumerate())
    expected = list(enumerate(my_list))
    assert result == expected
