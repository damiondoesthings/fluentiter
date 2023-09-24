from fluentiter import iterator


def test_filter_map():
    my_list = ["1", "two", "NaN", "four", "5"]
    my_iter = iterator(my_list).filter_map(lambda x: int(x) if x.isdigit() else None)
    assert list(my_iter) == [1, 5]
