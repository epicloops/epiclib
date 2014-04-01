# -*- coding: utf-8 -*-
'''
epicdb command
'''
import logging

import epic.db
from epic.cmd import Cmd
from epic import version


log = logging.getLogger(__name__)


class EpicdbCmd(Cmd):

    module = epic.db
    parser = {
        'name': 'epicdb',
        'version': version.__version__,
        'desc': module.__doc__,
    }
    subparsers = {
        'create': {
            'help': module.create.__doc__.split('\n\n')[0],
            'func': module.create
        },
        'truncate': {
            'help': module.truncate.__doc__.split('\n\n')[0],
            'func': module.truncate
        },
        'drop': {
            'help': module.drop.__doc__.split('\n\n')[0],
            'func': module.drop
        },
    }
