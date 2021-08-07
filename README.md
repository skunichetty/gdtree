# gdtree

gdtree is a directory tree generator built with Python.

## Description

gdtree provides easy directory tree generation. This command-line tool is inspired by the classic UNIX _tree_ utility.

Suppose that a given directory has the folder structure below

```
top_folder
|-- another_folder
|   |-- link_to_file_2
|--lower_folder
|   |-- secrets.py
|-- file_1.py
|-- file_2.txt
|-- file_3.json
|-- special_script.sh
```

where

-   _link_to_file_2_ is a symbolic link
-   _special_script.sh_ has execute privileges (for the current user)

gdtree will produce the following output when called on this directory

![A picture of gdtree output](https://raw.githubusercontent.com/skunichetty/gdtree/main/screenshots/linux_screenshot.png)

The directory is pretty-printed using unicode box characters, and is colorized based on the file type.

## Usage

gdtree can be easily installed using pip

```bash
pip install gdtree
```

To generate a directory tree for the current directory, enter the command

```bash
gdtree .
```

An absolute path can be used in place of the relative path to generate a directory tree for any directory

## Options

gdtree comes with options to provide information and customize some features of the tree generation:

-   `-h, --help` - Prints a help message containing usage details
-   `-n, --dncolorize` - Disables output colorization
-   `-f, --fancy` - Prints tree using fancy box characters (uses ╠══ instead of ├──)
-   `-r, --reverse` - Prints tree in reverse alphabetical order
