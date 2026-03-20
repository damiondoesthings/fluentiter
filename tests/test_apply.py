from typing import Any, Callable, Iterable, List

import hypothesis.strategies as st
from hypothesis import given

from fluentiter import FluentIterator, iterator

@given(st.lists(st.integers()), st.sampled_from((set, list, tuple)))
def test_apply(inp: List[int], container: Callable[[Iterable[int]], Any]):
    """Test that apply works like into but returns a FluentIterator"""
    it = iterator(inp)
    result = it.apply(container)
    assert isinstance(result, FluentIterator)

@given(st.lists(st.integers()))
def test_apply_chaining(inp: List[int]):
    """Test that apply allows for chaining operations"""
    it = iterator(inp)
    result = it.apply(set).map(lambda x: x * 2).to_list()
    expected = [x * 2 for x in set(inp)]
    assert sorted(result) == sorted(expected)

@given(st.lists(st.integers()))
def test_apply_empty(inp: List[int]):
    """Test that apply works with empty iterators"""
    it = iterator([])
    result = it.apply(list)
    assert result.to_list() == []

def test_apply_example():
    """Test the example from the docstring"""
    result = iterator([2, 3, 3, 4, 5, 5]).apply(set).map(lambda x: x * 2).to_list()
    assert sorted(result) == [4, 6, 8, 10]