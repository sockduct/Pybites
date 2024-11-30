#! /usr/bin/env python3.13


# Use NamedTuple instead to use type annotations:
# from collections import namedtuple
from datetime import datetime
import json
from typing import Any, NamedTuple, TypedDict


# Note:  Can also serialize int and float-derived enums which aren't included
#        here.  We capture the defaults and add the ability to do datetimes:
serializable_scalar = str|int|float|bool|None|datetime
# Since collections can be nested, using Any:
serializable = dict[str, Any]|list[Any]|tuple[Any, ...]|serializable_scalar


class BlogDict(TypedDict):
    name: str
    founders: tuple[str, str]
    started: datetime
    tags: list[str]
    location: str
    site: str

blog: BlogDict = dict(name='PyBites',
            founders=('Julian', 'Bob'),
            started=datetime(year=2016, month=12, day=19),
            tags=['Python', 'Code Challenges', 'Learn by Doing'],
            location='Spain/Australia',
            site='https://pybit.es')


# define namedtuple here
# BlogTuple = namedtuple('BlogTuple', blog.keys())
class BlogTuple(NamedTuple):
    name: str
    founders: tuple[str, str]
    started: datetime
    tags: list[str]
    location: str
    site: str


class DTEncoder(json.JSONEncoder):
    def default(self, obj: serializable) -> str:
        return obj.isoformat() if isinstance(obj, datetime) else super().default(obj)


def custom_decoder(obj: dict[str, Any]) -> dict[str, serializable]:
    if 'founders' in obj:
        obj['founders'] = tuple(obj['founders'])
    if 'started' in obj:
        obj['started'] = datetime.fromisoformat(obj['started'])

    return obj


def dict2nt(dict_: BlogDict) -> BlogTuple:
    return BlogTuple(**dict_)


def nt2json(nt: BlogTuple) -> str:
    return json.dumps(nt._asdict(), cls=DTEncoder)


def json2nt(json_: str) -> BlogTuple:
    # Alternatively:  nt = nt._replace(started=str(nt.started))
    # Problem with alternative - how to deserialize?
    interim = json.loads(json_, object_hook=custom_decoder)
    return dict2nt(interim)


if __name__ == '__main__':
    nt = dict2nt(blog)
    ntjson = nt2json(nt)
    new_nt = json2nt(ntjson)

    print(f'{nt=}\n\n{ntjson=}\n\n{new_nt=}')
