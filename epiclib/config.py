# -*- coding: utf-8 -*-
'''
Load config file.
'''
import sys
import os
import json
import logging


log = logging.getLogger(__name__)


def read_config():

    epic_dir = os.path.join(os.path.expanduser('~'), '.epic')

    config = {

        # GENERAL
        'tmp_dir': os.path.join(epic_dir, 'tmp'),
        # 'config_file': os.path.join(epic_dir, 'config'),
        'config_file': '/etc/epic/config',
        'log_level': 'info',
        'log_file': os.path.join(epic_dir, 'epic.log'),

        # this list is used by the sampler to determine which samples to split.
        # tatums and segments have such a short duration they are not worth
        # splitting. additionally, because there are so many, loading them from
        # the db in the sampler and then calling mp3split in a subprocess can
        # cause memory issues. TODO: find a better way to handle this.
        'samples': [
            'sections',
            'bars',
            'beats',
            # 'tatums',
            # 'segments'
        ],

        # AWS
        'aws_access_key_id': None,
        'aws_secret_access_key': None,
        'aws_region': None,
        'sqlalchemy_database_uri': None,
        'aws_s3_bucket': None,


        # ECHONEST
        'echonest_api_key': None,


        # CRAWLERA
        'crawlera_enabled': True,
        'crawlera_url': 'http://proxy.crawlera.com:8010',
        'crawlera_user': None,
        'crawlera_pass': None,
        'crawlera_download_timeout': 600,
        'crawlera_maxbans': 20,

    }

    try:
        f = open(config['config_file'])
    except IOError, e:
        log.error('Error opening epic config file. %s', e)
        sys.exit()
    else:
        config.update({k.lower(): v for k, v in json.loads(f.read()).items()})
        f.close()
        return config
