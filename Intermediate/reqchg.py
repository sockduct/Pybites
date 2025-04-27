#! /usr/bin/env python3.13
'''
In this Bite you compare a list of packages (aka requirement.txt) from before
vs. after (pip) upgrade. Check the TESTS tab for the format of the input data.

Complete the changed_dependencies function that receives the old and new
requirements (multiline) strs and returns a list of package names that were
upgraded (new version > previous version).

To keep it manageable you can assume that both requirement strs have the same
packages, no packages were added or deleted.

A note about the digits (major/minor) numbers in the packages: they are ints,
so twilio==6.23.1 > twilio==6.3.0 (see also Twilio's history log).

Have fun and we hope you learn a thing or two!
'''


from collections.abc import Callable
from packaging.version import Version


def changed_dependencies(old_reqs: str, new_reqs: str) -> list[str]:
    """Compare old vs new requirement multiline strings
    and return a list of dependencies that have been upgraded
    (have a newer version)
    """
    dictpkg: Callable[[str], dict[str, str]] = lambda req: dict(
        line.split('==') for line in req.strip().splitlines()
    )

    upgraded = []
    # for old, new in zip(old_reqs.strip().splitlines(), new_reqs.strip().splitlines(), strict=True):
    # Better:
    for (old_pkg, old_ver), (new_pkg, new_ver), in zip(
        dictpkg(old_reqs).items(), dictpkg(new_reqs).items(), strict=True
    ):
        if old_pkg != new_pkg:
            raise ValueError('Expected same old and new packages.')

        if Version(new_ver) > Version(old_ver):
            upgraded.append(new_pkg)

    return upgraded
