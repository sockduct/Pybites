#! /usr/bin/env python3.13
'''
You added some monitoring the other day writing log files to a directory. In
this Bite you will zip up the latest ones renaming the files to include the
creation date. Ready to learn some pathlib, Zipfile and a bit of datetime
goodness?

Complete zip_last_n_files that takes a directory (Path object), a zip_file
output filename (str) and n (int) = the amount files to include in the zipfile.
You zip up the last N log files to a zipfile in the current working directory.
The files need to include their creation date (%Y-%m-%d, e.g. 2019-10-30).

Here is an example how it should work. Given this directory (files sorted
ascending by creation timestamp):
$ ls -lrth /tmp/logs/
total 0
-rw-r--r--  1 bobbelderbos  wheel     0B Oct 30 23:16 file4.log
-rw-r--r--  1 bobbelderbos  wheel     0B Oct 30 23:16 file3.log
-rw-r--r--  1 bobbelderbos  wheel     0B Oct 30 23:16 file2.log
-rw-r--r--  1 bobbelderbos  wheel     0B Oct 30 23:16 file5.log
-rw-r--r--  1 bobbelderbos  wheel     0B Oct 30 23:17 file7.log
-rw-r--r--  1 bobbelderbos  wheel     0B Oct 30 23:17 file6.log
-rw-r--r--  1 bobbelderbos  wheel     0B Oct 31 00:10 file1.log

Your code should produce a zipfile with the last N (here = 3) files. (Note the
renamed file names!)
>>> from pathlib import Path
>>> from zipfile import ZipFile
>>> from files import zip_last_n_files
>>> path = Path('/tmp') / 'logs'
>>> zip_last_n_files(path, 'log_files.zip', n=3)
>>> zip_out = Path('log_files.zip')
>>> ZipFile(zip_out).namelist()
['file1_2019-10-31.log', 'file7_2019-10-30.log', 'file6_2019-10-30.log']

The order of the 3 files does not really matter, as long as you get the latest 3
(or whatever number n is).
'''


from datetime import datetime
from heapq import nlargest
import os
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


TMP = Path(os.getenv("TMP", "/tmp"))
LOG_DIR = TMP / 'logs'
ZIP_FILE = 'logs.zip'


def zip_last_n_files(directory: Path=LOG_DIR, zip_file: str=ZIP_FILE, n: int=3) -> None:
    files = {file: file.stat().st_mtime_ns for file in directory.iterdir() if file.is_file()}

    # Grab the newest (highest st_mtime_ns) n files:
    # Here we retrieve n files (keys from files dict) sorted by their values (st_mtime_ns)
    file_set = nlargest(n, files, key=files.__getitem__)

    with ZipFile(zip_file, mode='w', compression=ZIP_DEFLATED) as zf:
        for file in file_set:
            try:
                dt = datetime.fromtimestamp(file.stat().st_birthtime)
            except AttributeError:
                # Linux/UNIX doesn't have st_birthtime, us st_mtime instead
                # Could also consider st_ctime
                dt = datetime.fromtimestamp(file.stat().st_mtime)
            zf.write(file, arcname=f'{file.stem}_{dt:%Y-%m-%d}{file.suffix}')


if __name__ == '__main__':
    cwd = Path(__file__).parent
    zip_file1 = 'programs.zip'
    zip_last_n_files(cwd, zip_file1)
    print('Test 1:')
    ZipFile(Path(zip_file1)).printdir()
    Path(zip_file1).unlink()

    zip_file2 = 'log_files.zip'
    path = Path('/temp')
    zip_last_n_files(path, zip_file2, n=3)
    print(f'\nTest 2:\n{ZipFile(Path(zip_file2)).namelist()}')
    Path(zip_file2).unlink()
