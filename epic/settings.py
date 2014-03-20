'''
Settings.
'''
import os
import logging


log = logging.getLogger(__name__)


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
S3_BUCKET = os.environ.get('EPIC_S3_BUCKET')

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

ECHONEST_API_KEY = os.environ.get('ECHONEST_API_KEY')
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
CRAWLERA_USER = os.environ.get('CRAWLERA_USER')
CRAWLERA_PASS = os.environ.get('CRAWLERA_PASS')
CRAWLERA_DOWNLOAD_TIMEOUT = 600
CRAWLERA_MAXBANS = 20
