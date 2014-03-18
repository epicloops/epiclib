'''
epicsampler command
'''
import epic.sampler
from epic.cmds import Cmd, CmdMeta


class EpicsamplerCmd(Cmd):

    __metaclass__ = CmdMeta

    module = epic.sampler
    subparsers = {
        'up': {
            'help': module.up.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'profile',
                    'name_or_flags': ['-p', '--profile'],
                    'default': None,
                    'required': False,
                    'help': 'salt cloud profile'
                },
                {
                    'dest': 'servers',
                    'name_or_flags': ['-s', '--servers'],
                    'type': int,
                    'default': 1,
                    'required': False,
                    'help': 'number of servers to spin up'
                },
                {
                    'dest': 'display_ssh_output',
                    'name_or_flags': ['-d', '--display-ssh'],
                    'type': bool,
                    'default': False,
                    'required': False,
                    'help': 'flag to display ssh output'
                },
            ],
            'set_defaults': {
                'func': module.up
            }
        },
        'provision': {
            'help': module.provision.__doc__.split('\n\n')[0],
            'set_defaults': {
                'func': module.provision
            }
        },
        'ping': {
            'help': module.ping.__doc__.split('\n\n')[0],
            'set_defaults': {
                'func': module.ping
            }
        },
        'run': {
            'help': module.run.__doc__.split('\n\n')[0],
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
                    'dest': 'offset',
                    'name_or_flags': ['-o', '--offset'],
                    'type': int,
                    'default': 0,
                    'required': False,
                    'help': 'track offset to start at'
                },
                {
                    'dest': 'qty',
                    'name_or_flags': ['-q', '--qty'],
                    'type': int,
                    'default': -1,
                    'required': False,
                    'help': 'number of tracks to sample'
                },
            ],
            'set_defaults': {
                'func': module.run
            }
        },
        'monitor': {
            'help': module.monitor.__doc__.split('\n\n')[0],
            'set_defaults': {
                'func': module.monitor
            }
        },
        'kill': {
            'help': module.kill.__doc__.split('\n\n')[0],
            'set_defaults': {
                'func': module.kill
            }
        },
        'destroy': {
            'help': module.destroy.__doc__.split('\n\n')[0],
            'set_defaults': {
                'func': module.destroy
            }
        },
    }
