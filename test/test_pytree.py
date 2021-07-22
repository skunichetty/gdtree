import unittest
from unittest.case import TestCase
from pytree import app
from os import DirEntry, path
from unittest.mock import Mock
from typing import List


class TestPytree(TestCase):
    def generate_traversal_entry_mocks(self) -> List[Mock]:
        """
        Generates a set of mocked os.DirEntry objects needed to test
        traversal helper functions
        """
        mock_values = (
            ("/a/path/to/a/folder", True, False),
            ("/a/path/to/a/folder/but/symlink", False, True),
            ("/a/path/to/a/file.txt", False, False),
        )
        mocked_entries = []
        for path, is_dir, is_symlink in mock_values:
            mock = Mock()
            mock.path = path
            mock.is_dir.return_value = is_dir
            mock.is_symlink.return_value = is_symlink
            mocked_entries.append(mock)
        return mocked_entries

    def test_traversal_entry_generation_entry_type(self):
        """
        Tests that traversal entries are succesfully generated from input directories
        to reflect all possible values
        """
        entries = self.generate_traversal_entry_mocks()
        types = (
            app.EntryType.DIRECTORY,
            app.EntryType.SYMLINK,
            app.EntryType.FILE,
        )
        for index, entry in enumerate(entries):
            traversal_entry = app.generate_traversal_entry(entry, 0)
            assert traversal_entry.type == types[index]

    def test_traversal_entry_generation_depth(self):
        """
        Tests that traversal entries are generated with a correct and valid depth
        """
        entries = self.generate_traversal_entry_mocks()
        depths = (0, 5, -1)
        for index, entry in enumerate(entries):
            try:
                traversal_entry = app.generate_traversal_entry(
                    entry, depths[index]
                )
                assert traversal_entry.depth == depths[index] + 1
            except ValueError:
                assert index == 2

    def test_traversal_entry_path_generation(self):
        """
        Tests that traversal entries are generated with the correct path
        """
        entries = self.generate_traversal_entry_mocks()
        for entry in entries:
            traversal_entry = app.generate_traversal_entry(entry, 0)
            assert traversal_entry.path == entry.path


if __name__ == "__main__":
    unittest.main()
