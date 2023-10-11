# FluentIter

Nicer iterator patterns for Python! Chain map, filter, zip, unzip, cycle, skip and scan like
there is no tomorrow.

Install with

```bash
pip install fluentiter
```

[Straight to the API docs 👉](https://damiondoesthings.github.io/fluentiter/api)

## TLDR:

With **fluentiter** you can do this

```python
lines = iterator(haystack_csv.split("\n"))
header = [x for x in lines.next().split(",") if x.strip(" ")]
needle = (
    lines.map(lambda line: line.split(","))
    .map(lambda values: {k: v for k, v in zip(header, values)})
    .filter(lambda value_dct: value_dct["material"] != "hay")
    .find(lambda value_dct: value_dct["type"] == "needle")
)
```

instead of this

```python
lines = iter(some_csv.split("\n"))
header = [x for x in next(lines).split(",") if x.strip()]
needle = next(
    filter(
        lambda value_dct: value_dct["material"] != "hay",
        filter(
            lambda value_dct: value_dct["type"] == "needle",
            map(
                lambda values: {k: v for k, v in zip(header, values)},
                map(lambda line: line.split(","), lines),
            ),
        ),
    )
)
```

See the [this example](https://github.com/damiondoesthings/fluentiter/blob/main/examples/parsing.py) for a more complete version.

## Motivation

To me Pythons iterator functions (i.e. `map`, `filter`, `zip`, etc.) always seemed backward.
While generator expressions and list/dict/set comprehensions give you nice left-to-right readability,
`map` and `filter` force you to read "inside-out":

```python
[func(x) for x in something if x == y]
map(func, filter(lambda x: x == y, something))
```

This is not an issue for short an simple statements, as they can be written concisely using expressions, but chaining multiple operations,
will result in either many intermediate variable assignements or serious spaghettification.

## How to use

Any `Iterable` can be turned into a `FluentIterator` by just passing it to the `iterator` function:

```python
from fluentiter import iterator
bugs = ["john", "paul", "ringo", "george"]

fluent = iterator(bugs)
# you can now do
# fluent.map(...).filter(...).cycle(...).scan(...) and so on
```

The `FluentIterator` provides a rich set of methods you can call **and chain together** to your liking:

Of course there are the classic `map`, `filter`, and `reduce` functions, but also some more really useful features like `cycle` to repeat an iterator forever, `find` to find an element or even `partition` to turn your iterator into two.

In total `FluentIterator` provides **35** methods to compose beautiful and easy to follow iteration
patterns.
Check the [API docs](https://damiondoesthings.github.io/fluentiter/) to see them all.

## Features

- 36 cool fresh iterator methods
- 100% Type annotated e.g. `iterator(["foo", "bar"]).map(len).to_list()` gets correctly inferred as `list[int]`
- 100% Test coverage
- 0 dependencies outside the Python standard library[^0]

## Contributing

The simplest way to contribute is to open an issue. If you would like to see some feature implemented or
found a bug, head over to [the issues section](https://github.com/damiondoesthings/fluentiter/issues).

## Developing

1. Clone the repository
2. Install [Poetry](https://python-poetry.org/)
3. Install development dependencies with `poetry install`
4. Enter the poetry shell with `poetry shell`

## Guidelines

Your PR should include relevant tests for the changes you are contributing and be fully type annotated.
If you are unsure or stuck, please open the PR anyway and we can work it out together.

By opening a PR you agree to your code becoming part of the fluentiter package and being published
under fluentiters license.

## Running formatting, tests, and linting

- Formatting: `poe format`
- Linting: `poe lint`
- Tests: `poe test`

All of the above: `poe all`

### Viewing the coverage report

Running `coverage html` will create a file `htmlcov/index.html` you can open to view the test coverage report

## Changelog

+ 1.0.0
    + initial release
+ 1.0.1
    + fixed errors int readme
+ 1.1.0
    + added `into(...)` method

## Special Thanks

Thank you to all Rust maintainers for creating the [Iterator trait](https://doc.rust-lang.org/std/iter/trait.Iterator.html), which served as the main source of inspiration.

[^0]: Some functions may require the `more` extra which has [more-itertools](https://github.com/more-itertools/more-itertools) as a dependency