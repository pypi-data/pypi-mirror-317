import sys
import os
import argparse
from wcwidth import wcswidth

"""
github의 오픈소스 참고.
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

    # def print_root(self, args.directory):

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
            and filepath not in ["__MACOSX", "venv", ".git", ".idea", "node_modules"]
        ]
        file_only_paths = self.list_files(directory, all_filepaths)

        if DIRS_ONLY:
            filepaths = dir_only_paths
        else:
            if PRINT_FILES_FIRST:  # 파일을 먼저 출력하고 디렉토리를 출력
                filepaths = file_only_paths[:MAX_FILES] + dir_only_paths
            else:  # 디렉토리를 먼저 출력하고 파일을 출력
                filepaths = dir_only_paths + file_only_paths[:MAX_FILES]

        for index in range(len(filepaths)):
            # if filepaths[index][0] == ".":
            #     continue

            absolute = os.path.join(directory, filepaths[index])
            is_dir_path = os.path.isdir(absolute)
            if is_dir_path:
                # directory 출력
                emoji = "📂"
                # num_files = len(
                #     [
                #         f
                #         for f in os.listdir(absolute)
                #         if os.path.isfile(os.path.join(absolute, f))
                #     ]
                # )
                num_files = len(self.list_files(absolute, os.listdir(absolute)))
                file_count_str = f" {num_files:,}개의 파일" if num_files > 0 else ""
                dir_size = get_directory_size(absolute)
                dir_size_str = f"{human_readable_size(dir_size)}"

                if is_root:
                    directory_title = os.path.basename(os.path.normpath(directory))
                else:
                    directory_title = filepaths[index]

                paddding = self.get_padding(prefix, is_root, directory_title)

                formatted_output = f"{emoji} {directory_title}{' ' * paddding} [{dir_size_str}{file_count_str}]"
            else:
                # file 출력
                emoji = "📄"
                file_count_str = ""
                dir_size_str = f"{human_readable_size(os.path.getsize(absolute))}"
                formatted_output = f"{emoji} {filepaths[index]} [{dir_size_str}]"

            self.register(absolute)

            if index == len(filepaths) - 1:  # 마지막 항목인 경우
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
            and filepath[0] != "."  # 숨김파일 제외
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

    # 디렉토리만 출력하는 옵션
    parser.add_argument("directory", help="Directory to read")
    parser.add_argument(
        "-d", action="store_true", help="List directories only", default=False
    )

    # 출력 Depth를 제한하는 옵션. 기본값은 -1
    parser.add_argument(
        "-L",
        "--level",
        type=int,
        help="Descend only level directories deep",
        default=-1,
    )

    # 디렉토리 내의 파일을 최대 N개 까지만 출력하는 옵션. 기본값은 4
    parser.add_argument(
        "-n",
        "--max-files",
        type=int,
        help="Print only N files in each directory",
        default=4,
    )

    # 파일을 먼저 출력하고 디렉토리를 출력하는 옵션
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
        MAX_FILES = 1000000  # 100만개로 제한
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
