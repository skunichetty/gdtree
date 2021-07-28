"""
Directory tree traversal utilities
"""


import os
from pytree.traversal_history import TraversalHistory
from pytree.entry_type import EntryType
from pytree.directory_tree_entry import DirectoryTreeEntry
from typing import Generator
from pytree.utils import get_type


def _traverse(
    entry: DirectoryTreeEntry,
) -> Generator[DirectoryTreeEntry, None, None]:
    # Open directory and scan items in it
    try:
        scandir_it = os.scandir(entry.path)
    except OSError:
        # We don't want to fail the entire traversal if something fails on
        # OS call - continue with traversal
        return
    entry.history.add_history(False)
    # Generate sorted list from iterator
    try:
        with scandir_it:
            sorted_it = sorted(scandir_it, key=lambda x: x.name)
    except OSError:
        # Same OSError policy as above
        return
    num_entries = len(sorted_it)
    for index, directory_entry in enumerate(sorted_it):
        if not os.path.basename(directory_entry.path).startswith("."):
            type = get_type(directory_entry)
            history = TraversalHistory(
                entry.history.history, entry.history.depth
            )
            if index == num_entries - 1:
                history.update_history(entry.history.depth, True)
            new_entry = DirectoryTreeEntry(directory_entry.path, type, history)
            yield new_entry
            if type == EntryType.DIRECTORY:
                yield from _traverse(new_entry)


def traverse(start_dir: str) -> Generator[DirectoryTreeEntry, None, None]:
    starting_entry = DirectoryTreeEntry(start_dir, EntryType.DIRECTORY)
    yield from _traverse(starting_entry)
