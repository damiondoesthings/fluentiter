from unittest.mock import Mock

from fluentiter import iterator


def test_insepct():
    func = Mock()
    my_list = [0, 1, 2, 3, 4]
    my_iter = iterator(my_list).inspect(func)

    assert list(my_iter) == my_list
    assert [x.args[0] for x in func.call_args_list] == my_list
