"""
A set of utility functions used by pytree
"""

import os
from pytree.entry_type import EntryType


def get_type(entry: os.DirEntry) -> EntryType:
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
        is_dir = entry.is_dir(follow_symlinks=False)
    except OSError:
        # If error arises, we know that it cannot be of the type
        # expected - To not stop execution, return False
        is_dir = False
    if is_dir:
        return EntryType.DIRECTORY

    if os.access(entry.path, os.X_OK, follow_symlinks=False):
        return EntryType.EXECUTABLE
    return EntryType.FILE
