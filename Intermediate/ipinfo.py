#! /usr/bin/env python3.13


from ipaddress import ip_address, IPv4Address, IPv6Address
from pprint import pprint
from typing import TypeAlias

import requests


IPINFO_URL = 'http://ipinfo.io/{ip}/json'
IPAddr: TypeAlias = str | IPv4Address | IPv6Address


def get_ip_country(ip: IPAddr, *, verbose: bool=False) -> str|None:
    """Receives ip address string, use IPINFO_URL to get geo data,
       parse the json response returning the country code of the IP"""
    if not isinstance(ip, (IPv4Address, IPv6Address)):
        try:
            ip = ip_address(ip)
        except ValueError as err:
            print(f'Unable to build a valid IPv4 or IPv6 address from "{ip}".')
            return None

    if verbose:
        print(f"Checking ipinfo.io's database for {ip}...")
    resp = requests.get(IPINFO_URL.format(ip=ip))
    resp.raise_for_status()

    return res.get('country') if (res := resp.json()) else None


if __name__ == '__main__':
    for test_data in ('23.237.45.102', ip_address('12.17.137.99'), 5, 'bad', '272.13.104.99'):
        # Intentionally sending bad data to test error handling:
        pprint(get_ip_country(test_data, verbose=True))  # type: ignore
