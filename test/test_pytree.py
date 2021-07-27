from pytree.entry_type import EntryType
import unittest
from unittest.case import TestCase
from unittest.mock import Mock, patch
import pytree.constants as constants
from pytree.app import (
    generate_filestring,
    get_filestring_color,
    generate_prefix,
    get_type,
    DirectoryTreeEntry,
    _get_prefix,
    _get_prefix_file,
)
from colorama import Fore
from os import DirEntry, access


class TestTypeExtraction(TestCase):
    """
    Tests the ability to extract type from DirEntry objects returned by os.scandir().
    """

    @patch("pytree.app.os")
    def test_type_extraction_is_dir(self, mocked_os):
        """
        Tests that entry type is extracted when it is a directory
        """
        mock_values = ((True, False), (False, False))
        mocked_entries = []
        for is_dir, is_symlink in mock_values:
            mock = Mock(spec=DirEntry)
            mock.is_dir.return_value = is_dir
            mock.is_symlink.return_value = is_symlink
            mocked_entries.append(mock)

        # editing patched os module
        mocked_os.access.return_value = False

        expected_values = (EntryType.DIRECTORY, EntryType.FILE)
        for entry, expected_value in zip(mocked_entries, expected_values):
            type = get_type(entry)
            entry.is_dir.assert_called_once()
            self.assertEqual(type, expected_value)

    @patch("pytree.app.os")
    def test_type_extraction_is_dir_error(self, mocked_os):
        """
        Tests that testing for directory has errors handled to
        confirm nonexistence of directory
        """
        mock = Mock(spec=DirEntry)
        mock.is_dir.side_effect = OSError("")
        mock.is_symlink.return_value = False

        mocked_os.access.return_value = False

        type = get_type(mock)
        self.assertEqual(type, EntryType.FILE)

    @patch("pytree.app.os")
    def test_type_extraction_is_file(self, mocked_os):
        """
        Tests that entry type is extracted when it is a file
        """
        mock = Mock(spec=DirEntry)
        mock.is_dir.return_value = False
        mock.is_symlink.return_value = False

        mocked_os.access.return_value = False

        type = get_type(mock)
        self.assertEqual(type, EntryType.FILE)

    @patch("pytree.app.os")
    def test_type_extraction_is_symlink(self, mocked_os):
        """
        Tests that entry type is extracted when it is a symbolic link
        """
        mock_values = ((False, True), (False, False))
        mocked_entries = []
        for is_dir, is_symlink in mock_values:
            mock = Mock(spec=DirEntry)
            mock.is_dir.return_value = is_dir
            mock.is_symlink.return_value = is_symlink
            mocked_entries.append(mock)

        mocked_os.access.return_value = False

        expected_values = (EntryType.SYMLINK, EntryType.FILE)
        for entry, expected_value in zip(mocked_entries, expected_values):
            assert get_type(entry) == expected_value

    @patch("pytree.app.os")
    def test_type_extraction_is_symlink_error(self, mocked_os):
        """
        Tests that testing for directory has errors handled to
        confirm nonexistence of directory
        """
        mock = Mock(spec=DirEntry)
        mock.is_dir.return_value = False
        mock.is_symlink.side_effect = OSError("")

        mocked_os.access.return_value = False

        type = get_type(mock)
        assert type == EntryType.FILE

    @patch("pytree.app.os")
    def test_type_extraction_is_executable(self, mocked_os):
        """
        Tests that entry type is extracted when it is an executable
        """
        mock = Mock(spec=DirEntry)
        mock.is_dir.return_value = False
        mock.is_symlink.return_value = False

        mocked_os.access.return_value = True

        assert get_type(mock) == EntryType.EXECUTABLE


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
        self.assertEqual(entry.history, -1)
        self.assertEqual(entry.depth, 0)
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
        entry = DirectoryTreeEntry(path, type, history, depth)
        self.assertEqual(entry.path, path)
        self.assertEqual(entry.history, history)
        self.assertEqual(entry.depth, depth)
        self.assertEqual(entry.type, type)

    def test_update_history_basic(self):
        """
        Tests that adding a new value to DirectoryTreeEntry history is
        done successfully and accurately
        """
        entry = DirectoryTreeEntry("a/path", EntryType.FILE, 0b100101, 6)
        entry.update_history(True)
        self.assertEqual(entry.depth, 7)
        self.assertEqual(entry.history, 0b1100101)

    def test_update_history_error(self):
        """
        Tests that an error is raised when trying to update history
        past the max possible depth
        """
        entry = DirectoryTreeEntry(
            "a/path",
            EntryType.FILE,
            2 ** (constants.MAX_DEPTH) - 1,
            constants.MAX_DEPTH,
        )
        with self.assertRaises(RuntimeError):
            entry.update_history(True)

    def test_update_history_start(self):
        """
        Tests that adding a new value to DirectoryTreeEntry history is
        done successfully and accurately
        """
        entry = DirectoryTreeEntry("a/path", EntryType.FILE)
        entry.update_history(True)
        self.assertEqual(entry.depth, 1)
        self.assertEqual(entry.history, 0b1)


