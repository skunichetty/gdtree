import os
from enum import Enum, IntFlag
from collections import deque
from typing import Tuple

MAX_DEPTH = 30


class EntryType(Enum):
    DIRECTORY = 1
    FILE = 2
    EXECUTABLE = 3
    SYMLINK = 4


class TraversalEntry:
    def __init__(self, path, depth=0, type=EntryType.FILE):
        self.path = path
        self.depth = depth
        self.type = type


def start():
    print("Running Pytree")
    # with os.scandir(os.getcwd()) as it:
    #     files = sorted(it, key=lambda x: x.name, reverse=True)
    # print("\n\u2560\u2550 ".join(map(lambda x: x.path, files)))

    # # use this for timing comparison
    # for root, dirs, files in os.walk(os.getcwd()):
    #     print(root)
    traverse(os.getcwd())


def generate_traversal_entry(entry: os.DirEntry, depth: int) -> TraversalEntry:
    if depth < 0:
        raise ValueError(
            "Depth of %d cannot be traversed. Depth must be strictly nonnegative."
            % depth
        )
    filetype = EntryType.FILE

    if entry.is_dir():
        filetype = EntryType.DIRECTORY
    elif entry.is_symlink():
        filetype = EntryType.SYMLINK

    return TraversalEntry(entry.path, depth + 1, filetype)


def traverse(root_dir: str) -> None:
    stack = deque()
    start = TraversalEntry(root_dir, 0, EntryType.DIRECTORY)
    stack.append(start)
    while stack:
        current_entry = stack.pop()
        if os.path.split(current_entry.path)[1][0] != ".":
            if (
                current_entry.type == EntryType.DIRECTORY
                and current_entry.depth < MAX_DEPTH
            ):
                with os.scandir(current_entry.path) as it:
                    entries = sorted(it, key=lambda x: x.name, reverse=True)
                for entry in entries:
                    stack.append(
                        generate_traversal_entry(entry, current_entry.depth)
                    )

            elif current_entry.type == EntryType.FILE:
                print("FILE: %s" % current_entry.path)
            elif current_entry.type == EntryType.EXECUTABLE:
                print("EXEC: %s" % current_entry.path)
            elif current_entry.type == EntryType.SYMLINK:
                print("SYMLINK: %s" % current_entry.path)
            else:
                raise ValueError(
                    "Unknown Entry Type detected %s" % current_entry.type
                )
