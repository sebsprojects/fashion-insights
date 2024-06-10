#!/usr/bin/python3

"""Fashion data insights. Main executable."""
import itertools
import pathlib

import config
from data_analysis import compute_average_image_count
from data_ingress import FashionDataIterator


def main():
    """Main"""
    config.configure()
    data_path = config.CONFIG["data_path"]
    data_iter = FashionDataIterator(pathlib.Path(data_path))
    avg_images = compute_average_image_count(itertools.islice(data_iter, 20))
    print(avg_images)


if __name__ == "__main__":
    main()
