from fluentiter import iterator


def test_flat_map():
    my_iter = iterator(["Hello World", "Foo Bar"]).flat_map(lambda x: x.split())
    assert list(my_iter) == ["Hello", "World", "Foo", "Bar"]


def test_flat_map_exclude():
    my_iter = iterator("FooBar").flat_map(lambda x: x.upper(), exclude=())
    assert list(my_iter) == ["F", "O", "O", "B", "A", "R"]
