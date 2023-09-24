"""
Fluentiter makes parsing lines in a file much more fun
"""
import requests

from fluentiter import iterator


def with_fluentiter(raw_data: str) -> None:
    """
    Process the data using fluentiter
    """
    lines = iterator(raw_data.split("\n"))
    header = [x for x in lines.next().split(",") if x.strip(" ")]
    bielefeld = (
        lines.map(lambda line: line.split(","))
        .map(lambda values: {k: v for k, v in zip(header, values)})
        .filter(lambda value_dct: value_dct["country"] == "Germany")
        .find(lambda value_dct: value_dct["name"] == "Bielefeld")
    )
    print(f"Bielefeld is in {bielefeld['subcountry']}")


def without_fluentiter(raw_data: str) -> None:
    """
    Process the data without using fluentiter, but with map/filter
    """
    lines = iter(raw_data.split("\n"))
    header = [x for x in next(lines).split(",") if x.strip()]
    bielefeld = next(
        filter(
            lambda value_dct: value_dct["name"] == "Bielefeld",
            filter(
                lambda value_dct: value_dct["country"] == "Germany",
                map(
                    lambda values: {k: v for k, v in zip(header, values)},
                    map(lambda line: line.split(","), lines),
                ),
            ),
        )
    )
    print(f"Bielefeld is in {bielefeld['subcountry']}")


def abomination(raw_data: str) -> None:
    """
    Process the data without using fluentiter, but with expressions
    """
    lines = iter(raw_data.split("\n"))
    header = [x for x in next(lines).split(",") if x.strip()]
    # Good luck figuring out this kind of code in the wild
    bielefeld = next(
        (
            value_dct2
            for value_dct2 in (
                value_dct
                for value_dct in (
                    {k: v for k, v in zip(header, values)}
                    for values in (line.split(",") for line in lines)
                )
                if value_dct["country"] == "Germany"
            )
            if value_dct2["name"] == "Bielefeld"
        )
    )
    print(f"Bielefeld is in {bielefeld['subcountry']}")


if __name__ == "__main__":
    # the csv header is "name,country,subcountry,geonameid"
    raw_data = requests.get(
        "https://github.com/datasets/world-cities/blob/master/data/world-cities.csv"
    ).text

    with_fluentiter(raw_data)
    without_fluentiter(raw_data)
    abomination(raw_data)
