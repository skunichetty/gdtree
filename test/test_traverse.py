from os import DirEntry, scandir
from gdtree.end_state_history import EndStateHistory
from gdtree.utils import EntryType
from unittest import TestCase, main
from unittest.mock import patch, Mock
from gdtree.traverse import (
    filter_prefix,
    reverse_traverse_directory,
    traverse_directory,
    construct_from_history,
)


class TestTraversal(TestCase):
    @patch("gdtree.traverse.scandir", spec=scandir)
    @patch("gdtree.utils.access")
    def test_traverse(self, mocked_access, mocked_scandir):
        """
        Tests that traversal of a directory tree is completed
        """
        mocked_values = [
            ("a/path/to/__pycache__", "__pycache__", False, True),
            ("a/path/to/pytree", "pytree", False, False),
            ("a/path/to/python3.8", "python3.8", False, True),
            ("a/path/to/requirements.txt", "requirements.txt", False, False),
        ]
        mocked_directories = []
        for path, name, is_dir, is_symlink in mocked_values:
            mock = Mock(spec=DirEntry)
            mock.name = name
            mock.path = path
            mock.is_dir.return_value = is_dir
            mock.is_symlink.return_value = is_symlink
            mocked_directories.append(mock)
        mocked_scandir.return_value.__iter__.return_value = iter(
            mocked_directories
        )
        mocked_access.return_value = False
        mock_outputs = (
            (
                "__pycache__",
                EntryType.SYMLINK,
                EndStateHistory([False]),
            ),
            (
                "python3.8",
                EntryType.SYMLINK,
                EndStateHistory([False]),
            ),
            ("pytree", EntryType.FILE, EndStateHistory([False])),
            (
                "requirements.txt",
                EntryType.FILE,
                EndStateHistory([True]),
            ),
        )
        for item, expected_output in zip(
            traverse_directory("random_dir"), mock_outputs
        ):
            self.assertEqual(item[0], expected_output[0])
            self.assertEqual(item[1], expected_output[1])

    @patch("gdtree.traverse.scandir", spec=scandir)
    @patch("gdtree.utils.access")
    def test_reverse_traverse(self, mocked_access, mocked_scandir):
        """
        Tests that traversal of a directory tree is completed
        """
        mocked_values = [
            ("a/path/to/__pycache__", "__pycache__", False, True),
            ("a/path/to/pytree", "pytree", False, False),
            ("a/path/to/python3.8", "python3.8", False, True),
            ("a/path/to/requirements.txt", "requirements.txt", False, False),
        ]
        mocked_directories = []
        for path, name, is_dir, is_symlink in mocked_values:
            mock = Mock(spec=DirEntry)
            mock.name = name
            mock.path = path
            mock.is_dir.return_value = is_dir
            mock.is_symlink.return_value = is_symlink
            mocked_directories.append(mock)
        mocked_scandir.return_value.__iter__.return_value = iter(
            mocked_directories
        )
        mocked_access.return_value = False
        mock_outputs = (
            (
                "requirements.txt",
                EntryType.FILE,
                EndStateHistory([True]),
            ),
            ("pytree", EntryType.FILE, EndStateHistory([False])),
            (
                "python3.8",
                EntryType.SYMLINK,
                EndStateHistory([False]),
            ),
            (
                "__pycache__",
                EntryType.SYMLINK,
                EndStateHistory([False]),
            ),
        )
        for item, expected_output in zip(
            reverse_traverse_directory("random_dir"), mock_outputs
        ):
            self.assertEqual(item[0], expected_output[0])
            self.assertEqual(item[1], expected_output[1])

    def test_filter_prefix(self):
        """
        Tests that scandir entries are properly filtered given a
        blacklist prefix
        """
        mocked_values = [
            ("a/path/to/.pycache", ".pycache", False, True),
            ("a/path/to/..", "..", False, True),
            ("a/path/to/pytree", "pytree", False, False),
            ("a/path/to/python3.8", "python3.8", False, True),
            ("a/path/to/requirements.txt", "requirements.txt", False, False),
        ]
        mocked_directories = []
        for path, name, is_dir, is_symlink in mocked_values:
            mock = Mock(spec=DirEntry)
            mock.name = name
            mock.path = path
            mock.is_dir.return_value = is_dir
            mock.is_symlink.return_value = is_symlink
            mocked_directories.append(mock)
        it = iter(mocked_directories)

        outputs = mocked_directories[2:]
        output_it = list(filter_prefix(it, "."))
        for expected_output, output in zip(outputs, output_it):
            self.assertEqual(expected_output, output)

    def test_construct_from_history(self):
        """
        Tests whether history is constructed from previous values as expected
        """
        history = EndStateHistory([True, False, False])
        new_history = EndStateHistory([True, False, False, True])
        output_history = construct_from_history(history, True)
        for expected, output in zip(new_history, output_history):
            self.assertEqual(expected, output)


if __name__ == "__main__":
    main()
