#!/usr/bin/python3

"""Read a config file and provide it as the CONFIG constant"""

import configparser
import json
import os
import pathlib
import sys
from typing import Any

CONFIG_ENV_KEY: str = "CONFIG_PATH"
CONFIG: dict[str, Any] = {}


# TODO(Sebastian): Document raises
def read_config_as_ini(config_contents: str) -> dict[str, Any]:
    """Try parsing config_contents as a INI"""
    config = configparser.ConfigParser()
    config.read_string(config_contents)
    # Expected is a single section "fashion_data" that is transformed into a flat dict
    flat_dict = {}
    for key in config["fashion_data"].keys():
        flat_dict[key] = config["fashion_data"][key]
    return flat_dict


# TODO(Sebastian): Document raises
def read_config_as_json(config_contents: str) -> dict[str, Any]:
    """Try parsing config_contents as a JSON"""
    config = json.loads(config_contents)
    return config


def read_config_from_file(config_path: str) -> dict[str, Any]:
    """Read the config file and parse it either as a INI or JSON if possible
    Raises:
        FileNotFoundError
        ValueError
    """
    try:
        with open(config_path, encoding="utf-8") as config_file:
            config_contents = config_file.read()
    except FileNotFoundError as err:
        raise FileNotFoundError(
            f"File at {config_path} (from ENV {CONFIG_ENV_KEY}) not found"
        ) from err
    file_extension = pathlib.Path(config_path).suffix
    if file_extension == ".ini":
        return read_config_as_ini(config_contents)
    if file_extension == ".json":
        return read_config_as_json(config_contents)
    raise ValueError(
        f"""Config file ends in {file_extension}.
        Only .ini and .json are supported."""
    )


def read_config_from_cmd() -> dict[str, Any]:
    """Try to read the config file from a path provided as CMD arg
    Raises:
        RuntimeError
    """
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        return read_config_from_file(config_path)
    raise RuntimeError("Config file path was not provided as a CMD arg")


def read_config_from_env() -> dict[str, Any]:
    """Try to read the config file from a path provided in ENV
    Raises:
        RuntimeError
    """
    try:
        config_path = os.environ[CONFIG_ENV_KEY]
        return read_config_from_file(config_path)
    except Exception as err:
        raise RuntimeError(
            f"{CONFIG_ENV_KEY} is not among environment variables"
        ) from err


def read_config() -> dict[str, Any]:
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
    raise RuntimeError("Failed to read config from all sources (ENV and CMD)")


def configure() -> None:
    """
    Configure the config module: Load the config by reading a
    config file from ENV or CMD. This should be called exactly once at program
    start
    Raises:
        RuntimeError
    """
    global CONFIG
    if not CONFIG:
        CONFIG = read_config()
