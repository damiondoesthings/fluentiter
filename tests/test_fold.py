from fluentiter import iterator


def test_fold():
    assert iterator(["hot", "dog", "bun"]).fold(1, lambda a, x: a + len(x)) == 10
