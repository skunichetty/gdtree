from os.path import basename, abspath
from typing import Generator, Tuple, List
from gdtree.traverse import reverse_traverse_directory, traverse_directory
from colorama import init
from gdtree.filestring import create_filestring_builder, type_colorize
from gdtree.utils import EntryType, Settings
from argparse import Namespace, ArgumentParser


def start():
    """
    The starting function for the tree generation.
    """
    init()
    start_dir, settings = parse_settings()
    gen = generate_tree(start_dir, settings)
    print("\n".join(gen))


def generate_tree(
    directory: str, settings: Settings
) -> Generator[str, None, None]:
    """
    Generates the pretty-printed tree

    Args:
        directory (str): The directory for which to print the tree for
        settings (Settings): Print settings

    Yields:
        Generator[str, None, None]: Generator of pretty-printed tree strings.
    """
    num_dir, num_files = 0, 0

    filestring_builder = create_filestring_builder(settings)
    if settings & Settings.REVERSE:
        traverse = reverse_traverse_directory
    else:
        traverse = traverse_directory

    dir_name = basename(directory)
    if settings & Settings.COLORIZE:
        formatted_name = type_colorize(dir_name, EntryType.DIRECTORY)
    else:
        formatted_name = dir_name
    yield formatted_name

    for path, type, history in traverse(directory):
        if type == EntryType.DIRECTORY:
            num_dir += 1
        else:
            num_files += 1
        yield filestring_builder(path, type, history)
    yield "%d directories, %d files" % (num_dir, num_files)


def parse_settings(input_args: List[str] = None) -> Tuple[str, Settings]:
    """
    Parses settings from command line.

    Args:
        input_args (List[str], optional): Arguments to parse. Defaults to None.

    Returns:
        Tuple[str, Settings]: The start directory for the tree generation and
        the generation settings object
    """
    parser = setup_parser()
    if input_args is not None:
        args = parser.parse_args(input_args)
    else:
        args = parser.parse_args()
    settings = process_settings_from_args(args)
    directory = abspath(args.directory)
    return directory, settings


def process_settings_from_args(args: Namespace) -> Settings:
    """
    Return a Settings object from the arguments given from argparse.

    Args:
        args (Namespace): The arguments returned from ArgumentParser.parse_args()

    Returns:
        Settings: The corresponding settings
    """
    settings = Settings(0)
    if args.colorize:
        settings |= Settings.COLORIZE
    if args.fancy:
        settings |= Settings.FANCY
    if args.reverse:
        settings |= Settings.REVERSE
    return settings


def setup_parser() -> ArgumentParser:
    """
    Initializes an ArgumentParser to correctly parse user options for this application

    Returns:
        ArgumentParser: The argument parser object
    """
    parser = ArgumentParser(
        prog="gdtree", description="Produces a pretty-printed directory tree"
    )
    parser.add_argument(
        "directory",
        help="Path to the top-level directory to generate a tree from. Can be absolute or relative",
        type=str,
    )
    parser.add_argument(
        "-n",
        "--dncolorize",
        dest="colorize",
        help="Disables output colorization",
        action="store_false",
    )
    parser.add_argument(
        "-f",
        "--fancy",
        dest="fancy",
        help="Prints tree with fancy box chars (ex. ╠══ instead of ├── )",
        action="store_true",
    )
    parser.add_argument(
        "-r",
        "--reverse",
        dest="reverse",
        help="Reverses alphabetical order of print",
        action="store_true",
    )
    return parser
