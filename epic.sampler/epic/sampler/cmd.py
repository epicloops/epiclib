# -*- coding: utf-8 -*-
'''
epicsampler command
'''
import logging

import epic.sampler
from epic.cmd import Cmd


log = logging.getLogger(__name__)


class EpicsamplerCmd(Cmd):

    module = epic.sampler
    parser = {
        'name': 'epicsampler',
        'version': module.__version__,
        'desc': module.__doc__,
        'func': module.main
    }
