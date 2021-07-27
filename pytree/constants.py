"""
A set of constant variables and objects utilized by pytree
"""
from pytree.entry_type import EntryType
from colorama import Fore

# Mapping directory entry types to colors in terminal
COLORMAP = {
    EntryType.EXECUTABLE: Fore.RED,
    EntryType.FILE: Fore.WHITE,
    EntryType.SYMLINK: Fore.GREEN,
    EntryType.DIRECTORY: Fore.BLUE,
}

# The prefix that prepends directory entries in the final view
BRANCH_PREFIX = "\u251C\u2500\u2500 "
# Prefix for end of branch directory entries (aka, last file in a given folder)
BRANCH_END_PREFIX = "\u2514\u2500\u2500 "

# A fancier version of the above prefix
BRANCH_PREFIX_FANCY = "\u2560\u2550\u2550 "
# Prefix for end of branch directory entries (aka, last file in a given folder)
BRANCH_END_PREFIX_FANCY = "\u255A\u2550\u2550 "
# Spacer with branch limb
SPACER_WITH_LIMB = "\u2502   "
# Spacer with no branch limb
SPACER = "    "

# The maximum traversal depth for the directory printing
MAX_DEPTH = 30
