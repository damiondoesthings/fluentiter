from fluentiter import iterator


def test_any_true():
    """
    Check true case
    """
    assert iterator(range(10)).any(lambda x: x == 5)


def test_any_false():
    """
    Check false case
    """
    assert not iterator(range(10)).any(lambda _: False)
    assert not iterator([]).any(lambda _: True)
