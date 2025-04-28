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


class ToxIniParser:

    def __init__(self, ini_file: str|Path) -> None:
        """Use configparser to load ini_file into self.config"""
        self._config = configparser.ConfigParser()
        with open(ini_file) as f:
            self._config.read_file(f)

    @property
    def number_of_sections(self) -> int:
        """Return the number of sections in the ini file.
           New to properties? -> https://pybit.es/articles/property-decorator
        """
        return len(self._config.sections())

    @property
    def environments(self) -> list[str]:
        """Return a list of environments
           (= "envlist" attribute of [tox] section)"""
        return self._config.get('tox', 'envlist', fallback=None).split(', ')

    @property
    def base_python_versions(self) -> list[str]:
        """Return a list of all basepython across the ini file"""
        return [
            self._config.get(section, 'basepython', fallback=None)
            for section in self._config.sections()
            if self._config.get(section, 'basepython', fallback=None)
        ]
