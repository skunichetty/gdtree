from os import DirEntry
from pytree.entry_type import EntryType
from unittest import TestCase, main
from unittest.mock import Mock, patch
from pytree.app import get_type
from pytree.directory_tree_entry import DirectoryTreeEntry
from pytree.traverse import traverse


class TestTraversal(TestCase):
    mocked_directories = []

    @classmethod
    def setUpClass(cls) -> None:
        mock_values = (
            ("__pycache__", True, False),
            ("pytree", True, False),
            ("python3.8", False, True),
            ("requirements.txt", False, False),
        )
        dirs = []
        for path, is_dir, is_symlink in mock_values:
            mock = Mock(spec=DirEntry)
            mock.path = path
            mock.is_dir.return_value = is_dir
            mock.is_symlink.return_value = is_symlink
            dirs.append(mock)
        cls.mocked_directories = dirs

    @patch("pytree.traverse.os.scandir")
    @patch("pytree.traverse.os.access")
    def test_traverse(self, mocked_scandir, mocked_access):
        """
        Tests that traversal of a directory tree is completed
        """
        mocked_scandir.return_value = self.mocked_directories
        mocked_access.return_value = True
        outputs = [
            DirectoryTreeEntry("__pycache__", EntryType.DIRECTORY, 1, 0b0),
            DirectoryTreeEntry("pytree", EntryType.DIRECTORY, 1, 0b0),
            DirectoryTreeEntry("python3.8", EntryType.SYMLINK, 1, 0b0),
            DirectoryTreeEntry("requirements.txt", EntryType.FILE, 1, 0b1),
        ]
        for item, expected_output in zip(traverse("random_dir"), outputs):
            self.assertEqual(item.name == expected_output.name)
            self.assertEqual(item.type == expected_output.type)
            self.assertEqual(item.depth == expected_output.depth)
            self.assertEqual(item.history == expected_output.history)

    def test_traverse_error(self):
        """
        Tests that traversal fails when given an invalid directory
        """
        with self.assertRaises(NotADirectoryError):
            it = traverse("///")


if __name__ == "__main__":
    main()
