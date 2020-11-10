"""Utilities for CS 118 Project 1.

Functions:
    compare(f1:str,f2:str) -> bool
    allFiles(directory:str) -> []
"""
from filecmp import cmp
from os import walk, mkdir, remove, rmdir
from os.path import join

__all__ = ['compare', 'all_files']


def compare(f1, f2):
    """Compare the files f1 and f2, returning True if the files are the same, False otherwise."""
    return cmp(f1, f2, False)


def all_files(directory):
    """ returns a list, containing all files, found in the given directory structure."""
    file_list = []
    for root, dirs, files in walk(directory, topdown=False):
        for name in files:
            file_list.append(join(root, name))
    return file_list


def _write_into_file(file_path, content):
    with open(file_path, "w") as fh:
        fh.write(content)


def _test():
    # quick test
    dir_name = "tmp123"
    content = "The quick brown fox jumps over the lazy dog"
    mkdir(dir_name)
    _write_into_file(join(dir_name, "f1"), content)
    _write_into_file(join(dir_name, "f2"), content)
    _write_into_file(join(dir_name, "f3"), content * 2)

    assert 3 == len(all_files(dir_name)) == 3
    assert compare(join(dir_name, "f1"), join(dir_name, "f2"))
    assert not compare(join(dir_name, "f1"), join(dir_name, "f3"))

    remove(join(dir_name, "f1"))
    remove(join(dir_name, "f2"))
    remove(join(dir_name, "f3"))
    rmdir(dir_name)
    print("test passed")


if __name__ == '__main__':
    _test()
