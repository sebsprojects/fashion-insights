#!/usr/bin/python3

"""Fashion data insights. Main executable."""
import pathlib

import config
import data_ingress


def main():
    config.configure()
    data_path = config.CONFIG['data_path']
    print(data_ingress.list_data_point_uids(pathlib.Path(data_path), limit=20))


if __name__ == "__main__":
    main()
