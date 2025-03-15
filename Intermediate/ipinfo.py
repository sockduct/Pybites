#! /usr/bin/env python3.13


from ipaddress import ip_address, IPv4Address, IPv6Address
from pprint import pprint
from typing import TypeAlias

import requests


IPINFO_URL = 'http://ipinfo.io/{ip}/json'
IPAddr: TypeAlias = str | IPv4Address | IPv6Address


def get_ip_country(ip: IPAddr) -> str:
    """Receives ip address string, use IPINFO_URL to get geo data,
       parse the json response returning the country code of the IP"""
    if not isinstance(ip, (IPv4Address, IPv6Address)):
        ip = ip_address(ip)

    resp = requests.get(IPINFO_URL.format(ip=ip))
    resp.raise_for_status()

    return resp.json()


if __name__ == '__main__':
    pprint(get_ip_country('23.237.45.102'))
    pprint(get_ip_country(ip_address('12.17.137.99')))
