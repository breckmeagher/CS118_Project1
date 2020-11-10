"""
    Searches deep inside a directory structure, looking for duplicate file.
    Duplicates aka copies have the same content, but not necessarily the same name.
"""
__author__ = "Breck Meagher"
__email__ = "meagherb@my.erau.edu"
__version__ = "1.0"

# noinspection PyUnresolvedReferences
from os.path import getsize, join
from time import time

# noinspection PyUnresolvedReferences
from p1utils import all_files, compare


def search(file_list):
    """Looking for duplicate files in the provided list of files
    :returns a list of lists, where each list contains files with the same content

    Basic search strategy goes like this:
    - until the provided list is empty.
    - remove the 1st item from the provided file_list
    - search for its duplicates in the remaining list and put the item and all its duplicates into a new list
    - if that new list has more than one item (i.e. we did find duplicates) save the list in the list of lists
    As a result we have a list, each item of that list is a list,
    each of those lists contains files that have the same content
    """
    lol = []
    while 0 < len(file_list):
        """
        Removes the first item from the list of every file and compares it against
        every single file in the file list. Adds it to a list of duplicates, then
        the list of duplicates is added to the list of lists
        """
        duplicates = [file_list.pop(0)]
        for i in range(len(file_list) - 1, -1, -1):
            if compare(duplicates[0], file_list[i]):
                duplicates.append(file_list.pop(i))
        if 1 < len(duplicates):
            lol.append(duplicates)
    return lol


def faster_search(file_list):
    """Looking for duplicate files in the provided list of files
    :returns a list of lists, where each list contains files with the same content

    Here's an idea: executing the compare() function seems to take a lot of time.
    Therefore, let's optimize and try to call it a little less often.
    """
    lol = []
    file_sizes = list(map(getsize, file_list))
    duplicates = list(filter(lambda x: 1 < file_sizes.count(getsize(x)), file_list))
    for i in duplicates:
        """
        After creating a list of files with duplicate file sizes, compare among this much
        smaller list and appended similarly to search(), creating another list of lists
        """
        copies = [x for x in duplicates if compare(i, x)]
        if 1 < len(copies):
            lol.append(copies)

    return lol


def report(lol):
    """ Prints a report
    :param lol: list of lists (each containing files with equal content)
    :return: None
    Prints a report:
    - longest list, i.e. the files with the most duplicates
    - list where the items require the largest amount or disk-space
    """
    if len(lol) > 0:
        print(f"== == Duplicate File Finder Report == == \n")

        most_copies = list(max(lol, key=lambda x: len(x)))
        print(f"The file with the most duplicates is {most_copies[0]} \n")
        most_copies.pop(0)  # Most straightforward, readable way to reference the list without the first item
        print(f"Here are it's {len(most_copies)} copies:", *most_copies, sep="\n")

        file_sizes = list(max(lol, key=lambda x: sum([getsize(n) for n in x])))  # Adds up file sizes
        print(f"\n The most disk space {sum([getsize(n) for n in file_sizes])} could be recovered by"
              f"deleting copies of this file:{file_sizes[0]}")
        file_sizes.pop(0)
        print(f"\n Here are its {len(file_sizes)} copies:", *file_sizes, sep="\n")
    else:
        print("No duplicates found")


if __name__ == '__main__':
    path = join(".", "images")
    # measure how long the search and reporting takes:
    t0 = time()
    report(search(all_files(path)))
    print(f"\n Runtime: {time() - t0:.2f} seconds")

    print("\n\n .. and now with a faster search implementation:")

    # measure how long the search and reporting takes:
    t0 = time()
    report(faster_search(all_files(path)))
    print(f"Runtime: {time() - t0:.2f} seconds")
