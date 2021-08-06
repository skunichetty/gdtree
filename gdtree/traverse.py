"""
Directory tree traversal utilities
"""


from os import scandir, DirEntry
from gdtree.end_state_history import EndStateHistory
from gdtree.utils import EntryType, MAX_DEPTH, get_type
from typing import Generator, Iterator, Tuple


def filter_prefix(
    scandir_it: Generator[DirEntry, None, None], blacklisted_str: str
) -> Iterator:
    """
    Filters all os.DirEntry objects whose filename has the blacklisted prefix string
    Args:
        scandir_it (Generator[DirEntry, None, None]): The input generator from os.scandir()
        blacklisted_str (str): The string prefix to filter out

    Yields:
        Iterator: An iterator of filtered values
    """
    return filter(lambda x: not x.name.startswith(blacklisted_str), scandir_it)


def construct_from_history(history: EndStateHistory, is_end: bool) -> EndStateHistory:
    """
    Constructs a new EndStateHistory from a previous history, and appends a new end state to it.

    Args:
        history (EndStateHistory): The previous history
        is_end (bool): The new end state to append to the new history

    Returns:
        EndStateHistory: The new end state history
    """
    new_history = EndStateHistory()
    new_history.extend(history)
    new_history.append(is_end)
    return new_history


def _traverse(
    path: str, history: EndStateHistory, reverse: bool
) -> Generator[Tuple[str, EntryType, EndStateHistory], None, None]:
    """
    Traverses the directory starting at path

    Args:
        path (str): The top level directory to traverse downward from
        history (EndStateHistory): The end state traversal history up to this point
        reverse (bool): Reverses the order of traversal (lexicographical order)

    Yields:
        Generator[Tuple[str, EntryType, EndStateHistory], None, None]: Generates the paths,
        types, and end state histories of the entries traversed
    """
    try:
        scandir_it = scandir(path)
    except NotADirectoryError as err:
        return
    except OSError as err:
        # We don't want to fail the entire traversal if something fails on
        # OS call - continue with traversal
        # This will also catch if the input directory is bad, we rely on EAFP principle here
        print(err)
        return
    try:
        with scandir_it:
            filtered_it = list(filter_prefix(scandir_it, "."))
    except OSError as err:
        # Same OSError policy as above
        print(err)
        return

    filtered_it.sort(key=lambda x: x.name, reverse=reverse)
    last_index = len(filtered_it) - 1
    for index, directory_entry in enumerate(filtered_it):
        type = get_type(directory_entry)
        subentry_history = construct_from_history(history, index == last_index)
        yield directory_entry.name, type, subentry_history
        if type == EntryType.DIRECTORY and len(subentry_history) < MAX_DEPTH:
            yield from _traverse(directory_entry.path, subentry_history, reverse)


def reverse_traverse_directory(
    start_dir: str,
) -> Generator[Tuple[str, EntryType, EndStateHistory], None, None]:
    """
    Traverses the directory given and yields the entries found in reverse lexicographical order

    Args:
        start_dir (str): Absolute path to the directory to traverse

    Yields:
        Generator[Tuple[str, EntryType, EndStateHistory], None, None]: Generates the paths,
        types, and end state histories of the entries traversed
    """
    yield from _traverse(start_dir, EndStateHistory(), True)


def traverse_directory(
    start_dir: str,
) -> Generator[Tuple[str, EntryType, EndStateHistory], None, None]:
    """
    Traverses the directory given and yields the entries found

    Args:
        start_dir (str): Absolute path to the directory to traverse

    Yields:
        Generator[Tuple[str, EntryType, EndStateHistory], None, None]: Generates the paths,
        types, and end state histories of the entries traversed
    """
    yield from _traverse(start_dir, EndStateHistory(), False)
