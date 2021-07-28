"""
A set of utility functions used by pytree
"""

import os
from pytree.entry_type import EntryType


def _test_entry_type(type_function) -> bool:
    """
    Tests the return value given by the entry type function
    type_function with exception safety against OSError and returns
    boolean value to user.
    Args:
        type_function (Function): the entry type function

    Returns:
        bool: The output from the entry type test
    """
    try:
        is_type = type_function()
    except OSError:
        # If error arises, we know that it cannot be of the type
        # expected - To not stop execution, return False
        is_type = False
    return is_type


def get_type(entry: os.DirEntry) -> EntryType:
    """
    Gets the type of directory entry held by this file.

    May not function properly with non-POSIX file permission attributes.

    Args:
        entry (os.DirEntry): The directory entry object returned by os.scandir()

    Returns:
        EntryType: The type of directory entry located here (File, Directory, Symbolic Link, Executable)
    """

    is_dir = _test_entry_type(entry.is_dir)
    if is_dir:
        return EntryType.DIRECTORY
    is_symlink = _test_entry_type(entry.is_symlink)
    if is_symlink:
        return EntryType.SYMLINK
    if os.access(entry.path, os.X_OK):
        return EntryType.EXECUTABLE
    return EntryType.FILE
