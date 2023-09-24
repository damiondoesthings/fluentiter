from hypothesis import given

from fluentiter import FluentIterator, iterator

from .fuzz import st_iterables


def test_cycle_list():
    fluent = iterator([0, 1, 2]).cycle()
    assert isinstance(fluent, FluentIterator)
    collected = []
    for i in range(9):
        collected.append(fluent.next())
    assert collected == [0, 1, 2, 0, 1, 2, 0, 1, 2]


def test_cycle_range():
    fluent = iterator(range(3)).cycle()
    assert isinstance(fluent, FluentIterator)
    collected = []
    for i in range(9):
        collected.append(fluent.next())
    assert collected == [0, 1, 2, 0, 1, 2, 0, 1, 2]


@given(st_iterables)
def test_cycle_fuzz(it):
    fluent = iterator(it).cycle()
    assert isinstance(fluent, FluentIterator)
    # iterate a bit for testing
    for i, _ in enumerate(fluent):
        if i > 2:
            break
