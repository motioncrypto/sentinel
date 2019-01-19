import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from motiond import MotionDaemon
from motion_config import MotionConfig


def test_motiond():
    config_text = MotionConfig.slurp_config_file(config.motion_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000001e9dc60dd2618e91f7b9014134922c374496b61c1a272519b1c39979d78'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c'

    creds = MotionConfig.get_rpc_creds(config_text, network)
    motiond = MotionDaemon(**creds)
    assert motiond.rpc_command is not None

    assert hasattr(motiond, 'rpc_connection')

    # Motion testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = motiond.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert motiond.rpc_command('getblockhash', 0) == genesis_hash
