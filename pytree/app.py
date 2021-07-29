import os
from sys import platform
from pytree.traverse import traverse
from colorama import init
from pytree.filestring import generate_filestring
from pytree.entry_type import EntryType


def start():
    if platform == "win32" or platform == "cygwin":
        # initialize colorama since we need to escape ANSI characters
        # for use on Windows
        init()
    file_count = 0
    dir_count = 0
    print(os.path.basename(os.getcwd()))
    for it in traverse(os.getcwd()):
        print(generate_filestring(it, True))
        if it.type == EntryType.FILE or it.type == EntryType.EXECUTABLE:
            file_count += 1
        if it.type == EntryType.DIRECTORY:
            dir_count += 1
    print("Files: %d, Directories: %d" % (file_count, dir_count))
