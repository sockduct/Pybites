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


from pathlib import PosixPath, WindowsPath, Path
from difflib import get_close_matches


type AnyPath = PosixPath | WindowsPath | Path


def get_matching_files(directory: AnyPath, filter_str: str) -> list[str]:
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
    exact = []
    approx  = []
    for file in directory.iterdir():
        if file.name.lower() == filter_str.lower():
            exact.append(file.name)
        elif m := get_close_matches(filter_str.lower(), [file.name.lower()]):
            approx.extend(m)

    if exact:
        return exact
    elif approx:
        return approx
    else:
        return []


if __name__ == '__main__':
    cwd = Path(__file__).parent
    print(f'Using files in {cwd}...')
    filter_str = input('Filter string:  ')
    print(get_matching_files(cwd, filter_str))
