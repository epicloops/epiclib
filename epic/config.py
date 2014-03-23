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
        'AWS_ACCESS_KEY_ID' : None,
        'AWS_SECRET_ACCESS_KEY' : None,
        'AWS_S3_BUCKET' : None,
        'SQLALCHEMY_DATABASE_URI' : None,


        # ECHONEST
        'ECHONEST_API_KEY' : None,
        'ECHONEST_SAMPLES' : [
            'sections',
            'bars',
            'beats',
            'tatums',
            'segments',
        ],
        'PROCESS_SAMPLES' : [
            'sections',
            'bars',
            'beats',
            # 'tatums',
            # 'segments',
        ],


        # CRAWLERA
        'CRAWLERA_ENABLED' : True,
        'CRAWLERA_URL' : 'http://proxy.crawlera.com:8010',
        'CRAWLERA_USER' : None,
        'CRAWLERA_PASS' : None,
        'CRAWLERA_DOWNLOAD_TIMEOUT' : 600,
        'CRAWLERA_MAXBANS' : 20,


        # SCRAPY
        'BOT_NAME' : 'epicbot',
        'SPIDER_MODULES' : ['epic.bot.spiders'],
        'NEWSPIDER_MODULE' : 'epic.bot.spiders',
        'LOG_LEVEL' : 'DEBUG',

        # optimized
        # http://support.scrapinghub.com/topic/187082-optimizing-scrapy-settings-for-crawlera/
        # This seemed to be crashing the xmlinfo soundclick page
        # 'CONCURRENT_REQUESTS' : 100,
        # 'CONCURRENT_REQUESTS_PER_DOMAIN' : 100,
        # 'AUTOTHROTTLE_ENABLED' : False,
        # 'DOWNLOAD_TIMEOUT' : 600,

        # delayed
        'DOWNLOAD_DELAY' : 2,
        'AUTOTHROTTLE_ENABLED' : True,

        'DOWNLOADER_MIDDLEWARES' : {
            'scrapylib.crawlera.CrawleraMiddleware': 600,
        },

        'ITEM_PIPELINES' : {
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
            # Export metadata to db
            'epic.bot.pipelines.db.DbPipeline': 700,
        },

        'EXTENSIONS' : {
            'epic.bot.extensions.DroppedItemsCsv': 300,
        },

        'PERSIST_DROPPED_ITEMS_ENABLED' : True,

        'CRAWLER_STATS_ENABLED' : True,

        # CLOSESPIDER_TIMEOUT :
        'CLOSESPIDER_ITEMCOUNT' : 1000,
        'CLOSESPIDER_PAGECOUNT' : 20000, # ~1000 tracks at $30 conservative
                                         # ~ $25 crawlera + ~ $2 scrapinghub
        'CLOSESPIDER_ERRORCOUNT' : 20,

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
