from fluentiter import iterator


def test_to_list():
    my_iter = iterator(range(10))

    assert list(range(10)) == my_iter.to_list()
