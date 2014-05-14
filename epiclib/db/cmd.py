# -*- coding: utf-8 -*-
'''
epicdb command
'''
import logging

import epiclib
import epiclib.db
from epiclib.cmd import Cmd


log = logging.getLogger(__name__)


class EpicdbCmd(Cmd):

    module = epiclib.db
    parser = {
        'name': 'epicdb',
        'version': epiclib.__version__,
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
