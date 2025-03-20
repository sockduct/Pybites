#! /usr/bin/env python3.13
'''
In this Bite you complete get_files that receives a dirname and size_in_kb
(note kb, not bytes).

There are two things you need to code:
* Inspect/list the files in dirname
* Return files that are bigger or equal than size_in_kb (return a list or turn
  the function into a generator)

The os module is your friend here, but you also might want to check out glob.
Have fun and keep coding in Python!
'''


import os
from pathlib import Path
from pprint import pprint


ONE_KB = 1024


type PathT = str | Path | os.PathLike


def get_files(dirname: PathT, size_in_kb: int=0, *, verbose: bool=False) -> list[Path]:
    """Return files in dirname that are >= size_in_kb"""
    if not isinstance(dirname, Path):
        try:
            dirname = Path(dirname)
        except TypeError:
            print(f'Error:  Expected string or Path, not "{dirname}".')
            return

    files = []
    for entry in dirname.iterdir():
        if entry.is_file(follow_symlinks=False) and entry.stat().st_size//ONE_KB >= size_in_kb:
            files.append(entry)
        elif verbose:
            print(f'Skipping {entry} - either not a file or too small...')

    return files


if __name__ == '__main__':
    # get_files(123)
    pprint(get_files('.'))
