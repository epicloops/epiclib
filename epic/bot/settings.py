# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from epic.settings import *

#==============================================================================
# GENERAL
#==============================================================================
BOT_NAME = 'epicbot'
SPIDER_MODULES = ['epic.bot.spiders']
NEWSPIDER_MODULE = 'epic.bot.spiders'
LOG_LEVEL = 'DEBUG'


#==============================================================================
# OPTIMIZATION/DELAY
# http://support.scrapinghub.com/topic/187082-optimizing-scrapy-settings-for-crawlera/
#==============================================================================
# OPTIMIZED
# This seemed to be crashing the xmlinfo soundclick page
# CONCURRENT_REQUESTS = 100
# CONCURRENT_REQUESTS_PER_DOMAIN = 100
# AUTOTHROTTLE_ENABLED = False
# DOWNLOAD_TIMEOUT = 600

# DELAYED
DOWNLOAD_DELAY = 2
AUTOTHROTTLE_ENABLED = True


#==============================================================================
# MIDDLEWARES
#==============================================================================
DOWNLOADER_MIDDLEWARES = {
    'scrapylib.crawlera.CrawleraMiddleware': 600,
}

#==============================================================================
# PIPELINES
#==============================================================================
ITEM_PIPELINES = {
    # Add any additional post crawl data to every item returned from spiders
    'epic.bot.pipelines.post_crawl.PostCrawlPipeline': 200,
    # Drop dups based on crawl_key.
    'epic.bot.pipelines.filters.DuplicatesPipeline': 300,
    # Check for CC license and download flag
    'epic.bot.pipelines.filters.CCFilterPipeline': 400,
    # Download track data and store it in S3
    'epic.bot.pipelines.track.TrackPipeline': 500,
    # Run the track against the echonest api and gather data.
    'epic.bot.pipelines.echonest.EchonestPipeline': 600,
    # Export metadata to db
    'epic.bot.pipelines.db.DbPipeline': 700,
}

#==============================================================================
# EXTENSIONS
#==============================================================================
EXTENSIONS = {
    'epic.bot.extensions.DroppedItemsCsv': 300,
}

PERSIST_DROPPED_ITEMS_ENABLED = True

# CLOSESPIDER_TIMEOUT =
CLOSESPIDER_ITEMCOUNT = 1000
CLOSESPIDER_PAGECOUNT = 20000 # ~1000 tracks at $30 conservative
                              # ~ $25 crawlera + ~ $2 scrapinghub
CLOSESPIDER_ERRORCOUNT = 20
