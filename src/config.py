#!/usr/bin/python3

"""Read a config file and provide it as the CONFIG constant"""

import os
import configparser
import json
import sys
from pathlib import Path


CONFIG_ENV_KEY: str = "CONFIG_PATH"
CONFIG: dict[str, any] = dict()


def read_config_as_ini(config_contents: str) -> dict[str, any]:
    config = configparser.ConfigParser()
    config.read_string(config_contents)
    # TODO(Sebastian): convert the dict-like with sections into a flat normal dict
    return config


def read_config_as_json(config_contents: str) -> dict[str, any]:
    config = json.loads(config_contents)
    return config


# The following has issues with no-extension paths and double extension paths such as file.tar.gz
# file_extension = config_path.split(".")[-1]
# Using the os module:
# file_extension = os.path.splitext()[1]
# Using the pathlib module:
def read_config_from_file(config_path: str) -> dict[str, any]:
    """Read the config file and parse it either as a INI or JSON if possible
    Raises:
        FileNotFoundError
        ValueError
    """
    try:
        with open(config_path) as config_file:
            config_contents = config_file.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f'File at {config_path} (from ENV {CONFIG_ENV_KEY}) not found') from e
    file_extension = Path(config_path).suffix
    if file_extension == ".ini":
        return read_config_as_ini(config_contents)
    elif file_extension == ".json":
        return read_config_as_json(config_contents)
    else:
        raise ValueError(f'Config file ends in {file_extension}. Only .ini and .json are supported.')


def read_config_from_cmd() -> dict[str, any]:
    """Try to read the config file from a path provided as CMD arg
    Raises:
        RuntimeError
    """
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        return read_config_from_file(config_path)
    else:
        raise RuntimeError('Config file path was not provided as a CMD arg')


def read_config_from_env() -> dict[str, any]:
    """Try to read the config file from a path provided in ENV
    Raises:
        RuntimeError
    """
    try:
        config_path = os.environ[CONFIG_ENV_KEY]
        return read_config_from_file(config_path)
    except Exception as e:
        raise RuntimeError(f'{CONFIG_ENV_KEY} is not among environment variables') from e


def read_config() -> dict[str, any]:
    """Read the config from a path provided either as ENV variable or CMD arg
    Raises:
        RuntimeError
    """
    config_loaders = [read_config_from_env, read_config_from_cmd]
    for loader in config_loaders:
        try:
            config = loader()
            return config
        except RuntimeError:
            # TODO(Sebastian): perhaps log that this didn't work
            pass
    raise RuntimeError('Failed to read config from all sources (ENV and CMD)')


def configure() -> None:
    """Configure the config module: Load the config by reading a config file from ENV or CMD
    Raises:
        RuntimeError
    """
    global CONFIG
    CONFIG = read_config()
