#! /usr/bin/env python3.13
'''
Cisco Nexus 9k devices is one of the first network equipment with comprehensive
API programmatic access from Cisco. API capabilities might be familiar to
developers working with web apps but they are new to network engineers.

In this Bite we will practice making API calls to the Cisco Nexus device and
retrieve information from it. The focus of the Bite is on the HTTP header
requirements, the API request body, and general interaction between Python
scripts and network devices.

You can find more information about the Cisco Nexus API in the following links:
NX-API CLI:
https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/92x/programmability/guide/b-cisco-nexus-9000-series-nx-os-programmability-guide-92x/b-cisco-nexus-9000-series-nx-os-programmability-guide-92x_chapter_010011.html

NX-API REST:
https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/92x/programmability/guide/b-cisco-nexus-9000-series-nx-os-programmability-guide-92x/b-cisco-nexus-9000-series-nx-os-programmability-guide-92x_chapter_010100.html

NX-API Developer Sandbox:
https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/92x/programmability/guide/b-cisco-nexus-9000-series-nx-os-programmability-guide-92x/b-cisco-nexus-9000-series-nx-os-programmability-guide-92x_chapter_010110.html

We are going to make an API call to a Cisco Nexus 9k device using the requests
library and parse out the returned output for the current NX-OS version.

The call format will be json-rpc with the command type being cli.

The remote device is an always-on lab device provided by Cisco DevNet:
Nexus 9000v Host: sbx-nxos-mgmt.cisco.com
NXAPI Ports: 443 (HTTPS)
Username: admin
Password: Admin_1234!

Note: due to the current setup, you can use the verify=False kwarg in your
requests post.
'''


HOST = 'sbx-nxos-mgmt.cisco.com'
PROTOCOL = 'https'
USERNAME = 'admin'
# Horrible but required in this Bite...:
PASSWORD = 'Admin_1234!'


import json
from typing import cast

import requests


def nxapi_show_version() -> str:
    url =  f'{PROTOCOL}://{HOST}/ins'
    switchuser = USERNAME
    switchpassword = PASSWORD

    http_headers = {'Content-Type': 'application/json-rpc'}
    payload = [{'jsonrpc': '2.0',
                'method': 'cli',
                'params': {'cmd': 'show version', 'version': 1},
                'id': 1}]
    # 1. use requests to post to the switch
    #
    # Instead of using data and encoding manually:
    # response = requests.post(url, data=json.dumps(payload), ...
    # Can use this and have library take care of:
    response = requests.post(url, json=payload, headers=http_headers,
                             auth=(switchuser, switchpassword), verify=False)

    # 2. retrieve and return the kickstart_ver_str from the response
    # example response json:
    # {'result': {'body': {'bios_cmpl_time': '05/17/2018',
    #                      'kick_tmstmp': '07/11/2018 00:01:44',
    #                      'kickstart_ver_str': '9.2(1)',
    #                      ...
    #                      }
    #             }
    # }
    if not response.ok:
        raise RuntimeError(f'Error: {response.status_code}:\n{response.text}')

    result = response.json()
    # print(json.dumps(result, indent=4))
    version = result['result']['body']['kickstart_ver_str']

    return cast(str, version)


if __name__ == '__main__':
    result = nxapi_show_version()
    print(result)
