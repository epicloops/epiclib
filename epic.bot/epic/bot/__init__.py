# -*- coding: utf-8 -*-
'''
Web crawler. Includes site-specific spiders that scrape Creative Commons
tracks and run them against the echonest api.
'''
import logging

from scrapy.settings import CrawlerSettings
from scrapy.crawler import CrawlerProcess

import epic.config
from epic.db import session_scope


log = logging.getLogger(__name__)


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
    crawler_process.start()
