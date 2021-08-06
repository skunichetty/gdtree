from gdtree.app import process_settings_from_args, setup_parser
from unittest import TestCase, main
from unittest.mock import Mock
from argparse import Namespace
from gdtree.utils import Settings


class TestApp(TestCase):
    def test_process_args_none(self):
        """
        Tests that args are correctly processed into settings
        """
        mocked_args = Mock(spec=Namespace)
        mocked_args.colorize = False
        mocked_args.fancy = False
        mocked_args.reverse = False
        settings = Settings(0)
        output = process_settings_from_args(mocked_args)
        self.assertEqual(settings, output)

    def test_process_args_colorize(self):
        """
        Tests that args are correctly processed into settings when
        colorize is enabled
        """
        mocked_args = Mock(spec=Namespace)
        mocked_args.colorize = True
        mocked_args.fancy = False
        mocked_args.reverse = False
        settings = Settings(0)
        settings |= Settings.COLORIZE
        output = process_settings_from_args(mocked_args)
        self.assertEqual(settings, output)

    def test_process_args_fancy(self):
        """
        Tests that args are correctly processed into settings when
        fancy is enabled
        """
        mocked_args = Mock(spec=Namespace)
        mocked_args.colorize = False
        mocked_args.fancy = True
        mocked_args.reverse = False
        settings = Settings(0)
        settings |= Settings.FANCY
        output = process_settings_from_args(mocked_args)
        self.assertEqual(settings, output)

    def test_process_args_fancy(self):
        """
        Tests that args are correctly processed into settings when
        reverse is enabled
        """
        mocked_args = Mock(spec=Namespace)
        mocked_args.colorize = False
        mocked_args.fancy = False
        mocked_args.reverse = True
        settings = Settings(0)
        settings |= Settings.REVERSE
        output = process_settings_from_args(mocked_args)
        self.assertEqual(settings, output)

    def test_process_args_all(self):
        """
        Tests that args are correctly processed into settings when
        all settings are enabled
        """
        mocked_args = Mock(spec=Namespace)
        mocked_args.colorize = False
        mocked_args.fancy = False
        mocked_args.reverse = True
        settings = Settings(0)
        settings |= Settings.REVERSE
        output = process_settings_from_args(mocked_args)
        self.assertEqual(settings, output)

    def test_parser_all(self):
        """
        Tests that the argument parser setup by setup_parser() correctly parses arguments
        and options
        """
        args = ["directory", "-n", "-f", "-r"]
        parser = setup_parser()
        output = parser.parse_args(args)
        self.assertEqual(output.directory, "directory")
        self.assertFalse(output.colorize)
        self.assertTrue(output.fancy)
        self.assertTrue(output.reverse)

    def test_parser_no_options(self):
        """
        Tests that the argument parser setup by setup_parser() correctly parses when there are
        no options
        """
        args = ["directory"]
        parser = setup_parser()
        output = parser.parse_args(args)
        self.assertEqual(output.directory, "directory")
        self.assertTrue(output.colorize)
        self.assertFalse(output.fancy)
        self.assertFalse(output.reverse)

    def test_parser_dncolorize(self):
        """
        Tests that the argument parser setup by setup_parser() correctly parses arguments and options
        when only --dncolorize is specified
        """
        args = ["directory", "--dncolorize"]
        parser = setup_parser()
        output = parser.parse_args(args)
        self.assertEqual(output.directory, "directory")
        self.assertFalse(output.colorize)
        self.assertFalse(output.fancy)
        self.assertFalse(output.reverse)

    def test_parser_fancy(self):
        """
        Tests that the argument parser setup by setup_parser() correctly parses arguments and options
        when only --fancy is specified
        """
        args = ["directory", "--fancy"]
        parser = setup_parser()
        output = parser.parse_args(args)
        self.assertEqual(output.directory, "directory")
        self.assertTrue(output.colorize)
        self.assertTrue(output.fancy)
        self.assertFalse(output.reverse)

    def test_parser_reverse(self):
        """
        Tests that the argument parser setup by setup_parser() correctly parses arguments and options
        when only --reverse is specified
        """
        args = ["directory", "--reverse"]
        parser = setup_parser()
        output = parser.parse_args(args)
        self.assertEqual(output.directory, "directory")
        self.assertTrue(output.colorize)
        self.assertFalse(output.fancy)
        self.assertTrue(output.reverse)

    def test_parser_error(self):
        """
        Tests that the argument parser setup by setup_parser() throws an error when no directory agrument is given
        """
        args = ["--reverse"]
        parser = setup_parser()
        with self.assertRaises(SystemExit) as exit:
            output = parser.parse_args(args)
        self.assertEqual(exit.exception.code, 2)


if __name__ == "__main__":
    main()
