from pytree.entry_type import EntryType
from unittest import TestCase, main
from unittest.mock import Mock, patch
from pytree.utils import get_type
from os import DirEntry


class TestTypeExtraction(TestCase):
    """
    Tests the ability to extract type from DirEntry objects returned by os.scandir().
    """

    @patch("pytree.utils.os")
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

    @patch("pytree.utils.os")
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

    @patch("pytree.utils.os")
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

    @patch("pytree.utils.os")
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

    @patch("pytree.utils.os")
    def test_type_extraction_is_symlink_to_dir(self, mocked_os):
        """
        Tests that entry type is symbolic link even if to dir. Python is_dir() will return true if it is
        a symlink that points to a directory, so we want to read if its a symlink before read if its
        a directory

        Note: This test is invalidated with new changes in implementation,
        but is left in as a reminder of this potential bug
        """
        mock = Mock(spec=DirEntry)
        mock.is_dir.return_value = False
        mock.is_symlink.return_value = True
        mocked_os.access.return_value = False

        type = get_type(mock)
        assert type == EntryType.SYMLINK

    @patch("pytree.utils.os")
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

    @patch("pytree.utils.os")
    def test_type_extraction_is_executable(self, mocked_os):
        """
        Tests that entry type is extracted when it is an executable
        """
        mock = Mock(spec=DirEntry)
        mock.is_dir.return_value = False
        mock.is_symlink.return_value = False

        mocked_os.access.return_value = True

        assert get_type(mock) == EntryType.EXECUTABLE


if __name__ == "__main__":
    main()
