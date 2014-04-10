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

    config = {

        # GENERAL
        'TMP_DIR': os.path.join(os.path.expanduser('~'), '.epic', 'tmp'),
        'CONFIG_FILE': os.path.join(os.path.expanduser('~'),
                                    '.epic', 'config'),
        'LOG_FILE': os.path.join(os.path.expanduser('~'), '.epic', 'log.log'),

        # this list is used by the sampler to determine which samples to split.
        # tatums and segments have such a short duration they are not worth
        # splitting. additionally, because there are so many, loading them from
        # the db in the sampler and then calling mp3split in a subprocess can
        # cause memory issues. TODO: find a better way to handle this.
        'SAMPLES': [
            'sections',
            'bars',
            'beats',
            # 'tatums',
            # 'segments'
        ],

        # AWS
        'AWS_ACCESS_KEY_ID': None,
        'AWS_SECRET_ACCESS_KEY': None,
        'AWS_REGION': None,
        'SQLALCHEMY_DATABASE_URI': None,
        'AWS_S3_BUCKET': None,


        # ECHONEST
        'ECHONEST_API_KEY': None,


        # CRAWLERA
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_URL': 'http://proxy.crawlera.com:8010',
        'CRAWLERA_USER': None,
        'CRAWLERA_PASS': None,
        'CRAWLERA_DOWNLOAD_TIMEOUT': 600,
        'CRAWLERA_MAXBANS': 20,


        # SCRAPY
        'BOT_NAME': 'epicbot',
        'SPIDER_MODULES': ['epic.bot.spiders'],
        # don't use scrapy.log.ScrapyFileLogObserver instead we use
        # twisted.python.log.PythonLoggingObserver in epic.bot.__init__.py
        # to redirect log events toPython's standard logging module
        'LOG_ENABLED': False,
        'LOG_LEVEL': 'DEBUG',

        # optimized
        # http://support.scrapinghub.com/topic/187082-optimizing-scrapy-settings-for-crawlera/
        # This seemed to be crashing the xmlinfo soundclick page
        # 'CONCURRENT_REQUESTS': 100,
        # 'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
        # 'AUTOTHROTTLE_ENABLED': False,
        # 'DOWNLOAD_TIMEOUT': 600,

        # delayed
        'DOWNLOAD_DELAY': 5, # echonest api limit is 20/min.
                             # 3 secs even doesn't fix the issue, most likely
                             # because our api calls are deffered to twisted
                             # threads so their frequency isn't directly
                             # correlated to this delay. TODO: find better fix
        'AUTOTHROTTLE_ENABLED': True,

        'DOWNLOADER_MIDDLEWARES': {
            'scrapylib.crawlera.CrawleraMiddleware': 600,
        },

        'ITEM_PIPELINES': {
            # Add any additional post crawl data to every item returned from spiders
            'epic.bot.pipelines.post_crawl.PostCrawlPipeline': 200,
            # Drop dups based on track_id.
            'epic.bot.pipelines.filters.DuplicatesPipeline': 300,
            # Check for CC license and download flag
            'epic.bot.pipelines.filters.CCFilterPipeline': 400,
            # Download track data and store it in S3
            'epic.bot.pipelines.track.TrackPipeline': 500,
            # Run the track against the echonest api and gather data.
            'epic.bot.pipelines.echonest.EchonestPipeline': 600,
            # Persist item to db
            'epic.bot.pipelines.db.DbPipeline': 700,
            # Write item to queue to be picked up by samplers
            'epic.bot.pipelines.queue.QueuePipeline': 800,
        },

        'EXTENSIONS': {
            'epic.bot.extensions.ExtStats': 200,
            'epic.bot.extensions.PersistDroppedItems': 300,
        },

        # CLOSESPIDER_TIMEOUT:
        'CLOSESPIDER_ITEMCOUNT': 1000,
        'CLOSESPIDER_PAGECOUNT': 20000, # ~1000 tracks at $30 conservative
                                        # ~ $25 crawlera + ~ $2 scrapinghub
        'CLOSESPIDER_ERRORCOUNT': 20,

    }

    try:
        f = open(config['CONFIG_FILE'])
    except IOError, e:
        log.error('Error opening epic config file. %s', e)
        return
    else:
        config.update(json.loads(f.read()))
        f.close()

        for k, v in config.items():
            setattr(sys.modules[__name__], k, v)

        return config
