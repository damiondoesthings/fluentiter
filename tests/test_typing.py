import re
from tempfile import NamedTemporaryFile

import mypy.api


def get_mypy_type(python_code: str):
    """
    Helper function, which runs the mypy on some python_code
    and returns the revealed type.

    Unlike typing.reveal_type this also shows generics
    """
    with NamedTemporaryFile(mode="w") as f:
        f.write(python_code)
        f.seek(0)
        result = mypy.api.run([f.name, "--no-color-output"])
    stdout, stderr, _ = result
    match = re.search(r'note: Revealed type is "(.*?)"', stdout)
    try:
        return match.group(1).replace("builtins.", "")
    except Exception as e:
        raise RuntimeError(f"{stderr}, {stdout}") from e


def test_type_flatten():
    code = """
from fluentiter import iterator
from fluentiter.itertypes import FlatMapIterator
reveal_type(iterator([(1,2), (3,4)]).flatten())
"""
    assert get_mypy_type(code) == "fluentiter.itertypes.FlattenIterator[int]"


def test_type_flat_map():
    code = """
from fluentiter import iterator
from fluentiter.itertypes import FlatMapIterator
reveal_type(iterator([(1,2), (3,4)]).flat_map(lambda x: x))
"""
    assert get_mypy_type(code) == "fluentiter.itertypes.FlatMapIterator[int]"


def test_tumbling_window():
    code = """
from fluentiter import iterator
from fluentiter.itertypes import FlatMapIterator
reveal_type(iterator([1,2,3]).tumbling_window(2).to_list())
"""
    assert get_mypy_type(code) == "list[tuple[int, ...]]"
