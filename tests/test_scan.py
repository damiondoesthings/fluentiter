from fluentiter import iterator
from fluentiter.exceptions import StopScan  # noqa: F401


def test_scan():
    """
    Make fun fibonacci numbers
    """
    result = list(
        iterator(range(10)).scan(
            initial_state=(0, 0), func=lambda s, x: ((s[1], sum(s) or x), sum(s) or x)
        )
    )
    assert result == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_scan_end_iteration():
    """
    Test we can prematurely end the iteration in scan
    """
    result = list(
        iterator(range(10)).scan(
            0, lambda s, x: (x, x) if x < 5 else exec("raise StopScan")
        )
    )
    assert result == [0, 1, 2, 3, 4]
