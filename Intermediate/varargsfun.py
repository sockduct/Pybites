#! /usr/bin/env python3.13


from typing import NotRequired, TypedDict


class Profile(TypedDict):
    name: str
    age: int
    sports: NotRequired[list[str]]
    awards: NotRequired[dict[str, str]]


def get_profile(name: str, age: int, *args: tuple[str], verbose: bool=False,
                **kwargs: dict[str, str]) -> Profile:
    '''
    Takes:
    * required name
    * required age - if not int raises ValueError
    * one or more optional sports (args) - limit of 5 else ValueError
    * one or more optional awares (Kwargs)
    '''

    if not isinstance(age, int):
        raise ValueError(f'Expected age to be of type int, not {type(age)}.')

    profile = Profile(name=name, age=age)

    if args:
        max_sports = 5

        sports = sorted(args)
        if len(sports) > max_sports:
            raise ValueError(f'Maximum of {max_sports} allowed but {len(sports)} supplied.')

        profile['sports'] = sports
    else:
        sports = None

    if kwargs:
        awards = kwargs
        profile['awards'] = awards
    else:
        awards = None

    if verbose:
        print(f'Profile({name=}, {age=}, {sports=}, {awards=})')

    return profile


if __name__ == '__main__':
    kwargs = dict(champ='helped out team in crisis')
    for args in [('tim', 36), ('tim', 36, 'tennis', 'basketball'),
                 ('tim', 36, 'tennis', 'basketball', 'kwargs')]:
        if 'kwargs' in args:
            args = args[:-1]
            get_profile(*args, verbose=True, **kwargs)
        else:
            get_profile(*args, verbose=True)
