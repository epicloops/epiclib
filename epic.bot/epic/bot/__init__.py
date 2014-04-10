# -*- coding: utf-8 -*-
'''
Web crawler. Includes site-specific spiders that scrape Creative Commons
tracks and run them against the echonest api.
'''
import logging

from twisted.python.log import PythonLoggingObserver

import scrapy
from scrapy import log
from scrapy.settings import CrawlerSettings, overridden_settings
from scrapy.crawler import CrawlerProcess

import epic.config


__version__ = '0.1.0'


def crawl(session, crawl_id, spider_name, max_tracks, start_page, max_pages,
          genre, *args, **kwargs):
    '''Run epicbot web crawler.'''
    settings = CrawlerSettings(epic.config)
    crawler_process = CrawlerProcess(settings)
    crawler = crawler_process.create_crawler()
    crawler.session = session
    spider_kwargs = {
        'crawl_id': crawl_id,
        'max_tracks': max_tracks,
        'start_page': start_page,
        'max_pages': max_pages,
        'genre': genre,
    }
    spider = crawler.spiders.create(spider_name, **spider_kwargs)
    crawler.crawl(spider)

    # direct scrapy.log.msg to standard python logging module
    observer = PythonLoggingObserver(loggerName=__name__)
    observer.start()
    log.msg('Scrapy {} starting (bot: {})'.format(scrapy.__version__,
                                                  settings['BOT_NAME']))

    log.msg('Optional features available: {}'.format(
                                    ', '.join(scrapy.optional_features)))

    d = dict(overridden_settings(settings))
    log.msg(format='Overridden settings: %(settings)r', settings=d)

    crawler_process.start()
