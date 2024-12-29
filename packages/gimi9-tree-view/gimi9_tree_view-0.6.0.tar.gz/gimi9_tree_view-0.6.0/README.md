# Gimi9 Tree View

Improved version of the Linux tree utility.

Includes features useful for big data analysis and documentation.

Written for Python 3.12.3, works on Python 3.10 and above. It is expected to work on Python 3.2 and above.

## Features

* Tree structure output
* Size: human-readable
* File count
* File list limit
* Pretty diretory emoji 📂

* Note: Automatically excludes hidden files.

## Installation

> $ pip install gimi9_tree_view

## Usage

### Print help

> $ treeview -h

```
usage: treeview [-h] [-d] [-L LEVEL] [-n MAX_FILES] [-f] directory

List directory contents.

positional arguments:
  directory             Directory to read

options:
  -h, --help            show this help message and exit
  -d                    List directories only
  -L LEVEL, --level LEVEL
                        Descend only level directories deep
  -n MAX_FILES, --max-files MAX_FILES
                        Print only N files in each directory
  -f, --files-first     Print files before directories

github: https://github.com/gisman/tree-view
```

### Default

Full depth directory listing, 4 files per directory by default.

> $ treeview gimi9_tree_view

```
 📂 gimi9_tree_view                          [70MB, 9 Files]
    ├── 📂 build                             [12KB]
    │   ├── 📂 bdist.linux-x86_64            [0B]
    │   └── 📂 lib                           [12KB]
    │       └── 📂 gimi9_tree_view           [12KB, 3 Files]
    │           ├── 📄 __init__.py           [0B]
    │           ├── 📄 tree.py               [5KB]
    │           └── 📄 treeview.py           [7KB]
    ├── 📂 dist                              [19KB, 2 Files]
    │   ├── 📄 gimi9_tree_view-0.5.3-py3-none-any.whl [10KB]
    │   └── 📄 gimi9_tree_view-0.5.3.tar.gz  [8KB]
    ├── 📂 gimi9_tree_view                   [15KB, 2 Files]
    │   ├── 📄 __init__.py                   [0B]
    │   └── 📄 treeview.py                   [7KB]
    ├── 📂 gimi9_tree_view.egg-info          [5KB, 6 Files]
    │   ├── 📄 PKG-INFO                      [4KB]
    │   ├── 📄 SOURCES.txt                   [318B]
    │   ├── 📄 dependency_links.txt          [1B]
    │   └── 📄 entry_points.txt              [59B]
    ├── 📂 tests                             [4KB, 1 File]
    │   └── 📄 test_treeview.py              [1KB]
    ├── 📂 tree_view.egg-info                [4KB, 5 Files]
    │   ├── 📄 PKG-INFO                      [4KB]
    │   ├── 📄 SOURCES.txt                   [190B]
    │   ├── 📄 dependency_links.txt          [1B]
    │   └── 📄 requires.txt                  [87B]
    ├── 📄 CONTRIBUTING.md                   [2KB]
    ├── 📄 LICENSE                           [11KB]
    ├── 📄 Main_slow_UNUSED.py               [5KB]
    └── 📄 README.md                         [5KB]
```

### List directories only

> $ treeview -d gimi9_tree_view

```
 📂 gimi9_tree_view                          [70MB, 9 Files]
    ├── 📂 build                             [12KB]
    │   ├── 📂 bdist.linux-x86_64            [0B]
    │   └── 📂 lib                           [12KB]
    │       └── 📂 gimi9_tree_view           [12KB, 3 Files]
    ├── 📂 dist                              [19KB, 2 Files]
    ├── 📂 gimi9_tree_view                   [15KB, 2 Files]
    ├── 📂 gimi9_tree_view.egg-info          [5KB, 6 Files]
    ├── 📂 tests                             [4KB, 1 File]
    └── 📂 tree_view.egg-info                [4KB, 5 Files]
```

### Directory depth limit

Print directories only with the -d option and limit depth to 1 level

> $ treeview -d -L 1 gimi9_tree_view
```
 📂 gimi9_tree_view                          [70MB, 9 Files]
    ├── 📂 build                             [12KB]
    ├── 📂 dist                              [19KB, 2 Files]
    ├── 📂 gimi9_tree_view                   [15KB, 2 Files]
    ├── 📂 gimi9_tree_view.egg-info          [5KB, 6 Files]
    ├── 📂 tests                             [4KB, 1 File]
    └── 📂 tree_view.egg-info                [4KB, 5 Files]
```

### File List limit
Print 2 files per directory. Specify -1 to print the entire file list.

> $ treeview -n 2 gimi9_tree_view
```
 📂 gimi9_tree_view                          [70MB, 9 Files]
    ├── 📂 build                             [12KB]
    │   ├── 📂 bdist.linux-x86_64            [0B]
    │   └── 📂 lib                           [12KB]
    │       └── 📂 gimi9_tree_view           [12KB, 3 Files]
    │           ├── 📄 __init__.py           [0B]
    │           └── 📄 tree.py               [5KB]
    ├── 📂 dist                              [19KB, 2 Files]
    │   ├── 📄 gimi9_tree_view-0.5.3-py3-none-any.whl [10KB]
    │   └── 📄 gimi9_tree_view-0.5.3.tar.gz  [8KB]
    ├── 📂 gimi9_tree_view                   [15KB, 2 Files]
    │   ├── 📄 __init__.py                   [0B]
    │   └── 📄 treeview.py                   [7KB]
    ├── 📂 gimi9_tree_view.egg-info          [5KB, 6 Files]
    │   ├── 📄 PKG-INFO                      [4KB]
    │   └── 📄 SOURCES.txt                   [318B]
    ├── 📂 tests                             [4KB, 1 File]
    │   └── 📄 test_treeview.py              [1KB]
    ├── 📂 tree_view.egg-info                [4KB, 5 Files]
    │   ├── 📄 PKG-INFO                      [4KB]
    │   └── 📄 SOURCES.txt                   [190B]
    ├── 📄 CONTRIBUTING.md                   [2KB]
    └── 📄 LICENSE                           [11KB]
```
