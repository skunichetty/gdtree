from pytree.traversal_history import TraversalHistory
from pytree.entry_type import EntryType
from unittest import TestCase, main
import pytree.constants as constants
from pytree.directory_tree_entry import DirectoryTreeEntry


class TestDirectoryTreeEntry(TestCase):
    def test_initialization_default(self):
        """
        Tests that the DirectoryTreeEntry is initialized with default values
        for the history parameter
        """

        path = "a/path/to/a/folder"
        type = EntryType.FILE
        entry = DirectoryTreeEntry(path, type)
        self.assertEqual(entry.path, path)
        self.assertEqual(entry.history.history, -1)
        self.assertEqual(entry.history.depth, 0)
        self.assertEqual(entry.type, type)

    def test_initialization_all_params(self):
        """
        Tests that the DirectoryTreeEntry is initialized with the given values
        for all parameters
        """
        path = "a/path/to/a/folder"
        type = EntryType.FILE
        depth = 5
        history = 0b10000
        history_entry = TraversalHistory(history, depth)
        entry = DirectoryTreeEntry(path, type, history_entry)
        self.assertEqual(entry.path, path)
        self.assertEqual(entry.history.history, history)
        self.assertEqual(entry.history.depth, depth)
        self.assertEqual(entry.type, type)


if __name__ == "__main__":
    main()
