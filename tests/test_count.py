import hypothesis.strategies as st
from hypothesis import given

from fluentiter import iterator


def sized_iterables(elements: st.SearchStrategy) -> st.SearchStrategy:
    return st.lists(elements) | st.tuples(elements) | st.sets(elements)


@given(sized_iterables(st.booleans()))
def test_count(iter_obj):
    assert iterator(iter_obj).count() == len(iter_obj)
