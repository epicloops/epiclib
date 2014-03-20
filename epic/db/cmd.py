'''
epicdb command
'''
import logging

import epic.db
from epic.cmd import Cmd, CmdMeta


log = logging.getLogger(__name__)


class EpicdbCmd(Cmd):

    __metaclass__ = CmdMeta

    module = epic.db
    subparsers = {
        'up': {
            'help': module.up.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'snapshot',
                    'name_or_flags': ['-s', '--snapshot'],
                    'default': None,
                    'required': True,
                    'help': 'Snapshot to restore from.'
                },
            ],
            'set_defaults': {
                'func': module.up
            }
        },
        'create': {
            'help': module.create.__doc__.split('\n\n')[0],
            'set_defaults': {
                'func': module.create
            }
        },
        'truncate': {
            'help': module.truncate.__doc__.split('\n\n')[0],
            'set_defaults': {
                'func': module.truncate
            }
        },
        'drop': {
            'help': module.drop.__doc__.split('\n\n')[0],
            'set_defaults': {
                'func': module.drop
            }
        },
        'destroy': {
            'help': module.destroy.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'skip_snapshot',
                    'name_or_flags': ['-s', '--skip-snapshot'],
                    'action': 'store_true',
                    'help': 'skip final snapshot'
                },
            ],
            'set_defaults': {
                'func': module.destroy
            }
        }
    }
