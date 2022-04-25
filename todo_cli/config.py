"""This module provides the To-Do config functionality"""
# todo_cli/config.py

import configparser
from pathlib import Path
import typer
from todo_cli import (
    DB_WRITE_ERROR,
    DIR_ERROR,
    FILE_ERROR,
    SUCCESS,
    __app_name__
)
# /Users/ezracitron/Library/Application Support/todo-CLI
CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
# Path objecst must override the '/' and add it onto path
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"


def init_app(db_path: str) -> int:
    """Initialise the application."""
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code
    database_code = _create_database(db_path)
    if database_code != SUCCESS:
        return database_code
    return SUCCESS


def _init_config_file() -> int:
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError as e:
        return e
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError as e:
        return e
    return SUCCESS


def _create_database(db_path: str) -> int:
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"database": db_path}
    try:
        with CONFIG_FILE_PATH.open('w') as f:
            config_parser.write(f)
    except OSError:
        return DB_WRITE_ERROR
    return SUCCESS
