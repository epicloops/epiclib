# -*- coding: utf-8 -*-
'''
Add additional data to crawled items.
'''
from __future__ import unicode_literals

import hashlib


class PostCrawlPipeline(object):

    def __init__(self, crawler):
        self.settings = crawler.settings
        self.stats = crawler.stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):

        item['crawl_id'] = self.stats.get_value('crawl_id')
        item['spider'] = spider.name
        item['spider_start'] = self.stats.get_value(
                                        'spider_start_{}'.format(spider.name))

        m = hashlib.md5()
        m.update(item.get('track_url', 'Not populated.'))
        m.update(str(item.get('download_flag', 'Not populated.')))
        m.update(item.get('license_url', 'Not populated.'))
        item['track_id'] = m.hexdigest().decode('utf-8')

        return item
