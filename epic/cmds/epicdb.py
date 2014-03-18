'''
epicdb command
'''
import epic.models
from epic.cmds import Cmd, CmdMeta

class EpicdbCmd(Cmd):

    __metaclass__ = CmdMeta

    module = epic.models
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
        }
    }
