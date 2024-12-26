import sys
import os
import argparse
from tree import Tree

"""
github의 오픈소스 참고.
https://github.com/kddnewton/tree
https://github.com/kddnewton/tree/blob/main/tree.py
"""

if __name__ == "__main__":

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

    tree = Tree()
    tree.walk(args.directory)

    # print("\n" + tree.summary())
