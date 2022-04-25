"""This module provides the todo database functionality"""
# todo_cli/database.py

import json
import configparser
from pathlib import Path 
from todo_cli import DB_WRITE_ERROR, SUCCESS
from typing import Any, Dict, List, NamedTuple
from todo_cli import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR,SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "."+Path.home().stem +"_todo.json"
)

def get_database_path(config_file: Path)->Path:
    """Return the current path to the todo database"""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path:Path)-> int:
    """Create todo database"""
    try:
        db_path.write_text("[]") # empty todo
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR
    
class DBResponce(NamedTuple):
    todo_list: List[Dict[str,Any]]
    error: int

class DatabaseHandler:
    def __init__(self,db_path: Path) -> None:
        self._db_path = db_path
    
    def read_todos(self)-> DBResponce:
        try:
            with self._db_path.open('r') as db:
                try:
                    return DBResponce(json.load(db),SUCCESS)
                except json.JSONDecodeError:
                    return DBResponce([],JSON_ERROR)
        except OSError:
            return DBResponce([],DB_READ_ERROR)

    def write_todos(self, todo_list: list[Dict[str,Any]])-> DBResponce:
        try:
            with(self._db_path.open('w')) as db:
                json.dump(todo_list,db,indent=4)
            return DBResponce(todo_list,SUCCESS)
        except OSError:
            return DBResponce(todo_list,DB_WRITE_ERROR)
