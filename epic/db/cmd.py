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
    }
