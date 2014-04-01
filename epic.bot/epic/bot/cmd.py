# -*- coding: utf-8 -*-
'''
epicbot command
'''
import logging

import epic.bot
from epic.cmd import Cmd


log = logging.getLogger(__name__)


class EpicbotCmd(Cmd):

    module = epic.bot
    parser = {
        'name': 'epicbot',
        'version': module.__version__,
        'desc': module.__doc__,
    }
    subparsers = {
        'crawl': {
            'help': module.crawl.__doc__.split('\n\n')[0],
            'func': module.crawl,
            'args': [
                {
                    'name_or_flags': ['spider_name'],
                    'help': 'spider to run'
                },
                {
                    'dest': 'crawl_id',
                    'name_or_flags': ['-c', '--craw-id'],
                    'default': None,
                    'required': False,
                    'help': 'md5 to set as crawl_id'
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
        }
    }
