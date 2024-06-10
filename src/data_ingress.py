#!/usr/bin/python3

"""Making data available to the program"""
import pathlib
import re
from typing import Iterator


class FashionDataPoint:
    """A data point comprising a unique id and images as raw binary data"""

    def __init__(self, uid: str, raw_image_data: list[bytes]) -> None:
        self.uid: str = uid
        self.raw_image_data: list[bytes] = raw_image_data

    def __repr__(self) -> str:
        return f"""
            FashionDataPoint with uid={self.uid}
            and {len(self.raw_image_data)} images"""

    @classmethod
    def from_file_system_directory(cls, path: pathlib.Path) -> "FashionDataPoint":
        """Creates a data point by reading from the file system
        Raises:
            FileNotFoundError
            NotADirectoryError
        """
        if not path.exists():
            raise FileNotFoundError(f"The path {path} was not found.")
        if not path.is_dir():
            raise NotADirectoryError(f"The path {path} is not a directory.")
        uid = path.name
        raw_image_data = []
        # TODO(Sebastian): Maybe this could be done in a list comprehension
        for item in path.iterdir():
            if item.is_file() and re.match(r"^image-[0-9]\.jpg", item.name):
                try:
                    raw_image_data.append(item.read_bytes())
                except Exception as err:
                    print(f"Could not read data point: {err}")
        return cls(uid, raw_image_data)


# TODO(Sebastian): The limit is not really necessary, can use islice
class FashionDataIterator:
    """An iterator that reads from data_dir_path and yields FashionDataPoints"""

    def __init__(self, data_dir_path: pathlib.Path, *, limit=-1):
        self.data_dir_path = data_dir_path
        self.limit = limit
        self.uid_iter = iter_data_point_uids(data_dir_path, limit=limit)

    def __iter__(self):
        return self

    def __next__(self) -> FashionDataPoint:
        next_uid = next(self.uid_iter)
        return FashionDataPoint.from_file_system_directory(
            pathlib.Path(self.data_dir_path, next_uid)
        )


# TODO(Sebastian): The limit is not really necessary, can use islice
def iter_data_point_uids(data_dir_path: pathlib.Path, *, limit=-1) -> Iterator[str]:
    """
    Args:
        data_dir_path: The path to the parent directory containing data points
        limit: Upper bound for the amount of data points read.
            A value of -1 means no upper bound
    """
    count = 0
    for item in data_dir_path.iterdir():
        if item.is_dir() and (limit < 0 or 0 <= count <= limit):
            count += 1
            yield item.name
