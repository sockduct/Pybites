#! /usr/bin/env python3.13
'''
Complete the get_dates method given the following:
* A listing of date strings in unknown date format
* An enum class which contains allowed/supported date formats

Although the following assignment text is wordy, once you will see test cases
the task definition will become clearer.

The get_dates method will return a list of date strings in the format yyyy-mm-dd.

The date format of input date strings will be inferred based on the most
prevalent allowed date format of items in the list. Allowed/supported date
formats are defined in an enum class.

The most prevalent allowed date format of items must represent a single most
frequent date format. If there are two most frequent formats with the same
frequency raise a (custom) InfDateFmtError exception.

Items in an input list can be in any format no matter whether or not this format
is listed in the DateFormat enum class. Items can be even values which cannot
represent a date at all. Those items are nonparsable. If the frequency of
nonparsable elements is higher than the frequency of other allowed date formats
(counted individually for each format) raise a custom InfDateFmtError exception.

Once you have the most prevalent date format, parse dates in an input list and
return them as a list of strings in the format yyyy-mm-dd.

Dates which are not parsable replace with the string Invalid.

Important note: the list of allowed/supported date formats is supposed to be
stored in the DateFormat enum class only. The DateFormat enum class is subject
of change and this change is not under your control.

As a hint, you are provided with a helper method _maybe_DFs which shows how to
work with the DateFormat enum class.

This assignment introduces a very simple date format inferrer. For more serious
work you can check out:
* dateparser:  https://dateparser.readthedocs.io/
* dateinfer:  https://github.com/jeffreystarr/dateinfer
'''


from __future__ import annotations
from enum import Enum
from datetime import datetime
from collections import Counter
from contextlib import suppress
from pprint import pformat, pprint


class DateFormat(Enum):
    DDMMYY = 0  # dd/mm/yy
    MMDDYY = 1  # mm/dd/yy
    YYMMDD = 2  # yy/mm/dd
    NONPARSABLE = -999

    @classmethod
    def get_d_parse_formats(cls: type[DateFormat], val: int|None=None) -> list[str]|str:
        """ Arg:
        val(int | None) enum member value
        Returns:
        1. for val=None a list of explicit format strings
            for all supported date formats in this enum
        2. for val=n an explicit format string for a given enum member value
        """
        d_parse_formats = ["%d/%m/%y", "%m/%d/%y", "%y/%m/%d"]
        if val is None:
            return d_parse_formats
        if 0 <= val <= len(d_parse_formats):
            return d_parse_formats[val]
        raise ValueError


class InfDateFmtError(Exception):
    """custom exception when it is not possible to infer a date format
    e.g. too many NONPARSABLE or a tie """
    pass


def _maybe_DateFormats(date_str: str) -> list[DateFormat]:
    """ Args:
    date_str (str) string representing a date in unknown format
    Returns:
    a list of enum members, where each member represents
    a possible date format for the input date_str
    """
    d_parse_formats = DateFormat.get_d_parse_formats()
    maybe_formats = []
    for idx, d_parse_fmt in enumerate(d_parse_formats):
        with suppress(ValueError):
            _parsed_date = datetime.strptime(date_str, d_parse_fmt) # pylint: disable=W0612
            maybe_formats.append(DateFormat(idx))
    if not maybe_formats:
        maybe_formats.append(DateFormat.NONPARSABLE)
    return maybe_formats


def get_dates(dates: list[str]) -> list[datetime|str]:
    """ Args:
    dates (list) list of date strings
    where each list item represents a date in unknown format
    Returns:
    list of date strings, where each list item represents
    a date in yyyy-mm-dd format. Date format of input date strings is
    inferred based on the most prevalent format in the dates list.
    Allowed/supported date formats are defined in a DF enum class.
    """
    # complete this method
    results = []
    for date in dates:
        results.extend(_maybe_DateFormats(date))

    ranking = Counter(results).most_common()
    if len(ranking) > 1:
        first, second, *_ = ranking
        if first[1] == second[1]:
            raise InfDateFmtError('No dominant date format')
    else:
        first = ranking[0]

    if first[0] == DateFormat.NONPARSABLE:
        raise InfDateFmtError('Most prevalent format is non-parsable')

    fmt_idx = first[0].value
    dt_fmt = DateFormat.get_d_parse_formats(fmt_idx)
    if isinstance(dt_fmt, list):
        raise ValueError('Expected a single format string, got a list.')
    parsed = []
    for date in dates:
        '''
        Alternative approach:
        try:
            date = datetime.strptime(date_str, d_parse_format)
            date = datetime.strftime(date, "%Y-%m-%d")
            out_dates.append(date)
        except ValueError:
            out_dates.append("Invalid")
        '''
        parse: str|datetime = 'Invalid'
        with suppress(ValueError):
            parse = datetime.strptime(date, dt_fmt)
        parsed.append(parse)

    return [
        parse.strftime('%Y-%m-%d') if isinstance(parse, datetime) else parse
        for parse in parsed
    ]


if __name__ == '__main__':
    date_lists = [
        [
            '11/01/24',
            '12/12/24',
            '01/232/5',
            '05/30/23',
            '02/28/40',
        ],
        [
            'invalid'
        ],
        [
            '01/02/23'
        ],
        [
            '01/30/33'
        ],
    ]
    for date_list in date_lists:
        print(f'Checking:\n{pformat(date_list)}')
        try:
            print(f'Results:\n{pformat(get_dates(date_list))}\n')
        except InfDateFmtError as err:
            print(f'Caught error:\n{err}\n')
