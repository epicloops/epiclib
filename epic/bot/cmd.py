# -*- coding: utf-8 -*-
'''
epicbot command
'''
import logging

import epic.bot
from epic.cmd import Cmd, CmdMeta


log = logging.getLogger(__name__)


class EpicbotCmd(Cmd):

    __metaclass__ = CmdMeta

    module = epic.bot
    subparsers = {
        'crawl': {
            'help': module.crawl.__doc__.split('\n\n')[0],
            'args': [
                {
                    'name_or_flags': ['spider_name'],
                    'help': 'spider to run'
                },
                {
                    'dest': 'max_tracks',
                    'name_or_flags': ['-t', '--max-tracks'],
                    'type': int,
                    'default': None,
                    'required': False,
                    'help': 'max number of tracks to crawl per page'
                },
                {
                    'dest': 'start_page',
                    'name_or_flags': ['-s', '--start-page'],
                    'type': int,
                    'default': 1,
                    'required': False,
                    'help': 'page number to start crawling at'
                },
                {
                    'dest': 'max_pages',
                    'name_or_flags': ['-p', '--max-pages'],
                    'type': int,
                    'default': None,
                    'required': False,
                    'help': 'max number of pages to crawl per genre'
                },
                {
                    'dest': 'genre',
                    'name_or_flags': ['-g', '--genre'],
                    'default': 'prod',
                    'required': False,
                    'help': 'genre to crawl'
                },
            ],
            'set_defaults': {
                'func': module.crawl
            }
        }
    }