class TestStringGeneration(TestCase):
    def test_string_generation_colors(self):
        """
        Tests that colors of the output generation string are properly generated
        """
        mock_values = (
            (
                "__pycache__",
                EntryType.DIRECTORY,
                2,
            ),
            ("pytree", EntryType.DIRECTORY, 0),
            ("python3.8", EntryType.SYMLINK, 3),
            ("requirements.txt", EntryType.FILE, 8),
            ("activate", EntryType.EXECUTABLE, 3),
        )
        mocked_entries = []
        for name, type, depth in mock_values:
            mock = Mock()
            mock.name = name
            mock.type = type
            mock.depth = depth
            mocked_entries.append(mock)
        output_colors = (Fore.BLUE, Fore.BLUE, Fore.GREEN, Fore.WHITE, Fore.RED)
        for index, entry in enumerate(mocked_entries):
            self.assertEqual(output_colors[index], get_filestring_color(entry))

    def test_string_generation_colors_error(self):
        """
        Tests that passing an entry with an invalid type raises a value error
        """
        mock = Mock()
        mock.name = "a_file"
        mock.type = "invalid_type"
        mock.depth = 3
        with self.assertRaises(ValueError):
            color = get_filestring_color(mock)

    def test_string_generation_prefix(self):
        """
        Tests the correct prefix is returned based on the correct end state
        """
        input_values = (True, False)
        output_values = (constants.SPACER, constants.SPACER_WITH_LIMB)
        for input_value, output_value in zip(input_values, output_values):
            self.assertEqual(output_value, _get_prefix(input_value))

    def test_string_generation_prefix_file(self):
        """
        Tests the correct file prefix (prefix string just before the filename in the
        printed directory tree) is returned based on the correct end state
        """
        input_values = (True, False)
        output_values = (constants.BRANCH_END_PREFIX, constants.BRANCH_PREFIX)
        for input_value, output_value in zip(input_values, output_values):
            self.assertEqual(output_value, _get_prefix_file(input_value))

    def test_string_generation_integer(self):
        """
        Tests the correct prefix is returned when using numeric equivalents of booleans
        """
        input_values = (1, 0)
        output_values = (constants.SPACER, constants.SPACER_WITH_LIMB)
        for input_value, output_value in zip(input_values, output_values):
            self.assertEqual(output_value, _get_prefix(input_value))

    def test_string_generation_prefixes(self):
        """ """
        mock_values = (
            ("__pycache__", EntryType.DIRECTORY, 2, 0b00),
            ("pytree", EntryType.DIRECTORY, 0, -1),
            ("python3.8", EntryType.SYMLINK, 3, 0b001),
            ("requirements.txt", EntryType.FILE, 8, 0b11001000),
            ("activate", EntryType.EXECUTABLE, 3, 0b001),
        )
        mocked_entries = []
        for name, type, depth, history in mock_values:
            mock = Mock()
            mock.name = name
            mock.type = type
            mock.depth = depth
            mock.history = history
            mocked_entries.append(mock)
        output_strings = (
            "│   ├── ",
            "",
            "│   │   └── ",
            "        │   │       │   │   ├── ",
            "│   │   └── ",
        )
        for string, entry in zip(output_strings, mocked_entries):
            self.assertEqual(string, generate_prefix(entry))

    def test_string_generation_filestring(self):
        mock_values = (
            ("__pycache__", EntryType.DIRECTORY, 2, 0b00),
            ("pytree", EntryType.DIRECTORY, 0, -1),
            ("python3.8", EntryType.SYMLINK, 3, 0b001),
            ("requirements.txt", EntryType.FILE, 8, 0b11001000),
            ("activate", EntryType.EXECUTABLE, 3, 0b001),
        )
        mocked_entries = []
        for path, type, depth, history in mock_values:
            mock = Mock()
            mock.path = path
            mock.type = type
            mock.depth = depth
            mock.history = history
            mocked_entries.append(mock)
        output_strings = (
            "│   ├── " + Fore.BLUE + "__pycache__\n",
            Fore.BLUE + "pytree\n",
            "│   │   └── " + Fore.GREEN + "python3.8\n",
            "        │   │       │   │   ├── "
            + Fore.WHITE
            + "requirements.txt\n",
            "│   │   └── " + Fore.RED + "activate\n",
        )
        for output_string, entry in zip(output_strings, mocked_entries):
            self.assertEqual(output_string, generate_filestring(entry))


if __name__ == "__main__":
    unittest.main()
