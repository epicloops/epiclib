# -*- coding: utf-8 -*-
'''
epicpkg command
'''
import logging

import epic.pkg
from epic.cmd import Cmd, CmdMeta


log = logging.getLogger(__name__)


class EpicpkgCmd(Cmd):

    __metaclass__ = CmdMeta

    module = epic.pkg
    subparsers = {
        'dl': {
            'help': module.download.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'crawl_start',
                    'name_or_flags': ['-c', '--crawl-start'],
                    'default': None,
                    'required': True,
                    'help': 'start timestamp from epicbot'
                },
                {
                    'dest': 'spider',
                    'name_or_flags': ['-s', '--spider'],
                    'default': None,
                    'required': True,
                    'help': 'name of spider'
                },
                {
                    'dest': 'sampler_start',
                    'name_or_flags': ['-C', '--sampler-start'],
                    'default': None,
                    'required': True,
                    'help': 'start timestamp from epicsampler'
                },
                {
                    'dest': 'qry',
                    'name_or_flags': ['-q', '--qry'],
                    'default': None,
                    'required': True,
                    'help': 'qry used to determine best tracks to download'
                },
                {
                    'dest': 'limit',
                    'name_or_flags': ['-l', '--limit'],
                    'type': int,
                    'default': 50,
                    'required': True,
                    'help': 'number of tracks to download'
                },
                {
                    'dest': 'dl_samples',
                    'name_or_flags': ['-x', '--dl-samples'],
                    'action': 'store_false',
                    'help': 'do not download samples'
                },
            ],
            'set_defaults': {
                'func': module.download
            },
        },
        'pkg': {
            'help': module.pkg.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'crawl_start',
                    'name_or_flags': ['-c', '--crawl-start'],
                    'default': None,
                    'required': True,
                    'help': 'start timestamp from epicbot'
                },
                {
                    'dest': 'spider',
                    'name_or_flags': ['-s', '--spider'],
                    'default': None,
                    'required': True,
                    'help': 'name of spider'
                },
                {
                    'dest': 'sampler_start',
                    'name_or_flags': ['-C', '--sampler-start'],
                    'default': None,
                    'required': True,
                    'help': 'start timestamp from epicsampler'
                },
                {
                    'dest': 'qry',
                    'name_or_flags': ['-q', '--qry'],
                    'default': None,
                    'required': True,
                    'help': 'qry used to determine best tracks to download'
                },
                {
                    'dest': 'limit',
                    'name_or_flags': ['-l', '--limit'],
                    'type': int,
                    'default': 50,
                    'required': True,
                    'help': 'number of tracks to download'
                },
                {
                    'dest': 'zip_name',
                    'name_or_flags': ['-z', '--zip_name'],
                    'default': None,
                    'required': True,
                    'help': 'name of zip file'
                },
                {
                    'dest': 'clean',
                    'name_or_flags': ['-x', '--dont-clean'],
                    'action': 'store_false',
                    'help': 'do not remove pkg dir'
                },
            ],
            'set_defaults': {
                'func': module.pkg
            },
        },
        'build': {
            'help': module.build.__doc__.split('\n\n')[0],
            'set_defaults': {
                'func': module.build
            },
        },
        'zip': {
            'help': module.zip_.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'zip_name',
                    'name_or_flags': ['-z', '--zip_name'],
                    'default': None,
                    'required': True,
                    'help': 'name of zip file'
                },
            ],
            'set_defaults': {
                'func': module.zip_
            },
        },
        'ul': {
            'help': module.upload.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'zip_name',
                    'name_or_flags': ['-z', '--zip_name'],
                    'default': None,
                    'required': True,
                    'help': 'name of zip file'
                },
                {
                    'dest': 'clean',
                    'name_or_flags': ['-x', '--dont-clean'],
                    'action': 'store_false',
                    'help': 'do not remove pkg dir'
                },
            ],
            'set_defaults': {
                'func': module.upload
            },
        },
    }
