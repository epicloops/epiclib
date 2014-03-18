'''
epicqry command
'''
import epic.qry
from epic.cmds import Cmd, CmdMeta


class EpicqryCmd(Cmd):

    __metaclass__ = CmdMeta

    module = epic.qry
    subparsers = {
        'avg_confidence': {
            'help': module.avg_confidence.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'name',
                    'name_or_flags': ['-n', '--name'],
                    'default': None,
                    'required': True,
                    'help': 'name of attribute whose confidence to rank on'
                },
            ],
            'set_defaults': {
                'func': module.avg_confidence
            }
        }
    }
