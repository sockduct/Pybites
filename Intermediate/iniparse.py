#! /usr/bin/env python3.13
'''
The INI file format is an informal standard for configuration files for some
platforms or software. (Wikipedia).

In this Bite you will use configparser to parse a tox ini file.

Complete the ToxIniParser class, completing the stub properties making the tests
happy.

See the TESTS tab. There is a lot of ini file data, so scroll down to the actual
tests ...

Additionally here is how it would work in the Python REPL using a copy of
Django's tox ini file saved to my local /tmp folder:
  >>> from ini import ToxIniParser
  >>> tox = ToxIniParser('/tmp/django-tox.ini')
  >>> tox.number_of_sections
  7
  >>> tox.environments
  ['py3', 'flake8', 'docs', 'isort']
  >>> tox.base_python_versions
  ['python3']

Good luck and keep calm and code in Python!
'''


import configparser
from pathlib import Path
import re


class ToxIniParser:
    def __init__(self, ini_file: str|Path) -> None:
        """Use configparser to load ini_file into self.config"""
        self.config = configparser.ConfigParser()
        with open(ini_file) as f:
            self.config.read_file(f)

    @property
    def number_of_sections(self) -> int:
        """Return the number of sections in the ini file.
           New to properties? -> https://pybit.es/articles/property-decorator
        """
        return len(self.config.sections())

    @property
    def environments(self) -> list[str|None]:
        """Return a list of environments
           (= "envlist" attribute of [tox] section)"""
        if envs := self.config.get('tox', 'envlist', fallback=None):
            # Split on separators and prune out empty strings:
            # return  [e for e in re.split(r'\s+|\s*,\s*', result.strip()) if e]
            # Probably better - just split on "," or newlines and strip off
            # excess whitespace:
            return [env.strip() for env in re.split(r'\n|,', envs) if env]

        return []

    @property
    def base_python_versions(self) -> list[str|None]:
        """Return a list of all basepython across the ini file"""
        return list({
            bp for section in self.config.sections()
            if (bp := self.config.get(section, 'basepython', fallback=None))
        })
