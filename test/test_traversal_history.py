from pytree.entry_type import EntryType
from unittest import TestCase, main
import pytree.constants as constants
from pytree.directory_tree_entry import DirectoryTreeEntry
from pytree.traversal_history import DepthError, TraversalHistory


class TestTraversalHistory(TestCase):
    def test_initialization_basic(self):
        """
        Tests that values are initializesd properly to the correct default values
        """
        entry = TraversalHistory()
        self.assertEqual(entry.depth, 0)
        self.assertEqual(entry.history, -1)

    def test_initialization_all_params(self):
        """
        Tests that values are initializesd properly to the given parameters
        """
        entry = TraversalHistory(0b10101010, 8)
        self.assertEqual(entry.depth, 8)
        self.assertEqual(entry.history, 0b10101010)

    def test_add_history_basic(self):
        """
        Tests that adding a new value to history is
        done successfully and accurately
        """
        entry = TraversalHistory(0b100101, 6)
        entry.add_history(True)
        self.assertEqual(entry.depth, 7)
        self.assertEqual(entry.history, 0b1100101)

    def test_add_history_error(self):
        """
        Tests that an error is raised when trying to update history
        past the max possible depth
        """
        entry = TraversalHistory(
            2 ** (constants.MAX_DEPTH) - 1,
            constants.MAX_DEPTH,
        )
        with self.assertRaises(DepthError):
            entry.add_history(True)

    def test_add_history_start(self):
        """
        Tests that adding a new value to history is
        done successfully and accurately when at the start
        """
        entry = TraversalHistory()
        entry.add_history(True)
        self.assertEqual(entry.depth, 1)
        self.assertEqual(entry.history, 0b1)

    def test_update_history(self):
        """
        Tests that history is updated at correct depth
        """
        entry = TraversalHistory(0b100101, 6)
        entry.update_history(4, True)
        self.assertEqual(entry.depth, 6)
        self.assertEqual(entry.history, 0b101101)
        entry.update_history(4, False)
        self.assertEqual(entry.depth, 6)
        self.assertEqual(entry.history, 0b100101)

    def test_update_history_edge(self):
        """
        Tests that history is updated at exactly the overall depth
        """
        entry = TraversalHistory(0b100101, 6)
        entry.update_history(6, False)
        self.assertEqual(entry.history, 0b000101)
        entry.update_history(6, True)
        self.assertEqual(entry.depth, 6)
        self.assertEqual(entry.history, 0b100101)

    def test_update_error(self):
        """
        Tests that attempting to update history at an invalid depth throws an error
        """
        entry = TraversalHistory(0b100101, 6)
        with self.assertRaises(DepthError):
            entry.update_history(7, True)
        with self.assertRaises(DepthError):
            entry.update_history(0, True)


if __name__ == "__main__":
    main()
