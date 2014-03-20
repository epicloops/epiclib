'''
Settings.
'''
import sys
import os
import json
import logging


log = logging.getLogger(__name__)


def read_config():

    config = {
        'AWS_ACCESS_KEY_ID' : None,
        'AWS_SECRET_ACCESS_KEY' : None,
        'AWS_S3_BUCKET' : None,
        'SQLALCHEMY_DATABASE_URI' : None,
        'ECHONEST_API_KEY' : None,
        'ECHONEST_SAMPLES' : [
            'sections',
            'bars',
            'beats',
            'tatums',
            'segments',
        ],
        'SAMPLER_SAMPLES' : [
            'sections',
            'bars',
            'beats',
            # 'tatums',
            # 'segments',
        ],
        'CRAWLERA_ENABLED' : True,
        'CRAWLERA_URL' : 'http://proxy.crawlera.com:8010',
        'CRAWLERA_USER' : None,
        'CRAWLERA_PASS' : None,
        'CRAWLERA_DOWNLOAD_TIMEOUT' : 600,
        'CRAWLERA_MAXBANS' : 20,
    }

    config_file = os.path.join(os.path.expanduser('~'), '.epic', 'config')
    try:
        f = open(config_file)
    except IOError, e:
        log.error('Error opening epic config file. %s', e)
        return
    else:
        config.update(json.loads(f.read()))
        f.close()

        for k, v in config.items():
            setattr(sys.modules[__name__], k, v)

        return config
