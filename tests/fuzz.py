import hypothesis.strategies as st

# a big variety of python types, which could be in iterables
_elements = st.deferred(
    lambda: (
        st.binary()
        | st.booleans()
        | st.text()
        | st.integers()
        | st.dictionaries(st.integers(), _elements)
        | st.tuples(_elements)
        | st.functions()
    )
)

st_iterables = st.iterables(_elements)
