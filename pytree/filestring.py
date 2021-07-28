"""
A set of filestring generating utilities.
"""

import colorama
from pytree.directory_tree_entry import DirectoryTreeEntry
import pytree.constants as constants
import os


def generate_filestring(entry: DirectoryTreeEntry, do_colorize: bool) -> str:
    """
    Generates filestring to print to output given a corresponding entry

    Args:
        entry (DirectoryTreeEntry): The entry being considered

    Returns:
        str: The filestring for this entry as to be printed out.
    """
    prefix = generate_prefix(entry)
    name = get_name(entry, do_colorize)
    string = [prefix, name]
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
    depth = entry.history.depth
    if depth == 0:
        return ""
    mask = 1
    prefixes = []
    # To generate string, start from LSB and iterate forward
    # File prefix lies at MSB (depth - 1)
    for i in range(depth):
        current_state = entry.history.history & mask
        prefix_function = _get_prefix
        if i == depth - 1:
            prefix_function = _get_prefix_file
        prefixes.append(prefix_function(current_state))
        mask <<= 1
    result = "".join(prefixes)
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
        raise ValueError(entry.type)
    return color


def colorize(color: str, text: str) -> str:
    """
    Colorizes the given text to the given color. Will terminate text with the
    default color as defined in constants.py

    Args:
        color (str): The ANSI escape sequence giving the color to colorize to
        text (str): The text to colorize

    Returns:
        str: The properly escaped and colorized string
    """
    return "".join([color, text, constants.DEFAULT_COLOR])


def get_name(entry: DirectoryTreeEntry, do_colorize: bool) -> str:
    """
    Gets the properly formatted entry name from the entry given.

    Args:
        entry (DirectoryTreeEntry): The entry whose formatted name is returned
        do_colorize (bool): If true, the name will be colorized appropriately; else not

    Returns:
        str: The properly formatted entry name
    """
    color = get_filestring_color(entry)
    name = os.path.basename(entry.path)
    if not do_colorize or color == constants.DEFAULT_COLOR:
        # in either case, do not colorize
        return name
    return colorize(color, name)
