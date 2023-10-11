from typing import Any, Callable, Iterable, List

import hypothesis.strategies as st
from hypothesis import given

from fluentiter import iterator


@given(st.lists(st.integers()), st.sampled_from((list, set, tuple)))
def test_into(inp: List[int], container: Callable[[Iterable[int]], Any]):
    it = iterator(inp)
    assert it.into(container) == container(inp)
