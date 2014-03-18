'''
A tool to crawl, download, split, and package Creative Commons audio files from
the web.
'''
import argparse
import logging

import epic.models
import epic.bot
import epic.sampler
import epic.qry
import epic.pkg
from epic.log import LEVELS
from epic.log import init


__author__ = 'A.J. Welch'
__email__ = 'awelch0100@gmail.com'
__version__ = '0.1.0'


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


class EpicsamplerCmd(Cmd):

    __metaclass__ = CmdMeta

    module = epic.sampler
    subparsers = {
        'up': {
            'help': module.up.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'profile',
                    'name_or_flags': ['-p', '--profile'],
                    'default': None,
                    'required': False,
                    'help': 'salt cloud profile'
                },
                {
                    'dest': 'servers',
                    'name_or_flags': ['-s', '--servers'],
                    'type': int,
                    'default': 1,
                    'required': False,
                    'help': 'number of servers to spin up'
                },
                {
                    'dest': 'display_ssh_output',
                    'name_or_flags': ['-d', '--display-ssh'],
                    'type': bool,
                    'default': False,
                    'required': False,
                    'help': 'flag to display ssh output'
                },
            ],
            'set_defaults': {
                'func': module.up
            }
        },
        'provision': {
            'help': module.provision.__doc__.split('\n\n')[0],
            'set_defaults': {
                'func': module.provision
            }
        },
        'ping': {
            'help': module.ping.__doc__.split('\n\n')[0],
            'set_defaults': {
                'func': module.ping
            }
        },
        'run': {
            'help': module.run.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'crawl_start',
                    'name_or_flags': ['-c', '--crawl-start'],
                    'default': None,
                    'required': True,
                    'help': 'start timestamp from epicbot'
                },
                {
                    'dest': 'spider',
                    'name_or_flags': ['-s', '--spider'],
                    'default': None,
                    'required': True,
                    'help': 'name of spider'
                },
                {
                    'dest': 'offset',
                    'name_or_flags': ['-o', '--offset'],
                    'type': int,
                    'default': 0,
                    'required': False,
                    'help': 'track offset to start at'
                },
                {
                    'dest': 'qty',
                    'name_or_flags': ['-q', '--qty'],
                    'type': int,
                    'default': -1,
                    'required': False,
                    'help': 'number of tracks to sample'
                },
            ],
            'set_defaults': {
                'func': module.run
            }
        },
        'monitor': {
            'help': module.monitor.__doc__.split('\n\n')[0],
            'set_defaults': {
                'func': module.monitor
            }
        },
        'kill': {
            'help': module.kill.__doc__.split('\n\n')[0],
            'set_defaults': {
                'func': module.kill
            }
        },
        'destroy': {
            'help': module.destroy.__doc__.split('\n\n')[0],
            'set_defaults': {
                'func': module.destroy
            }
        },
    }


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


class EpicpkgCmd(Cmd):

    __metaclass__ = CmdMeta

    module = epic.pkg
    subparsers = {
        'dl': {
            'help': module.download.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'filename',
                    'name_or_flags': ['-f', '--file'],
                    'default': None,
                    'required': True,
                    'help': 'filename relative to cwd containing crawl keys to'
                            ' download'
                },
                {
                    'dest': 'bot_bucket',
                    'name_or_flags': ['-b', '--bot-bucket'],
                    'default': None,
                    'required': True,
                    'help': 'name of s3 bucket where epicbot results are'
                            ' stored'
                },
                {
                    'dest': 'sampler_bucket',
                    'name_or_flags': ['-B', '--sampler-bucket'],
                    'default': None,
                    'required': True,
                    'help': 'name of s3 bucket where epicsampler results are '
                            'stored'
                },
                {
                    'dest': 'spider',
                    'name_or_flags': ['-s', '--spider'],
                    'default': None,
                    'required': True,
                    'help': 'name of spider'
                },
                {
                    'dest': 'crawl_start',
                    'name_or_flags': ['-c', '--crawl-start'],
                    'default': None,
                    'required': True,
                    'help': 'start timestamp from epicbot'
                },
                {
                    'dest': 'sampler_start',
                    'name_or_flags': ['-C', '--sampler-start'],
                    'default': None,
                    'required': True,
                    'help': 'start timestamp from epicsampler'
                },
                {
                    'dest': 'dl_samples',
                    'name_or_flags': ['-x', '--dl-samples'],
                    'action': 'store_false',
                    'help': 'do not download samples'
                },
            ],
            'set_defaults': {
                'func': module.download
            },
        },
        'pkg': {
            'help': module.pkg.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'dl_dir',
                    'name_or_flags': ['-d', '--dl-dir'],
                    'default': None,
                    'required': True,
                    'help': 'directory containing track and samples to package'
                },
                {
                    'dest': 'pkg_bucket',
                    'name_or_flags': ['-b', '--pkg-bucket'],
                    'default': None,
                    'required': True,
                    'help': 'name of s3 bucket where epicpkg results will be '
                            'stored'
                },
                {
                    'dest': 'crawl_start',
                    'name_or_flags': ['-c', '--crawl-start'],
                    'default': None,
                    'required': True,
                    'help': 'start timestamp from epicbot'
                },
                {
                    'dest': 'clean',
                    'name_or_flags': ['-x', '--dont-clean'],
                    'action': 'store_false',
                    'help': 'do not remove pkg dir'
                },
            ],
            'set_defaults': {
                'func': module.pkg
            },
        },
        'build': {
            'help': module.build.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'dl_dir',
                    'name_or_flags': ['-d', '--dl-dir'],
                    'default': None,
                    'required': True,
                    'help': 'directory containing track and samples to package'
                },
                {
                    'dest': 'crawl_start',
                    'name_or_flags': ['-c', '--crawl-start'],
                    'default': None,
                    'required': True,
                    'help': 'start timestamp from epicbot'
                },
            ],
            'set_defaults': {
                'func': module.build
            },
        },
        'zip': {
            'help': module.zip_.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'pkg_dir',
                    'name_or_flags': ['-d', '--pkg-dir'],
                    'default': '',
                    'required': True,
                    'help': 'directory containing files to be zipped'
                },
            ],
            'set_defaults': {
                'func': module.zip_
            },
        },
        'ul': {
            'help': module.upload.__doc__.split('\n\n')[0],
            'args': [
                {
                    'dest': 'filename',
                    'name_or_flags': ['-f', '--file'],
                    'default': None,

                    'required': True,
                    'help': 'zip file to upload'
                },
                {
                    'dest': 'pkg_bucket',
                    'name_or_flags': ['-b', '--pkg-bucket'],
                    'default': None,
                    'required': True,
                    'help': 'name of s3 bucket where zip file will be uploaded'
                },
                {
                    'dest': 'clean',
                    'name_or_flags': ['-x', '--dont-clean'],
                    'action': 'store_false',
                    'help': 'do not remove pkg dir'
                },
            ],
            'set_defaults': {
                'func': module.upload
            },
        },
    }
