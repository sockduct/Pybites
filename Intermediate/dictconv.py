#! /usr/bin/env python3.13


from collections import namedtuple
from datetime import datetime
import json
from typing import Any


blog = dict(name='PyBites',
            founders=('Julian', 'Bob'),
            started=datetime(year=2016, month=12, day=19),
            tags=['Python', 'Code Challenges', 'Learn by Doing'],
            location='Spain/Australia',
            site='https://pybit.es')


# define namedtuple here
BlogTuple = namedtuple('BlogTuple', blog.keys())


class DTEncoder(json.JSONEncoder):
    def default(self, obj: Any):
        return obj.isoformat() if isinstance(obj, datetime) else super().default(obj)


def custom_decoder(obj: Any):
    if 'founders' in obj:
        obj['founders'] = tuple(obj['founders'])
    if 'started' in obj:
        obj['started'] = datetime.fromisoformat(obj['started'])

    return obj


def dict2nt(dict_: dict[str, Any]):
    return BlogTuple(**dict_)


def nt2json(nt: BlogTuple):
    return json.dumps(nt._asdict(), cls=DTEncoder)


def json2nt(json_: str):
    interim = json.loads(json_, object_hook=custom_decoder)
    return dict2nt(interim)


if __name__ == '__main__':
    nt = dict2nt(blog)
    ntjson = nt2json(nt)
    new_nt = json2nt(ntjson)

    print(f'{nt=}\n\n{ntjson=}\n\n{new_nt=}')
