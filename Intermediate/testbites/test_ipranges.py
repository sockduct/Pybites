#! /usr/bin/env python
'''
Another Test Bite, we ❤️ them 😁 - today you will write tests for IPv4Network
(ipaddress module) and dataclass objects 💪.

Check out the ips module I wrote parsing a JSON file of IP ranges
(ip-ranges.json) under CODE TO TEST, then write tests to get to 100% test
coverage and a 100% mutation score.

Good luck and keep calm and code in Python 🐍 and pytest. Share your
accomplishment upon completing the Bite 😎
'''


from collections import Counter
from ipaddress import IPv4Network
from pathlib import Path
from random import sample
from tempfile import TemporaryDirectory
from urllib.request import urlretrieve

import pytest

'''
Notes on importing ips.py module:

Best practice:
Treat Intermediate/testbites as a package and use relative imports in tests.
Then run the test module with -m (so it has a package context), not by executing
the file directly.

Recommended structure/usage:
Keep the import as from .ips import ServiceIPRange, parse_ipv4_service_ranges,
get_aws_service_range in test_ipranges.py.
Run (pytest) tests from repo root with: test_ipranges.py
Run the module directly with: python -m Intermediate.testbites.test_ipranges
This gives both pytest and "direct run" without import hacks.

To get test_ipranges.py to work too, you can add a small fallback (hack):
try:
    from .ips import ServiceIPRange, parse_ipv4_service_ranges, get_aws_service_range
except ImportError:
    from ips import ServiceIPRange, parse_ipv4_service_ranges, get_aws_service_range
'''
# from ips import ServiceIPRange, parse_ipv4_service_ranges, get_aws_service_range
from .ips import ServiceIPRange, parse_ipv4_service_ranges, get_aws_service_range


URL = "https://bites-data.s3.us-east-2.amazonaws.com/ip-ranges.json"
# TMP = os.getenv("TMP", "/tmp")
TMPDIR = TemporaryDirectory()
TMP = TMPDIR.name
PATH = Path(TMP, "ip-ranges.json")
IP = IPv4Network('192.0.2.8/29')


@pytest.fixture(scope='module')
def json_file() -> Path:
    """Import data into tmp folder"""
    urlretrieve(URL, PATH)
    return PATH


# write your pytest code ...
'''
AWS Regions:
['GLOBAL', 'af-south-1', 'ap-east-1', 'ap-northeast-1', 'ap-northeast-2',
 'ap-northeast-3', 'ap-south-1', 'ap-southeast-1' , 'ap-southeast-2',
 'ca-central-1', 'cn-north-1', 'cn-northwest-1', 'eu-central-1', 'eu-north-1',
 'eu-west-1', 'eu-west-2', 'eu-west-3', 'me-south-1', 'sa-east-1', 'us-east-1',
 'us-east-2', 'us-gov-east-1', 'us-gov-west-1', 'us-west-1', 'us-west-2'
]

AWS Services:
['AMAZON', 'AMAZON_CONNECT', 'API_GATEWAY', 'CLOUD9', 'CLOUDFRONT', 'CODEBUILD',
 'DYNAMODB', 'EC2', 'EC2_INSTANCE_CONNECT' , 'GLOBALACCELERATOR', 'ROUTE53',
 'ROUTE53_HEALTHCHECKS', 'S3', 'WORKSPACES_GATEWAYS'
]

AWS Networks (1,254):
[IPv4Network('3.0.0.0/15'), ..., IPv4Network('216.182.238.0/23')]

Tests:
* Test for valid and invalid regions
* Test for valid and invalid services
* Test for valid and invalid IP Addresses and Networks
* Create matrix and cover valid/invalid combinations for all 3
'''

@pytest.fixture()
def ipv4_service_ranges(json_file: Path) -> list[ServiceIPRange]:
    return parse_ipv4_service_ranges(json_file)


def test_regions(ipv4_service_ranges: list[ServiceIPRange]) -> None:
    regions = {ent.region for ent in ipv4_service_ranges}
    regions.add('INVALID')
    for region in regions:
        count = sum(ent.region == region for ent in ipv4_service_ranges)
        if region != 'INVALID':
            assert count >= 1
        else:
            assert count == 0

def test_services(ipv4_service_ranges: list[ServiceIPRange]) -> None:
    services = {ent.service for ent in ipv4_service_ranges}
    services.add('INVALID')
    for service in services:
        count = sum(ent.service == service for ent in ipv4_service_ranges)
        if service != 'INVALID':
            assert count >= 1
        else:
            assert count == 0

def test_ipv4net(ipv4_service_ranges: list[ServiceIPRange]) -> None:
    cidrs = {ent.cidr for ent in ipv4_service_ranges}
    top3 = Counter(ent.cidr for ent in ipv4_service_ranges).most_common(3)
    invalid_bottom = '2.1.1.1'
    invalid_top = '222.111.1.1'

    # Invalid address raises AddressValueError but function raises ValueError:
    with pytest.raises(ValueError):
        get_aws_service_range('not-an-ipv4-address', ipv4_service_ranges)

    for ent, count in top3:
        res = get_aws_service_range(str(ent.network_address + 1), ipv4_service_ranges)
        assert len(res) == count

    for cidr in cidrs:
        # Not shown unless error or enabled via flag:
        print(f'{cidr=}, {cidr.network_address=}\n\\_{cidr.network_address - 1=}, '
              f' {cidr.network_address + 1=}')
        test_address = cidr.network_address if cidr.prefixlen == 32 else cidr.network_address + 1
        assert (
            len(get_aws_service_range(str(test_address), ipv4_service_ranges)) >= 1
        )

    # Random sample:
    cidr_list = list(cidrs)
    cidr_sample = int(len(cidr_list) * 0.2)
    for cidr in sample(cidr_list, cidr_sample):
        assert (
            len(get_aws_service_range(str(cidr.network_address), ipv4_service_ranges)) >= 1
        )

    for bad_ip in {invalid_bottom, invalid_top}:
        assert (
            len(get_aws_service_range(bad_ip, ipv4_service_ranges)) == 0
        )


### Solution Provided:
def test_dataclass() -> None:
    expected = ("192.0.2.8/29 is allocated to the pybites service "
                "in the US region")
    assert str(ServiceIPRange('pybites', 'US', IP)) == expected


def test_parse_ranges(json_file: Path) -> None:
    out = parse_ipv4_service_ranges(json_file)
    assert len(out) == 1886

    assert type(out) == list
    assert all(type(element) == ServiceIPRange for element in out)
    assert str(out[0]) == ("13.248.118.0/24 is allocated to the AMAZON "
                           "service in the eu-west-1 region")


def test_get_aws_service_range_zero_hits(json_file: Path) -> None:
    assert get_aws_service_range('13.248.118.0', []) == []


def test_get_aws_service_range_two_hits(json_file: Path) -> None:
    service_range = parse_ipv4_service_ranges(json_file)
    expected = [
        ServiceIPRange(service='AMAZON', region='eu-west-1',
                       cidr=IPv4Network('13.248.118.0/24')),
        ServiceIPRange(service='GLOBALACCELERATOR', region='eu-west-1',
                       cidr=IPv4Network('13.248.118.0/24'))
    ]
    assert get_aws_service_range('13.248.118.0', service_range) == expected


def test_get_aws_service_range_exception(json_file: Path) -> None:
    with pytest.raises(ValueError) as exc:
        get_aws_service_range('nonsense', [])
    assert str(exc.value) == "Address must be a valid IPv4 address"
