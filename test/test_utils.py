from gdtree.utils import EntryType, get_type
from unittest import TestCase, main
from unittest.mock import Mock, patch
from os import DirEntry


class TestTypeExtraction(TestCase):
    """
    Tests the ability to extract type from DirEntry objects returned by os.scandir().
    """

    @patch("gdtree.utils.access")
    def test_type_extraction_is_dir(self, mocked_access):
        """
        Tests that entry type is extracted when it is a directory
        """
        mock = Mock(spec=DirEntry)
        mock.is_dir.return_value = True
        mock.is_symlink.return_value = False

        # editing patched os module
        mocked_access.return_value = False
        type = get_type(mock)
        mock.is_dir.assert_called_once()
        self.assertEqual(type, EntryType.DIRECTORY)

    @patch("gdtree.utils.access")
    def test_type_extraction_is_dir_error(self, mocked_access):
        """
        Tests that testing for directory has errors handled to
        confirm nonexistence of directory
        """
        mock = Mock(spec=DirEntry)
        mock.is_dir.side_effect = OSError("")
        mock.is_symlink.return_value = False

        mocked_access.return_value = False

        type = get_type(mock)
        self.assertEqual(type, EntryType.FILE)

    @patch("gdtree.utils.access")
    def test_type_extraction_is_file(self, mocked_access):
        """
        Tests that entry type is extracted when it is a file
        """
        mock = Mock(spec=DirEntry)
        mock.is_dir.return_value = False
        mock.is_symlink.return_value = False

        mocked_access.return_value = False

        type = get_type(mock)
        self.assertEqual(type, EntryType.FILE)

    @patch("gdtree.utils.access")
    def test_type_extraction_is_symlink(self, mocked_access):
        """
        Tests that entry type is extracted when it is a symbolic link
        """
        mock = Mock(spec=DirEntry)
        mock.is_dir.return_value = False
        mock.is_symlink.return_value = True

        # editing patched os module
        mocked_access.return_value = False
        type = get_type(mock)
        mock.is_symlink.assert_called_once()
        self.assertEqual(type, EntryType.SYMLINK)

    @patch("gdtree.utils.access")
    def test_type_extraction_is_symlink_to_dir(self, mocked_access):
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
        mocked_access.return_value = False

        type = get_type(mock)
        mock.is_symlink.assert_called_once()
        mock.is_dir.assert_not_called()
        assert type == EntryType.SYMLINK

    @patch("gdtree.utils.access")
    def test_type_extraction_is_symlink_error(self, mocked_access):
        """
        Tests that testing for directory has errors handled to
        confirm nonexistence of directory
        """
        mock = Mock(spec=DirEntry)
        mock.is_dir.return_value = False
        mock.is_symlink.side_effect = OSError("")

        mocked_access.return_value = False

        type = get_type(mock)
        assert type == EntryType.FILE

    @patch("gdtree.utils.access")
    def test_type_extraction_is_executable(self, mocked_access):
        """
        Tests that entry type is extracted when it is an executable
        """
        mock = Mock(spec=DirEntry)
        mock.is_dir.return_value = False
        mock.is_symlink.return_value = False

        mocked_access.return_value = True

        assert get_type(mock) == EntryType.EXECUTABLE


if __name__ == "__main__":
    main()
