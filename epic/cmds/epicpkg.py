'''
epicpkg command
'''
import epic.pkg
from epic.cmds import Cmd, CmdMeta


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
