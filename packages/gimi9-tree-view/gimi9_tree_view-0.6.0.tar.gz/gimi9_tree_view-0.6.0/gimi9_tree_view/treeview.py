import sys
import os
import argparse
from wcwidth import wcswidth

"""
This script is inspired by the open-source project available at:
https://github.com/kddnewton/tree
https://github.com/kddnewton/tree/blob/main/tree.py
"""


DIRS_ONLY = False
LEVEL = -1
MAX_FILES = 4
PRINT_FILES_FIRST = False


def human_readable_size(size):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.0f}{unit}"
        size /= 1024


def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


class Tree:
    def __init__(self):
        self.dirCount = 0
        self.fileCount = 0

    def register(self, absolute):
        if os.path.isdir(absolute):
            self.dirCount += 1
        else:
            self.fileCount += 1

    def summary(self):
        return str(self.dirCount) + " directories, " + str(self.fileCount) + " files"

    def walk(self, directory, prefix="", depth=0, is_root=True):  # , num_files=0):
        if LEVEL > -1 and depth > LEVEL:
            return

        if is_root:
            all_filepaths = ["."]
        else:
            all_filepaths = sorted(os.listdir(directory))

        dir_only_paths = [
            filepath
            for filepath in all_filepaths
            if os.path.isdir(os.path.join(directory, filepath))
            and filepath
            not in ["__MACOSX", "venv", ".git", ".idea", "node_modules", "__pycache__"]
            and (
                filepath == "." or not filepath.startswith(".")
            )  # Exclude hidden directories starting with "."
        ]
        file_only_paths = self.list_files(directory, all_filepaths)

        if DIRS_ONLY:
            filepaths = dir_only_paths
        else:
            if PRINT_FILES_FIRST:  # Print files first and then directories
                filepaths = file_only_paths[:MAX_FILES] + dir_only_paths
            else:  # Print directories first and then files
                filepaths = dir_only_paths + file_only_paths[:MAX_FILES]

        for index in range(len(filepaths)):
            absolute = os.path.join(directory, filepaths[index])
            is_dir_path = os.path.isdir(absolute)
            if is_dir_path:
                # print directory
                emoji = "📂"
                num_files = len(self.list_files(absolute, os.listdir(absolute)))
                s = "s" if num_files > 1 else ""
                file_count_str = f", {num_files:,} File{s}" if num_files > 0 else ""
                dir_size = get_directory_size(absolute)
                dir_size_str = f"{human_readable_size(dir_size)}"

                if is_root:
                    directory_title = os.path.basename(os.path.normpath(directory))
                else:
                    directory_title = filepaths[index]

                paddding = self.get_padding(prefix, is_root, directory_title)

                # color = "0;34m"  # blue
                color = "1;34m"  # bold blue
                # color = "4;34m"  # underline blue
                # color = "1;94m"  # bodl High Intensity blue

                formatted_output = f"{emoji} \033[{color}{directory_title}{' ' * paddding} [{dir_size_str}{file_count_str}]\033[0m"
            else:
                # file 출력
                emoji = "📄"
                file_count_str = ""
                dir_size_str = f"{human_readable_size(os.path.getsize(absolute))}"

                paddding = self.get_padding(prefix, False, filepaths[index])

                formatted_output = (
                    f"{emoji} {filepaths[index]}{' ' * paddding} [{dir_size_str}]"
                )

            self.register(absolute)

            if index == len(filepaths) - 1:  # If it is the last item
                if PRINT_FILES_FIRST and not is_dir_path:
                    print(f"{prefix}{'' if is_root else '  '} {formatted_output}")
                else:
                    print(f"{prefix}{'' if is_root else '└──'} {formatted_output}")
                new_prefix = prefix + "    "
            else:
                if PRINT_FILES_FIRST and not is_dir_path:
                    if dir_only_paths:
                        print(f"{prefix}{'' if is_root else '│  '} {formatted_output}")
                    else:
                        print(f"{prefix}   {formatted_output}")
                else:
                    print(f"{prefix}├── {formatted_output}")
                new_prefix = prefix + "│   "

            if is_dir_path:
                self.walk(
                    absolute,
                    new_prefix,
                    depth=depth + 1,
                    is_root=False,
                )

    def list_files(self, directory, all_filepaths):
        return [
            filepath
            for filepath in all_filepaths
            if not os.path.isdir(os.path.join(directory, filepath))
            and filepath not in ("_.DS_Store", ".DS_Store")
            and filepath[0] != "."  # Exclude hidden files
        ]

    def get_padding(self, prefix, is_root, directory_title):
        paddding = 40 - (
            wcswidth(prefix) + len("" if is_root else "└──") + len(directory_title)
        )

        return paddding


def main():
    parser = argparse.ArgumentParser(
        description="List directory contents.",
        epilog="github: https://github.com/gisman/tree-view",
    )

    # Option to list directories only
    parser.add_argument("directory", help="Directory to read")
    parser.add_argument(
        "-d", action="store_true", help="List directories only", default=False
    )

    # Option to limit the output depth. Default is -1
    parser.add_argument(
        "-L",
        "--level",
        type=int,
        help="Descend only level directories deep",
        default=-1,
    )

    # Option to print only up to N files in each directory. Default is 4
    parser.add_argument(
        "-n",
        "--max-files",
        type=int,
        help="Print only N files in each directory",
        default=4,
    )

    # Option to print files before directories
    parser.add_argument(
        "-f",
        "--files-first",
        action="store_true",
        help="Print files before directories",
        default=False,
    )

    args = parser.parse_args()

    global DIRS_ONLY
    global LEVEL
    global MAX_FILES
    global PRINT_FILES_FIRST

    DIRS_ONLY = args.d
    LEVEL = args.level
    if args.max_files < 0:
        MAX_FILES = 1000000  # Limit to 1 million
    else:
        MAX_FILES = args.max_files

    PRINT_FILES_FIRST = args.files_first

    # check if the directory exists
    if not os.path.isdir(args.directory):
        print("The directory does not exists.")
        sys.exit

    t = Tree()
    t.walk(args.directory)

    # print("\n" + tree.summary())


if __name__ == "__main__":
    main()
