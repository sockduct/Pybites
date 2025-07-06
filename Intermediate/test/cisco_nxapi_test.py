from pathlib import Path
import sys
from unittest.mock import patch, Mock

import requests

sys.path.append(str(Path(__file__).resolve().parent.parent))

from cisco_nxapi import nxapi_show_version


switch_output = dict(
    kern_uptm_secs=21,
    kick_file_name='bootflash:///nxos.9.2.1.bin.S2460',
    rr_service=None,
    module_id='Supervisor Module',
    kick_tmstmp='07/11/2018 00:01:44',
    bios_cmpl_time='05/17/2018',
    bootflash_size=20971520,
    kickstart_ver_str='9.2(1)',
    kick_cmpl_time='7/9/2018 9:00:00',
    chassis_id='Nexus9000 C9504 (4 Slot) Chassis',
    proc_board_id='SAL171211LX',
    memory=16077872,
    manufacturer='Cisco Systems, Inc.',
    kern_uptm_mins=26,
    bios_ver_str='05.31',
    cpu_name='Intel(R) Xeon(R) CPU D-1528 @ 1.90GHz',
    kern_uptm_hrs=2,
    rr_usecs=816550,
    rr_sys_ver='9.2(1)0',
    rr_reason='Reset Requested by CLI command reload',
    rr_ctime='Wed Jul 11 20:44:39 2018',
    header_str='Cisco Nexus Operating System (NX-OS) Software',
)


@patch.object(requests, 'post')
def test_get_version(mock_post):
    response = dict(result=dict(body=switch_output))
    mock_post.return_value = Mock(json=lambda: response)
    assert nxapi_show_version() == "9.2(1)"


@patch.object(requests, 'post')
def test_get_different_version(mock_post):
    switch_output['kickstart_ver_str'] = "7.2(0)"
    response = dict(result=dict(body=switch_output))
    mock_post.return_value = Mock(json=lambda: response)
    assert nxapi_show_version() == "7.2(0)"
