from unittest import TestCase, main

import colorama

from pytree.filestring import (
    generate_filestring,
    get_filestring_color,
    generate_prefix,
    _get_prefix,
    _get_prefix_file,
    get_name,
    colorize,
)
from pytree.entry_type import EntryType
from unittest.mock import Mock
from colorama import Fore
import pytree.constants as constants


class TestStringGeneration(TestCase):
    def test_string_generation_get_colors(self):
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

    def test_string_generation_get_colors_error(self):
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
            ("python3.8", EntryType.SYMLINK, 3, 0b100),
            ("requirements.txt", EntryType.FILE, 8, 0b00010011),
            ("activate", EntryType.EXECUTABLE, 3, 0b100),
        )
        mocked_entries = []
        for path, type, depth, history in mock_values:
            mocked_entry = Mock()
            mocked_history = Mock()
            mocked_entry.path = path
            mocked_entry.type = type
            mocked_history.depth = depth
            mocked_history.history = history
            mocked_entry.history = mocked_history
            mocked_entries.append(mocked_entry)
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
            ("pytree", EntryType.DIRECTORY, 0, -1),
            ("python3.8", EntryType.SYMLINK, 3, 0b100),
            ("requirements.txt", EntryType.FILE, 8, 0b00010011),
            ("activate", EntryType.EXECUTABLE, 3, 0b100),
        )
        mocked_entries = []
        for path, type, depth, history in mock_values:
            mocked_entry = Mock()
            mocked_history = Mock()
            mocked_entry.path = path
            mocked_entry.type = type
            mocked_history.depth = depth
            mocked_history.history = history
            mocked_entry.history = mocked_history
            mocked_entries.append(mocked_entry)
        colorize_values = (True, True, False, True, True, True)
        output_strings = (
            "│   ├── " + Fore.BLUE + "__pycache__" + Fore.WHITE,
            Fore.BLUE + "pytree" + Fore.WHITE,
            "pytree",
            "│   │   └── " + Fore.GREEN + "python3.8" + Fore.WHITE,
            "        │   │       │   │   ├── requirements.txt",
            "│   │   └── " + Fore.RED + "activate" + Fore.WHITE,
        )
        for output_string, entry, colorize in zip(
            output_strings, mocked_entries, colorize_values
        ):
            self.assertEqual(
                output_string, generate_filestring(entry, colorize)
            )

    def test_string_generation_colorize(self):
        """
        Tests that text is appropriately colorized
        """
        input_text = (
            "__pycache__",
            "pytree",
            "python3.8",
            "requirements.txt",
            "activate",
        )
        colorize_values = (
            Fore.BLUE,
            Fore.BLUE,
            Fore.GREEN,
            Fore.WHITE,
            Fore.RED,
        )
        output_text = (
            Fore.BLUE + "__pycache__" + Fore.WHITE,
            Fore.BLUE + "pytree" + Fore.WHITE,
            Fore.GREEN + "python3.8" + Fore.WHITE,
            Fore.WHITE + "requirements.txt" + Fore.WHITE,
            Fore.RED + "activate" + Fore.WHITE,
        )
        for input_name, output_name, color in zip(
            input_text, output_text, colorize_values
        ):
            self.assertEqual(output_name, colorize(color, input_name))

    def test_string_generation_name(self):
        """
        Tests that the proper filenames are produced
        """
        mock_values = (
            (
                "a/path/to/__pycache__",
                EntryType.DIRECTORY,
                True,
            ),
            ("pytree", EntryType.DIRECTORY, False),
            ("a/path/to/symlink/python3.8", EntryType.SYMLINK, True),
            ("a/path/to/text/requirements.txt", EntryType.FILE, True),
            ("a/path/to/exec/activate", EntryType.EXECUTABLE, True),
        )
        mocked_entries = []
        for path, type, colorize in mock_values:
            mock = Mock()
            mock.path = path
            mock.type = type
            mocked_entries.append((mock, colorize))
        output_names = (
            Fore.BLUE + "__pycache__" + Fore.WHITE,
            "pytree",
            Fore.GREEN + "python3.8" + Fore.WHITE,
            "requirements.txt",
            Fore.RED + "activate" + Fore.WHITE,
        )
        for name, entry in zip(output_names, mocked_entries):
            self.assertEqual(name, get_name(entry[0], entry[1]))


if __name__ == "__main__":
    main()
