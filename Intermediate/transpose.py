#! /usr/bin/env python3.13


from typing import Any


def transpose(data: dict[Any, Any]|tuple[Any, ...]) -> list[tuple[Any, ...]]:
    """Transpose a data structure
    1. dict
    data = {'2017-8': 19, '2017-9': 13}
    In:  transpose(data)
    Out: [('2017-8', '2017-9'), (19, 13)]

    2. list of (named)tuples
    data = [Member(name='Bob', since_days=60, karma_points=60,
                   bitecoin_earned=56),
            Member(name='Julian', since_days=221, karma_points=34,
                   bitecoin_earned=78)]
    In: transpose(data)
    Out: [('Bob', 'Julian'), (60, 221), (60, 34), (56, 78)]
    """
    # For mappings:
    # res = [tuple(data.keys()), tuple(data.values())]
    # Alternatively just:  return [data.keys(), data.values()]

    # Generic:
    generic_data = data.items() if isinstance(data, dict) else data

    # For namedtuples and dict.items:
    return list(zip(*generic_data))
