import os
from sys import platform
import stat as read_stat
from collections import deque
from pytree import entry_type
import pytree.constants as constants
from pytree.entry_type import EntryType
from colorama import init


class DirectoryTreeEntry:
    def __init__(
        self, path: str, type: EntryType, history: int = -1, depth: int = 0
    ):
        """
        Initializes DirectoryTreeEntry

        Args:
            path (str): The path of the entry
            type (EntryType): The entry type
            history (int, optional): The history of the entry up to that point Defaults to -1.
            depth (int, optional): The depth of this entry in the tree. Defaults to 0.
        """
        self.depth = depth
        self.history = history
        self.path = path
        self.type = type

    def update_history(self, is_end: bool):
        """
        Updates the history of this specific entry

        Args:
            is_end (bool): The history state to update with, specifying whether at this depth
            the entry was at the end of a directory subtree

        Raises:
            RuntimeError: Raises error if history is attempted to be updated beyond
            maximum history depth
        """
        if self.depth == constants.MAX_DEPTH:
            raise RuntimeError(
                "Attempted to update history to extend beyond maximum allowed depth"
            )
        if self.depth == 0:
            self.history = 0
        if is_end:
            mask = 1 << self.depth
            self.history |= mask
        self.depth += 1


def start():
    if platform == "win32" or platform == "cygwin":
        # initialize colorama since we need to escape ANSI characters
        # for use on Windows
        init()


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


def generate_filestring(entry: DirectoryTreeEntry) -> str:
    """
    Generates filestring to print to output given a corresponding entry

    Args:
        entry (DirectoryTreeEntry): The entry being considered

    Returns:
        str: The filestring for this entry as to be printed out.
    """
    prefix = generate_prefix(entry)
    color = get_filestring_color(entry)
    name = os.path.basename(entry.path)
    string = [prefix, color, name, "\n"]
    return "".join(string)


def _get_prefix(is_end: bool) -> str:
    """
    Gets the prefix given state value at that depth.

    Args:
        is_end (bool): The state of the entry; is at the end of a directory tree or not.

    Returns:
        str: Correct prefix value given that state
    """
    if is_end:
        return constants.SPACER
    return constants.SPACER_WITH_LIMB


def _get_prefix_file(is_end: bool) -> str:
    """
    Gets the prefix directly preceding a file name given state value at that depth.

    Args:
        is_end (bool): The state of the entry; is at the end of a directory tree or not.

    Returns:
        str: Correct prefix value given that state
    """
    if is_end:
        return constants.BRANCH_END_PREFIX
    return constants.BRANCH_PREFIX


def generate_prefix(entry: DirectoryTreeEntry) -> str:
    """
    Generates prefix string from traversal history stored in a
    DirectoryTreeEntry. This is responsible for generating the set of fancy box characters
    which precede each filename

    Args:
        entry (DirectoryTreeEntry): The current entry

    Returns:
        str: The prefix string corresponding to the location of the entry
    """
    if entry.depth == 0:
        return ""
    mask = 1
    prefixes = []
    for i in range(entry.depth):
        current_state = entry.history & mask
        prefix_function = _get_prefix
        if i == 0:
            prefix_function = _get_prefix_file
        prefixes.append(prefix_function(current_state))
        mask <<= 1
    result = "".join(prefixes[::-1])
    return result


def get_filestring_color(entry: DirectoryTreeEntry) -> str:
    """
    Get the color used in the filestring for the given entry. These are
    ANSI escape strings that colorize output text in the terminal.

    Args:
        entry (DirectoryTreeEntry): The entry to get filestring color for

    Raises:
        ValueError: Raises error if the entry type is invalid

    Returns:
        str: The ANSI color escape sequence
    """
    try:
        color = constants.COLORMAP[entry.type]
    except KeyError:
        # Entry Type is not in COLORMAP - thus it is not a valid
        # file type
        raise ValueError("Invalid entry type given")
    return color
