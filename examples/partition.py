"""
How to use fluentiter's `partition`function
"""
from fluentiter import iterator


def main():
    text = ["Calm down, Marty, I didn't disintegrate anything"]
    odd_len, even_len = (
        iterator(text)
        # split into words
        .flat_map(lambda s: s.split())
        # remove the commas
        .map(lambda s: s.replace(",", ""))
        # separate by character count
        .partition(lambda x: bool(len(x) & 1))
    )
    print(odd_len.to_list())
    print(even_len.to_list())


if __name__ == "__main__":
    main()
