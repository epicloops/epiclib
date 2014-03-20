'''
Settings.
'''
import os
import json
import logging


log = logging.getLogger(__name__)


with open(os.path.join(os.path.expanduser('~'), '.epic', 'config')) as f:
    CONFIG = json.loads(f.read())

AWS_ACCESS_KEY_ID = CONFIG.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = CONFIG.get('AWS_SECRET_ACCESS_KEY', None)
AWS_S3_BUCKET = CONFIG.get('AWS_S3_BUCKET', None)

SQLALCHEMY_DATABASE_URI = CONFIG.get('SQLALCHEMY_DATABASE_URI', None)

ECHONEST_API_KEY = CONFIG.get('ECHONEST_API_KEY', None)
ECHONEST_SAMPLES = [
    'sections',
    'bars',
    'beats',
    'tatums',
    'segments',
]

SAMPLER_SAMPLES = [
    'sections',
    'bars',
    'beats',
    # 'tatums',
    # 'segments',
]

CRAWLERA_ENABLED = True
CRAWLERA_URL = 'http://proxy.crawlera.com:8010'
CRAWLERA_USER = CONFIG.get('CRAWLERA_USER', None)
CRAWLERA_PASS = CONFIG.get('CRAWLERA_PASS', None)
CRAWLERA_DOWNLOAD_TIMEOUT = 600
CRAWLERA_MAXBANS = 20
