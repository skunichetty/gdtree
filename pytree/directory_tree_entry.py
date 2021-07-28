"""
A wrapper on directory entries as utilized during the tree traversal
"""
from pytree.entry_type import EntryType
from pytree.traversal_history import TraversalHistory


class DirectoryTreeEntry:
    """
    A lightweight class used to store information extracted from the directory tree
    during traversal
    """

    def __init__(
        self,
        path: str,
        type: EntryType,
        history: TraversalHistory = None,
    ):
        """
        Initializes DirectoryTreeEntry

        Args:
            path (str): The path of the entry
            type (EntryType): The entry type
            history (TraversalHistory): The history of the entry up to that point
        """
        if history is not None:
            self.history = history
        else:
            self.history = TraversalHistory()
        self.path = path
        self.type = type
