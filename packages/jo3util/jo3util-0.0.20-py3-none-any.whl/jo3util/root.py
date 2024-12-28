#! /usr/bin/env python3

import inspect
import os
import json
from importlib.resources import files, as_file
from pathlib import Path
from typing import Optional, Union

import __main__
from .string import hash_string
from .warning import todo


def walk_stack() -> Optional[Path]:
    todo("check if this is being called from the python shell")
    stack = inspect.stack()
    i = 0
    file_name = "<>"
    while -i <= len(stack) and file_name[0] == "<" and file_name[-1] == ">":
        i -= 1
        file_name = stack[i].filename

    if file_name[0] == "<" and file_name[-1] == ">":
        return None
    return Path(file_name)


def root_dir() -> Path:
    if "FILE_PATH" in os.environ:
        return Path(os.environ["FILE_PATH"]).parent

    if __main__.__package__:
        with as_file(files(__main__.__package__)) as path:
            return path

    if "__file__" in dir(__main__):
        return Path(__main__.__file__).parent

    # Find the path of the ipython notebook.
    try:
        get_ipython()
        import ipynbname

        return ipynbname.path().parent
    except (NameError, IndexError):
        pass

    out = walk_stack()
    if out:
        return out.parent

    return Path(os.path.abspath("."))


def root_file():
    if "FILE_PATH" in os.environ:
        return Path(os.environ["FILE_PATH"])

    if "FILE_NAME" in os.environ:
        return root_dir() / os.environ["FILE_NAME"]

    if __main__.__package__:
        return files(__main__.__package__).joinpath("__main__.py")

    if "__file__" in dir(__main__):
        return Path(__main__.__file__)

    try:
        get_ipython()
        import ipynbname

        return ipynbname.path()
    except (NameError, IndexError):
        pass

    out = walk_stack()
    if out:
        return out

    raise NotImplementedError


def run_dir(
    obj,
    root: Union[Path, str] = root_dir() / "run",
    name_len=8
):
    obj_hash: str = hash_string(json.dumps(
        obj,
        default=lambda x: vars(x) if hasattr(x, "__dict__") else str(x)
    ))[:name_len]
    return root / Path(obj_hash)
