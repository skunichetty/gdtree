"""
A set of filestring generating utilities.
"""

from sys import prefix
from gdtree.end_state_history import EndStateHistory
from gdtree.utils import EntryType, Settings
from typing import Callable, Dict
from colorama import Fore


# =====Prefixes=====
BRANCH_PREFIX = "\u251C\u2500\u2500 "
BRANCH_END_PREFIX = "\u2514\u2500\u2500 "
SPACER_WITH_LIMB = "\u2502   "
SPACER = "    "
# ==Fancy Prefixes==
SPACER_WITH_LIMB_FANCY = "\u2551   "
BRANCH_END_PREFIX_FANCY = "\u255A\u2550\u2550 "
BRANCH_PREFIX_FANCY = "\u2560\u2550\u2550 "

# =====Prefix Sets=====
# These are maps from End state to the prefix strings which are printed
# before file names in the printed output
# ==Subsets==
EXT = {
    # External prefixes, show branch location rather than file location
    True: SPACER,
    False: SPACER_WITH_LIMB,
}
FANCY = {
    # Fancy external prefixes,
    True: SPACER,
    False: SPACER_WITH_LIMB_FANCY,
}
FILE_EXT = {
    # File prefixes, show file location within subdirectory
    True: BRANCH_END_PREFIX,
    False: BRANCH_PREFIX,
}
FILE_FANCY = {
    # Fancy file prefixes
    True: BRANCH_END_PREFIX_FANCY,
    False: BRANCH_PREFIX_FANCY,
}
# ==Main Sets==
PREFIX_REGULAR = {True: FILE_EXT, False: EXT}
PREFIX_FANCY = {True: FILE_FANCY, False: FANCY}

# The default color to be printed
DEFAULT_COLOR = Fore.WHITE

# Mapping directory entry types to colors in terminal
COLORMAP = {
    EntryType.EXECUTABLE: Fore.RED,
    EntryType.FILE: DEFAULT_COLOR,
    EntryType.SYMLINK: Fore.GREEN,
    EntryType.DIRECTORY: Fore.CYAN,
}


def _get_prefix(end_state: bool, prefix_subset: Dict[bool, str]) -> str:
    """
    Returns proper prefix given state and prefix_subset.

    Args:
        end_state (bool): End state for this prefix.
        prefix_subset (Dict[bool, str]): A map of end state to prefixes.

    Raises:
        ValueError: Raises if the state given is invalid (end_state not boolean)

    Returns:
        str: The correct prefix in the prefix_set
    """
    try:
        output_prefix = prefix_subset[end_state]
    except KeyError as err:
        raise ValueError("Invalid state type") from err
    return output_prefix


def _build_prefix(
    history: EndStateHistory, prefix_set: Dict[bool, Dict[bool, str]]
) -> str:
    last_index = len(history) - 1
    prefixes = [None] * (last_index + 1)
    for index, state in enumerate(history):
        prefix_subset = prefix_set[index == last_index]
        prefix = _get_prefix(state, prefix_subset)
        prefixes[index] = prefix
    return "".join(prefixes)


def build_prefix(history: EndStateHistory) -> str:
    """
    Build a regular prefix from an EndStateHistory

    Args:
        history (EndStateHistory): History of the end states for this entry

    Returns:
        str: The corresponding prefix
    """
    return _build_prefix(history, PREFIX_REGULAR)


def build_fancy_prefix(history: EndStateHistory) -> str:
    """
    Builds a fancy prefix from an EndStateHistory

    Args:
        history (EndStateHistory): History of the end states for this entry

    Returns:
        str: The corresponding prefix
    """
    return _build_prefix(history, PREFIX_FANCY)


def get_filestring_color(type: EntryType) -> str:
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
        color = COLORMAP[type]
    except KeyError:
        # Entry Type is not in COLORMAP - thus it is not a valid
        # file type
        raise ValueError(type)
    return color


def type_colorize(text: str, type: EntryType) -> str:
    """
    Colorizes the text given depending on the type

    Args:
        text (str): The text to colorize
        type (EntryType): The type of text with which colorization is performed.

    Raises:
        ValueError: Raises if an invalid type is given

    Returns:
        str: The colorized text
    """
    if type == EntryType.FILE:
        # Files have no special colors - so don't even perform any colorization
        return text
    color_escape_seq = get_filestring_color(type)
    return "".join([color_escape_seq, text, DEFAULT_COLOR])


def create_filestring_builder(
    settings: Settings,
) -> Callable[[str, EntryType, EndStateHistory], str]:
    """
    Generates a filestring builder function from user settings

    Args:
        settings (Settings): User defined settings, specified at command line

    Returns:
        Callable[[str, EntryType, EndStateHistory], str]: The filestring builder function
        with the settings enabled
    """
    colorize = bool(settings & Settings.COLORIZE)
    fancy = bool(settings & Settings.FANCY)

    prefix_function = build_fancy_prefix if fancy else build_prefix

    def build_filestring(
        name: str, type: EntryType, history: EndStateHistory
    ) -> str:
        """
        Builds a filestring for a directory entry

        Args:
            path (str): The path to the entry
            type (EntryType): The type of entry
            history (EndStateHistory): End state history of this entry's location

        Returns:
            str: The properly formatted filestring
        """
        prefix = prefix_function(history)
        if colorize:
            name = type_colorize(name, type)
        return "".join((prefix, name))

    return build_filestring
