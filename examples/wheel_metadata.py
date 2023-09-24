"""
Getting the METADATA from a Python wheel (.whl) file.
"""
import zipfile

from fluentiter import iterator


def main():
    with zipfile.ZipFile("path_to_wheel", mode="r") as whl_file:
        # this is how you might do it in plain python
        next(
            map(
                lambda x: x.filename,
                filter(
                    lambda x: x.filename.endswith(
                        ".dist-info/METADATA", whl_file.filelist
                    )
                ),
            )
        )
        # how to do it with fluentiter
        (
            iterator(whl_file.filelist)
            .filter(lambda x: x.filename.endswith(".dist-info/METADATA"))
            .map(lambda x: x.filename)
            .first()
        )
