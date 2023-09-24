import hypothesis.strategies as st
from hypothesis import given

from fluentiter import iterator

from .fuzz import st_iterables


@given(st_iterables)
def test_next_fuzz(iter_obj):
    my_iter = iterator(iter_obj)
    for _ in my_iter:
        pass


@given(st.lists(st.integers(), min_size=1))
def test_next_lists(test_list):
    my_iter = iterator(test_list)
    for i in range(len(test_list)):
        assert test_list[i] == my_iter.next()


@given(st.lists(st.integers()))
def test_iter_protocol(test_list):
    my_iter = iterator(test_list)
    for i, e in enumerate(my_iter):
        assert e == test_list[i]
