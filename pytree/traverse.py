"""
Directory tree traversal utilities
"""


import os
from pytree.traversal_history import TraversalHistory
from pytree.entry_type import EntryType
from pytree.directory_tree_entry import DirectoryTreeEntry
from typing import Generator
from pytree.utils import get_type
import pytree.constants as constants


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

    # Generate sorted list from iterator
    try:
        with scandir_it:
            sorted_it = sorted(scandir_it, key=lambda x: x.name)
    except OSError:
        # Same OSError policy as above
        return

    # Update once to get the new history and depth - less calls to original entry
    new_history, new_depth = entry.history.add_history(False)

    num_entries = len(sorted_it)
    for index, directory_entry in enumerate(sorted_it):
        # we want to avoid . directories and files (hidden by nature)
        if not os.path.basename(directory_entry.path).startswith("."):
            type = get_type(directory_entry)

            # Create a new history entry that reflects the updated depth
            current_subentry_history = TraversalHistory(new_history, new_depth)
            # If we are at the end, update the entry's history to reflect that state
            if index == num_entries - 1:
                current_subentry_history.update_history(new_depth - 1, True)

            current_subentry = DirectoryTreeEntry(
                directory_entry.path, type, current_subentry_history
            )

            yield current_subentry

            if type == EntryType.DIRECTORY and new_depth < constants.MAX_DEPTH:
                yield from _traverse(current_subentry)


def traverse(start_dir: str) -> Generator[DirectoryTreeEntry, None, None]:
    starting_entry = DirectoryTreeEntry(start_dir, EntryType.DIRECTORY)
    yield from _traverse(starting_entry)
