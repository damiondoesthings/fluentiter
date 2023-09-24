"""
How to use fluentiter's `partition`function
"""
from fluentiter import iterator


def main():
    text = ["Calm down, Marty, I didn't disintegrate anything"]
    attribution = ["-", "Doc", "Brown"]
    full_text = (
        iterator(text)
        # split into words
        .flat_map(lambda s: s.split())
        .chain(attribution)
        # yes you could just call " ".join instead
        .inspect(print)
        .reduce(lambda acc, x: acc + x)
    )
    print(full_text.to_list())


if __name__ == "__main__":
    main()
