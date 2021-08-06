from unittest import TestCase, main
from gdtree.filestring import (
    create_filestring_builder,
    get_filestring_color,
    type_colorize,
    _get_prefix,
    build_prefix,
    build_fancy_prefix,
)
from gdtree.utils import EntryType, Settings
from colorama import Fore
from gdtree.end_state_history import EndStateHistory


class TestFilestring(TestCase):
    def test_get_color_directory(self):
        """
        Tests that colors corresponding to a directory are properly generated
        """
        self.assertEqual(Fore.CYAN, get_filestring_color(EntryType.DIRECTORY))

    def test_get_color_symlink(self):
        """
        Tests that colors corresponding to a symbolic link are properly generated
        """
        self.assertEqual(Fore.GREEN, get_filestring_color(EntryType.SYMLINK))

    def test_get_color_executable(self):
        """
        Tests that colors corresponding to an executable are properly generated
        """
        self.assertEqual(Fore.RED, get_filestring_color(EntryType.EXECUTABLE))

    def test_get_color_file(self):
        """
        Tests that colors corresponding to a file are properly generated
        """
        self.assertEqual(Fore.WHITE, get_filestring_color(EntryType.FILE))

    def test_get_colors_error(self):
        """
        Tests that passing an invalid type raises a value error
        """
        with self.assertRaises(ValueError):
            color = get_filestring_color("an invalid type")

    def test_colorize(self):
        """
        Tests that text is colorized properly given type
        """
        input_text = "__pycache__"
        input_type = EntryType.DIRECTORY
        output_text = type_colorize(input_text, input_type)
        expected_output = Fore.CYAN + "__pycache__" + Fore.WHITE
        self.assertEqual(output_text, expected_output)

    def test_colorize_file(self):
        """
        Tests that text is colorized properly given file type, in which case
        no colorization should occur (to save on processing)
        """
        input_text = "__pycache__"
        input_type = EntryType.FILE
        output_text = type_colorize(input_text, input_type)
        expected_output = "__pycache__"
        self.assertEqual(output_text, expected_output)

    def test_colorize_error(self):
        """
        Tests that a ValueError is raised when given an invalid type
        """
        input_text = "__pycache__"
        input_type = 0
        with self.assertRaises(ValueError):
            output_text = type_colorize(input_text, input_type)

    def test_get_name(self):
        """
        Tests that the formatted name is properly gotten given input path
        """
        input_path = "a/path/to/a/file"
        pass

    def test_prefix_true(self):
        """
        Tests that the correct prefix is returned from a given prefix set
        when end state is True
        """
        prefix_set = {True: "prefix1", False: "prefix2"}
        output = _get_prefix(True, prefix_set)
        self.assertEqual("prefix1", output)

    def test_prefix_false(self):
        """
        Tests that the correct prefix is returned from a given prefix set
        when end state is False
        """
        prefix_set = {True: "prefix1", False: "prefix2"}
        output = _get_prefix(False, prefix_set)
        self.assertEqual("prefix2", output)

    def test_prefix_error(self):
        """
        Tests that the correct prefix is returned from a given prefix set
        when end state is True
        """
        prefix_set = {True: "prefix1", False: "prefix2"}
        with self.assertRaises(ValueError):
            prefix = _get_prefix("an invalid state", prefix_set)

    def test_prefix_generation_end_false(self):
        """
        Tests that the proper prefix is generated given end state history
        with the most recent state value being False
        """
        history = EndStateHistory([True, False, False, True, True, False])
        output_string = build_prefix(history)
        expected_output = "    │   │           ├── "
        self.assertEqual(output_string, expected_output)

    def test_prefix_generation_end_true(self):
        """
        Tests that the proper prefix is generated given end state history
        with the most recent state value being True
        """
        history = EndStateHistory([True, False, False, True, True, True])
        output_string = build_prefix(history)
        expected_output = "    │   │           └── "
        self.assertEqual(output_string, expected_output)

    def test_prefix_generation_one_entry(self):
        """
        Tests that the proper prefix is generated for a state history with
        only one entry
        """
        history = EndStateHistory([True])
        output_string = build_prefix(history)
        expected_output = "└── "
        self.assertEqual(output_string, expected_output)

    def test_prefix_fancy_generation_end_false(self):
        """
        Tests that a fancy prefix is generated given end state history with
        the most recent state value being False
        """
        history = EndStateHistory([True, False, False, True, True, False])
        output_string = build_fancy_prefix(history)
        expected_output = "    ║   ║           ╠══ "
        self.assertEqual(output_string, expected_output)

    def test_prefix_fancy_generation_end_true(self):
        """
        Tests that a fancy prefix is generated given end state history with
        the most recent state value being True
        """
        history = EndStateHistory([True, False, False, True, True, True])
        output_string = build_fancy_prefix(history)
        expected_output = "    ║   ║           ╚══ "
        self.assertEqual(output_string, expected_output)

    def test_prefix_fancy_generation_one_entry(self):
        """
        Tests that the proper prefix is generated for a state history with
        only one entry
        """
        history = EndStateHistory([True])
        output_string = build_fancy_prefix(history)
        expected_output = "╚══ "
        self.assertEqual(output_string, expected_output)

    def test_filestring_builder_basic(self):
        """
        Tests that the filestring builder is correctly created from default
        settings
        """
        # Item options
        path = "directory"
        type = EntryType.DIRECTORY
        history = EndStateHistory([True, False, False, True, True, True])

        settings = Settings(0)

        generator = create_filestring_builder(settings)
        output = generator(path, type, history)
        expected_output = "    │   │           └── directory"
        self.assertEqual(output, expected_output)

    def test_filestring_builder_colorization(self):
        """
        Tests that the filestring builder is correctly created to colorize
        output string
        """
        # Item options
        path = "directory"
        type = EntryType.DIRECTORY
        history = EndStateHistory([True, False, False, True, True, True])

        settings = Settings(0)
        settings |= Settings.COLORIZE

        generator = create_filestring_builder(settings)
        output = generator(path, type, history)
        expected_output = "    │   │           └── %sdirectory%s" % (
            Fore.CYAN,
            Fore.WHITE,
        )
        self.assertEqual(output, expected_output)

    def test_filestring_builder_fancy(self):
        """
        Tests that the filestring builder is correctly created to make
        output string fancy
        """
        # Item options
        path = "directory"
        type = EntryType.DIRECTORY
        history = EndStateHistory([True, False, False, True, True, True])

        settings = Settings(0)
        settings |= Settings.FANCY

        generator = create_filestring_builder(settings)
        output = generator(path, type, history)
        expected_output = "    ║   ║           ╚══ directory"
        self.assertEqual(output, expected_output)

    def test_filestring_builder_fancy_and_colorized(self):
        """
        Tests that the filestring builder is correctly created to make
        output string both fancy and colorized
        """
        # Item options
        path = "directory"
        type = EntryType.DIRECTORY
        history = EndStateHistory([True, False, False, True, True, True])

        settings = Settings(0)
        settings |= Settings.FANCY
        settings |= Settings.COLORIZE

        generator = create_filestring_builder(settings)
        output = generator(path, type, history)
        expected_output = "    ║   ║           ╚══ %sdirectory%s" % (
            Fore.CYAN,
            Fore.WHITE,
        )
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    main()
