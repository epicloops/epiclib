# -*- coding: utf-8 -*-
'''
Cli base and meta classes.
'''
import argparse
import logging

from epiclib.log import LEVEL_KEYS, init
from epiclib.config import read_config


log = logging.getLogger(__name__)


class CmdMeta(type):

    def __new__(mcs, name, bases, attrs):

        try:
            parser = attrs.pop('parser')
        except KeyError:
            parser = None

        try:
            subparsers = attrs.pop('subparsers')
        except KeyError:
            subparsers = None

        # instantiate after popping parsers
        instance = super(CmdMeta, mcs).__new__(mcs, name, bases, attrs)

        if parser:
            instance.parser = argparse.ArgumentParser(
                add_help=True, description=parser.get('desc', None),
                epilog='for subcommand help '
                       'run `{} SUBCOMMAND -h`'.format(parser['name'])
            )
            instance.parser.add_argument('-l', '--log-level',
                                    choices=LEVEL_KEYS,
                                    dest='log_level', help='Set log level.')
            instance.parser.add_argument('--log-file', dest='log_file',
                                    help='Set log file.')
            instance.parser.add_argument('--version', action='version',
                                    version=parser['version'],
                                    help='print version and exit.')

            for arg in parser.get('args', []):
                instance.parser.add_argument(*arg.pop('name_or_flags'), **arg)

            func = parser.get('func', None)
            if func:
                instance.parser.set_defaults(func=func)


        if subparsers:
            instance.subparsers = instance.parser.add_subparsers(
                                                title='available subcommands')

            for k, v in subparsers.items():
                subparser = instance.subparsers.add_parser(k, help=v['help'])
                for arg in v.get('args', []):
                    subparser.add_argument(*arg.pop('name_or_flags'), **arg)
                subparser.set_defaults(func=v['func'])


        return instance


class Cmd(object):

    __metaclass__ = CmdMeta

    @classmethod
    def run(cls):
        args = cls().parser.parse_args()

        # Omit parser values of None in order to default to config values
        # returned from read_config()
        args = {k: v for k, v in args.__dict__.items() if v is not None}

        config = read_config()
        config.update(args)

        init(config['log_level'], config['log_file'])

        try:
            args['func'](**config)
        except KeyboardInterrupt:
            raise SystemExit('\nExiting gracefully on Ctrl-c')
