#! /usr/bin/env python3.14
'''
Another Test Bite, we ❤️ them 😁 - today you will write tests for IPv4Network
(ipaddress module) and dataclass objects 💪.

Check out the ips module I wrote parsing a JSON file of IP ranges
(ip-ranges.json) under CODE TO TEST, then write tests to get to 100% test
coverage and a 100% mutation score.

Good luck and keep calm and code in Python 🐍 and pytest. Share your
accomplishment upon completing the Bite 😎
'''


from ipaddress import IPv4Network
import os
from pathlib import Path
from urllib.request import urlretrieve

import pytest

from ips import ServiceIPRange, parse_ipv4_service_ranges, get_aws_service_range


URL = "https://bites-data.s3.us-east-2.amazonaws.com/ip-ranges.json"
TMP = os.getenv("TMP", "/tmp")
PATH = Path(TMP, "ip-ranges.json")
IP = IPv4Network('192.0.2.8/29')


@pytest.fixture(scope='module')
def json_file():
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
