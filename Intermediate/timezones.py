#! /usr/bin/env python3.13


from datetime import datetime, UTC
from zoneinfo import ZoneInfo, available_timezones, ZoneInfoNotFoundError


# Globals:
MIN_MEETING_HOUR = 6
MAX_MEETING_HOUR = 22
TIMEZONES = set(available_timezones())


def within_schedule(utc: datetime, *timezones: str) -> bool:
    """
    Receive a UTC datetime and one or more timezones and check if
    they are all within MIN_MEETING_HOUR and MAX_MEETING_HOUR
    (both included).
    """

    dt_utc = utc.replace(tzinfo=UTC)
    try:
        return all(
            MIN_MEETING_HOUR <= dt_utc.astimezone(ZoneInfo(zone)).hour <= MAX_MEETING_HOUR
            for zone in timezones
        )
    except ZoneInfoNotFoundError as err:
        raise ValueError(err) from err


if __name__ == '__main__':
    within_schedule(datetime.now(), 'bogus')
