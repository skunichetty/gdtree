"""
A set of smaller (but important) utility constants, functions, and classes used by gdtree
"""

from os import access, X_OK, DirEntry
from enum import Enum, Flag, auto
from typing import Callable

# Maximum depth of traversal
MAX_DEPTH = 32


class EntryType(Enum):
    """
    Enum type consisting of all possible directory entry types
    """

    DIRECTORY = 1
    FILE = 2
    EXECUTABLE = 3
    SYMLINK = 4


class Settings(Flag):
    """
    Holds all program settings
    """

    COLORIZE = auto()
    FANCY = auto()
    REVERSE = auto()


def get_type(entry: DirEntry) -> EntryType:
    """
    Gets the type of directory entry held by this file.

    May not function properly with non-POSIX file permission attributes.

    Args:
        entry (os.DirEntry): The directory entry object returned by os.scandir()

    Returns:
        EntryType: The type of directory entry located here (File, Directory, Symbolic Link, Executable)
    """

    try:
        is_symlink = entry.is_symlink()
    except OSError:
        # If error arises, we know that it cannot be of the type
        # expected - To not stop execution, return False
        is_symlink = False
    if is_symlink:
        return EntryType.SYMLINK

    try:
        is_dir = entry.is_dir()
    except OSError:
        # If error arises, we know that it cannot be of the type
        # expected - To not stop execution, return False
        is_dir = False
    if is_dir:
        return EntryType.DIRECTORY

    if access(entry.path, X_OK):
        return EntryType.EXECUTABLE
    return EntryType.FILE
