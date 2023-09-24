from fluentiter import iterator


def test_step_by():
    assert list(iterator(list(range(10))).step_by(2)) == list(range(0, 10, 2))
