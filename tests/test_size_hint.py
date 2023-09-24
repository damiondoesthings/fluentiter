from fluentiter import iterator


def test_size_hint_list():
    assert iterator([None] * 5).size_hint() == 5


def test_size_hint_zero():
    assert iterator([]).size_hint() == 0


def test_size_hint_range():
    assert iterator(range(5)).size_hint() == 5


def test_size_hint_chain():
    assert iterator([1, 2, 3]).chain([1, 2, 3]).size_hint() == 6


def faux_generator():
    while True:
        yield None


def test_size_hint_unknown():
    assert iterator(faux_generator()).size_hint() is None
