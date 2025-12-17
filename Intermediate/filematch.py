#! /usr/bin/env python3.13
'''
We love it when CLI or web apps take the extra mile to be more user friendly. In
this Bite you will tweak the user experience of a function yourself.

Have you noticed how Django's migrate.py helps you type in the right command?
$ python manage.py migrat
Unknown command: 'migrat'. Did you mean migrate?
Type 'manage.py help' for usage.

Using Python's difflib this is actually not that hard to implement. Let's roll
our own using another theme: file matching.

Complete the get_matching_files function below. It takes a target directory Path
object and filter_str str to match (case insensitive). If any files match
exactly, return a list with matches. If there is no exact match, see if there
are closely matching files and return those. If no closely matching files
either, return an empty list.
'''


from collections import defaultdict
from collections.abc import Iterable
from difflib import SequenceMatcher, get_close_matches
from pathlib import Path, PosixPath, WindowsPath


def get_ratios(files: Iterable[str], filter_str: str) -> dict[str, float]:
    return {file: SequenceMatcher(a=filter_str, b=file).ratio() for file in files}


def filter_ratios(files: dict[str, float], *, min_ratio: float=0.6,
                  ratio_from_highest: None|float=None) -> list[str]:
    if ratio_from_highest:
        max_ratio = max(files.values())
        return [
            file for file, ratio in files.items()
            if ratio >= min_ratio and ratio >= max_ratio * ratio_from_highest
        ]
    else:
        return [file for file, ratio in files.items() if ratio >= min_ratio]


def get_matching_files3(directory: Path, filter_str: str) -> list[str]:
    """Get all file names in "directory" and (case insensitive) match the ones
       that exactly match "filter_str"

       In case there is no exact match, return closely matching files.
       If there are no closely matching files either, return an empty list.
       (Return file names, not full paths).

       For example:

       d = Path('.')
       files in dir: bite1 test output

       get_matching_files(d, 'bite1') => ['bite1']
       get_matching_files(d, 'Bite') => ['bite1']
       get_matching_files(d, 'pybites') => ['bite1']
       get_matching_files(d, 'test') => ['test']
       get_matching_files(d, 'test2') => ['test']
       get_matching_files(d, 'output') => ['output']
       get_matching_files(d, 'o$tput') => ['output']
       get_matching_files(d, 'nonsense') => []
    """
    file_map: defaultdict[str, list[str]] = defaultdict(list)
    for file in directory.iterdir():
        if file.is_file():
            file_map[file.name.lower()].append(file.name)

    # Exact match(es):
    if (filter := filter_str.lower()) in file_map:
        return file_map[filter]
    # Closest match(es):
    # elif match := get_close_matches(filter_str.lower(), file_map.keys()):
    elif match := filter_ratios(
        get_ratios(file_map.keys(), filter_str.lower()), ratio_from_highest=0.75
    ):
        values = []
        for key, value in file_map.items():
            if key in match:
                values.extend(value)
        return values
    else:
        return []


def get_matching_files(directory: Path, filter_str: str) -> list[str]:
    exact = []
    close = []
    for file in directory.iterdir():
        if file.name.lower() == filter_str.lower():
            exact.append(file.name)
        ######################################################################
        # Possibilities:
        # ------------------------------------------------------
        # | filter_str.lower? | file.name.lower? | Tests Pass? |
        # --------------------|------------------|--------------
        # |       True        |       True       |    False    |
        # |       True        |       False      |    False    |
        # |       False       |       True       |    True     |
        # |       False       |       False      |    True     |
        # ------------------------------------------------------
        elif match := get_close_matches(filter_str.lower(), [file.name.lower()], cutoff=0.67):
        # elif match := get_close_matches(filter_str.lower(), [file.name]):
        # elif match := get_close_matches(filter_str, [file.name.lower()]):
        # elif match := get_close_matches(filter_str, [file.name]):
            close.extend(match)

    if exact:
        return exact
    elif close:
        return close
    else:
        return []


def get_matching_files2(directory: PosixPath, filter_str: str) -> list[str]:
    files = [file_.name for file_ in directory.iterdir()]
    matches = [file_ for file_ in files
               if filter_str.lower() == file_.lower()]
    return matches or get_close_matches(filter_str, files)


if __name__ == '__main__':
    cwd = Path(__file__).parent
    print(f'Using files in {cwd}...')
    filter_str = input('Filter string:  ')
    print(get_matching_files(cwd, filter_str))
