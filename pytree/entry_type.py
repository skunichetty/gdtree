"""
Enum type consisting of all possible directory entry types encountered by pytree.
"""
from enum import Enum


class EntryType(Enum):
    DIRECTORY = 1
    FILE = 2
    EXECUTABLE = 3
    SYMLINK = 4
