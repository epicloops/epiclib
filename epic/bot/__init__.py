'''
Crawls the web searching for Creative Commons tracks and runs them against the
echonest api.
'''
import logging

from scrapy.settings import CrawlerSettings
from scrapy.crawler import CrawlerProcess

import epic.config


log = logging.getLogger(__name__)


def crawl(spider_name, max_tracks, start_page, max_pages, genre, *args,
          **kwargs):
    '''Run epicbot web crawler.'''
    settings = CrawlerSettings(epic.config)
    crawler_process = CrawlerProcess(settings)
    crawler = crawler_process.create_crawler()
    spider_kwargs = {
        'max_tracks': max_tracks,
        'start_page': start_page,
        'max_pages': max_pages,
        'genre': genre,
    }
    spider = crawler.spiders.create(spider_name, **spider_kwargs)
    crawler.crawl(spider)
    crawler_process.start()
