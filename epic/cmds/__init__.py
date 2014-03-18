'''
Base for cli commands.
'''
import argparse
import logging

from epic import __version__
from epic.log import LEVELS
from epic.log import init


log = logging.getLogger(__name__)


class CmdMeta(type):

    def __new__(mcs, name, bases, attrs):
        module = attrs.pop('module')
        subparsers = attrs.pop('subparsers')
        instance = super(CmdMeta, mcs).__new__(mcs, name, bases, attrs)

        instance.parser = argparse.ArgumentParser(
            add_help=True, description=module.__doc__,
            epilog='for subcommand help run `{} SUBCOMMAND -h`'.format(
                                                name.split('Cmd')[0].lower())
        )
        instance.parser.add_argument('-l', '--loglevel', default='info',
                                choices=LEVELS.keys(),
                                dest='loglevel', help='Set log level.')
        instance.parser.add_argument('--version', action='version',
                                version=__version__,
                                help='print version and exit.')
        instance.subparsers = instance.parser.add_subparsers(
                                                title='available subcommands')

        for k, v in subparsers.items():
            subparser = instance.subparsers.add_parser(k, help=v['help'])
            for arg in v.get('args', []):
                subparser.add_argument(*arg.pop('name_or_flags'), **arg)
            subparser.set_defaults(func=v['set_defaults']['func'])

        return instance


class Cmd(object):

    @classmethod
    def run(cls):
        args = cls().parser.parse_args()
        init(args.loglevel)
        try:
            args.func(**args.__dict__)
        except KeyboardInterrupt:
            raise SystemExit('\nExiting gracefully on Ctrl-c')
