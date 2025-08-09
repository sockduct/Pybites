#! /usr/bin/env python3.13
'''
Each file and directory in Unix has its permissions broken down into owner,
group and other (world) attributes, see here.

Each attribute has one or more permissions: r(ead), w(rite), e(x)ecute. The lack
of any permission is indicated by a dash (-). So r-- = read only, rw- = read +
write, and rwx = full permissions.

The file permission for owner + group + other has 3 of those strings after the
initial character which indicates file type (- = file / d = directory):

$ lt bite.html
-rw-r--r--  1 bobbelderbos  staff   229B Oct  9 14:03 bite.html

To change the file permission you use the chmod and its octal representation,
for each attribute (owner, group, other) we translate the permission string
summing a value for each permission: r = 4, w = 2, and x = 1, hence:

$ touch myfile
$ lt myfile
-rw-r--r--  1 bobbelderbos  staff     0B Oct 11 10:12 myfile

$ chmod 400 myfile
$ lt myfile
-r--------  1 bobbelderbos  staff     0B Oct 11 10:12 myfile

$ chmod 600 myfile
$ lt myfile
-rw-------  1 bobbelderbos  staff     0B Oct 11 10:12 myfile

$ chmod 700 myfile
$ lt myfile
-rwx------  1 bobbelderbos  staff     0B Oct 11 10:12 myfile

$ chmod 740 myfile
$ lt myfile
-rwxr-----  1 bobbelderbos  staff     0B Oct 11 10:12 myfile

$ chmod 745 myfile
$ lt myfile
-rwxr--r-x  1 bobbelderbos  staff     0B Oct 11 10:12 myfile

That concludes our little Unix file permission lesson. In this Bite you will
complete get_octal_from_file_permission that takes a permission string and
returns its octal representation, for example:
>>> from permissions import get_octal_from_file_permission
>>> get_octal_from_file_permission('rw-r--r--')
'644'
>>> get_octal_from_file_permission('rwxrwxrwx')
'777'

Of course the tests check a bunch more (wonder about parametrize? You can read
more about it on our blog - bullet 9). Have fun and keep calm and code in
Python!
'''


from itertools import batched


def get_octal_val(rwx: tuple[str, str, str]) -> int:
    val = 0

    if rwx[0] == 'r':
        val += 4
    if rwx[1] == 'w':
        val += 2
    if rwx[2] == 'x':
        val += 1

    return val


def get_octal_from_file_permission(rwx: str) -> str:
    """Receive a Unix file permission and convert it to
       its octal representation.

       In Unix you have user, group and other permissions,
       each can have read (r), write (w), and execute (x)
       permissions expressed by r, w and x.

       Each has a number:
       r = 4
       w = 2
       x = 1

       So this leads to the following input/ outputs examples:
       rw-r--r-- => 644 (user = 4 + 2, group = 4, other = 4)
       rwxrwxrwx => 777 (user/group/other all have 4 + 2 + 1)
       r-xr-xr-- => 554 (user/group = 4 + 1, other = 4)


       Alternative approach:
       rwxs = '--- --x -w- -wx r-- r-x rw- rwx'.split()
       octals = [str(i) for i in range(0, 8)]
       permissions = dict(zip(rwxs, octals))

       parts = [rwx[i:i+3] for i in range(0, len(rwx), 3)]
       return ''.join(
           permissions[p]
           for p in parts
       )
    """
    if not isinstance(rwx, str) or len(rwx) != 9:
        raise ValueError(f'Expected string of 9 digits, got:  {rwx}')

    vals = {
        item: get_octal_val((user, group, other))
        # Would like to use strict=True in batched but requires Python v3.13
        # PyBites platform is at v3.12
        for item, (user, group, other) in zip(['user', 'group', 'other'], batched(rwx, 3), strict=True)
    }

    return f'{vals["user"]}{vals["group"]}{vals["other"]}'


if __name__ == '__main__':
    '''
    Sanity checks:
    >>> get_octal_from_file_permission('rw-r--r--')
    '644'
    >>> get_octal_from_file_permission('rwxrwxrwx')
    '777'
    '''
    for testvals in ('rw-r--r--', 'rwxrwxrwx'):
        print(f'{get_octal_from_file_permission(testvals)=} ({testvals=})')
