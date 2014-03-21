# -*- coding: utf-8 -*-
'''
epicqry command
'''
import logging

import epic.qry
from epic.cmd import Cmd, CmdMeta


log = logging.getLogger(__name__)


class EpicqryCmd(Cmd):

    __metaclass__ = CmdMeta

    module = epic.qry
    subparsers = {
        'pro': {
            'help': module.pro.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'crawl_start',
                    'name_or_flags': ['-c', '--crawl-start'],
                    'default': None,
                    'required': True,
                    'help': 'start timestamp from epicbot'
                },
                {
                    'dest': 'limit',
                    'name_or_flags': ['-l', '--limit'],
                    'type': int,
                    'default': 50,
                    'required': True,
                    'help': 'number of tracks to return'
                },
            ],
            'set_defaults': {
                'func': module.pro
            }
        },
        'lite': {
            'help': module.lite.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'crawl_start',
                    'name_or_flags': ['-c', '--crawl-start'],
                    'default': None,
                    'required': True,
                    'help': 'start timestamp from epicbot'
                },
                {
                    'dest': 'limit',
                    'name_or_flags': ['-l', '--limit'],
                    'type': int,
                    'default': 50,
                    'required': True,
                    'help': 'number of tracks to return'
                },
            ],
            'set_defaults': {
                'func': module.lite
            }
        }
    }
