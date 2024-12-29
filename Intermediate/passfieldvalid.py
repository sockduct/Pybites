#! /usr/bin/env python3.13


from string import (
    digits, ascii_lowercase as lowercase,
    ascii_uppercase as uppercase, punctuation
)


used_passwords = set('PassWord@1 PyBit$s9'.split())


def atleastone(target: str, group: str) -> bool:
    return any(char in group for char in target)


def validate_password(password: str) -> bool:
    '''
    Takes password (str) and validates as follows:
    * is between 6 and 12 chars long (both inclusive)
    * has at least 1 digit [0-9]
    * has at least two lowercase chars [a-z]
    * has at least one uppercase char [A-Z]
    * has at least one punctuation char (use: PUNCTUATION_CHARS)
    * Has not been used before (use: used_passwords)

    Valid:
    * If the password matches all criteria the store the password in
      used_passwords and return True (else return False)
    '''
    if 6 > len(password) > 12:
        return False
    if not atleastone(password, digits):
        return False
    # Alternatively use regex:
    # if not re.search(r'[a-z].*[a-z]', password):
    if sum(char in lowercase for char in password) < 2:
        return False
    if not atleastone(password, uppercase):
        return False
    if not atleastone(password, punctuation):
        return False
    if password in used_passwords:
        return False

    used_passwords.add(password)
    return True
