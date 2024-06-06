#!/usr/bin/python3

"""Making data available to the program"""
import pathlib
import re


class FashionDataPoint:
    """A data point comprising a unique id and images as raw binary data"""
    def __init__(self, uid: str, raw_image_data: list[bytes]) -> None:
        self.uid = uid
        self.raw_image_data: raw_image_data

    def __repr__(self) -> str:
        return f"""
            FashionDataPoint with uid={self.uid}
            and {len(self.raw_image_data)} images"""

    @classmethod
    def from_file_system_directory(
            cls,
            path: pathlib.Path
    ) -> "FashionDataPoint":
        """Creates a data point by reading from the file system
        Raises:
            FileNotFoundError
            NotADirectoryError
        """
        if not path.exists():
            raise FileNotFoundError(f'The path {path} was not found.')
        if not path.is_dir():
            raise NotADirectoryError(f'The path {path} is not a directory.')
        uid = path.name
        raw_image_data = []
        for item in path.iterdir():
            if item.is_file() and re.match(r'^image-[0,9]\.jpg', item.name):
                try:
                    raw_image_data.append(item.read_bytes())
                except Exception as e:
                    print(f'Could not read data point: {e}')
        return cls(uid, raw_image_data)


def list_data_point_uids(path: pathlib.Path, *, limit=-1) -> list[str]:
    """
    Args:
        path: The path to the parent directory containing data points
        limit: Upper bound for the amount of data points read.
            A value of -1 means no upper bound
    """
    data_point_uids = []
    for item in path.iterdir():
        if item.is_dir():
            data_point_uids.append(item.name)
        if 0 <= limit <= len(data_point_uids):
            return data_point_uids
