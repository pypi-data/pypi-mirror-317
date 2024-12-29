import os
import pytest
import sys

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from gimi9_tree_view.treeview import Tree


@pytest.fixture
def setup_test_directory():
    test_dir = "test_dir"
    os.makedirs(test_dir, exist_ok=True)
    with open(os.path.join(test_dir, "file1.txt"), "w") as f:
        f.write("test file 1")
    os.makedirs(os.path.join(test_dir, "subdir"), exist_ok=True)
    with open(os.path.join(test_dir, "subdir", "file2.txt"), "w") as f:
        f.write("test file 2")
    yield test_dir
    for root, dirs, files in os.walk(test_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(test_dir)


def test_register(setup_test_directory):
    tree = Tree()
    tree.register(os.path.join(setup_test_directory, "file1.txt"))
    tree.register(os.path.join(setup_test_directory, "subdir"))
    assert tree.fileCount == 1
    assert tree.dirCount == 1


def test_summary(setup_test_directory):
    tree = Tree()
    tree.register(os.path.join(setup_test_directory, "file1.txt"))
    tree.register(os.path.join(setup_test_directory, "subdir"))
    summary = tree.summary()
    assert summary == "1 directories, 1 files"


def test_walk(setup_test_directory):
    tree = Tree()
    tree.walk(setup_test_directory)
    assert tree.fileCount == 2
    assert tree.dirCount == 2
