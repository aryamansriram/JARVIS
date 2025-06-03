"""
This module provides tools for file and directory operations within the software factory.

Functions:
- create_directory: Creates a directory at the specified path.
- delete_directory: Deletes a directory at the specified path.
- create_file_with_code: Creates a file and writes code to it.
- read_file: Reads the contents of a file.
- delete_file: Deletes a file.
- run_terminal_command: Executes a terminal command.
"""

import os
from langchain_core.tools import tool
from loguru import logger


@tool
def create_directory(path_to_directory: str):
    """
    Creates a directory at the specified path
    """
    os.makedirs(path_to_directory, exist_ok=True)
    logger.info(f"Created directory at {path_to_directory}")


@tool
def delete_directory(path_to_directory: str):
    """
    Deletes a directory at the specified path
    """
    os.rmdir(path_to_directory)
    logger.info(f"Deleted directory at {path_to_directory}")


@tool
def create_file_with_code(path_to_file: str, code: str):
    """
    Creates a file at the specified path and writes the specified code to it
    """
    with open(path_to_file, "w") as f:
        f.write(code)
    logger.info(f"Created file at {path_to_file}")


@tool
def read_file(path_to_file: str):
    """
    Reads the file at the specified path and returns its contents
    """
    with open(path_to_file, "r") as f:
        return f.read()
    logger.info(f"Read file at {path_to_file}")


@tool
def delete_file(path_to_file: str):
    """
    Deletes the file at the specified path
    """
    os.remove(path_to_file)
    logger.info(f"Deleted file at {path_to_file}")


@tool
def run_terminal_command(command: str):
    """
    Runs the specified terminal command
    For example, to run a python file: run_terminal_command("python file.py")
    For example, to run a node package: run_terminal_command("npx dev")
    Or to install a package: run_terminal_command("pip install package_name")
    """
    os.system(command)
    logger.info(f"Ran command: {command}")
