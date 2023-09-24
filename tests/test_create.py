from fluentiter import FluentIterator, iterator


def test_iterator_from_list():
    x = [1, 2, 3, 4, 5]
    my_iter = iterator(x)
    assert isinstance(my_iter, FluentIterator)


def test_iterator_from_generator():
    x = range(20)
    my_iter = iterator(x)
    assert isinstance(my_iter, FluentIterator)
