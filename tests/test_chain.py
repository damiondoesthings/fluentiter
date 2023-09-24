from fluentiter import iterator


def test_chain_list():
    list_a = [1, 2, 3]
    list_b = [4, 5, 6]
    my_iter = iterator(list_a).chain(list_b)
    assert list(my_iter) == list_a + list_b

    my_iter = iterator(list_b).chain(list_a)
    assert list(my_iter) == list_b + list_a


def faux_generator():
    while True:
        yield None


def test_chain_length_hint():
    list_a = [1, 2, 3]
    list_b = [4, 5, 6]
    my_iter = iterator(list_a).chain(list_b)
    assert my_iter.size_hint() == 6

    my_iter = iterator([]).chain([])
    assert my_iter.size_hint() == 0

    my_iter = iterator(faux_generator()).chain([])
    assert my_iter.size_hint() is None
    my_iter = iterator([]).chain(faux_generator())
    assert my_iter.size_hint() is None
