from fluentiter import iterator


def test_position():
    """
    Check position returns the correct index
    """
    assert iterator(range(10)).position(lambda x: x == 4) == 4


def test_position_no_match():
    """
    Check `-1` is returned if no element matches
    """
    assert iterator(range(10)).position(lambda _: False) == -1
    assert iterator([]).position(lambda _: False) == -1
    assert iterator([]).position(lambda _: True) == -1
