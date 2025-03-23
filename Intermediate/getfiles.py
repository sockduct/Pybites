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


from collections.abc import Iterator
from os import PathLike
from pathlib import Path
from pprint import pprint


ONE_KB = 1024


type PathT = str | Path | PathLike[str]
type SizeT = int | float


def get_files(dirname: PathT, size_in_kb: SizeT=0.0, *, verbose: bool=False) -> Iterator[Path]:
    """Return files in dirname that are >= size_in_kb"""
    if not isinstance(dirname, Path):
        try:
            dirname = Path(dirname)
        except TypeError as err:
            raise TypeError(
                f'Error:  Expected string, Path, or PathLike not "{dirname}".'
            ) from err

    '''
    Alternatively:
    # Probably better to use multiplication over division:
    for file in glob.glob(os.path.join(dirname, '*')):
        if os.stat(file).st_size >= size_in_kb * ONE_KB:
            ...
    '''
    for entry in dirname.iterdir():
        if entry.is_file(follow_symlinks=False) and entry.stat().st_size/ONE_KB >= size_in_kb:
            yield entry
        elif verbose:
            print(f'Skipping {entry} - either not a file or too small...')


if __name__ == '__main__':
    for args in ((123,), ('.', 3)):
        print(f'Invoking get_files{args}...')
        try:
            res = list(get_files(*args, verbose=True))
        except TypeError as err:
            print(err)
            res = []
        pprint(list(res)) if res else print('Empty result')
