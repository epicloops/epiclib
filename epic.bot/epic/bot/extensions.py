# -*- coding: utf-8 -*-
'''
Scrapy extensions.
'''
from __future__ import unicode_literals

from scrapy import log
from scrapy import signals


class PersistDroppedItems(object):
    '''Writes dropped items to db.'''

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.settings = crawler.settings
        self.session = crawler.session

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)
        crawler.signals.connect(ext.item_dropped, signals.item_dropped)
        return ext

    def item_dropped(self, item, spider, exception):

        item['dropped_item_exception'] = str(exception)

        self.session.add(item.instance(dropped=True))
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        else:
            log.msg(format='Persisted: Dropped - %(track_page_url)s',
                    level=log.DEBUG, spider=spider,
                    track_page_url=item['track_page_url'])

        return item


class ExtStats(object):
    '''Add extended stats to crawler object.'''

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.settings = crawler.settings

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)
        crawler.signals.connect(ext.spider_opened, signals.spider_opened)
        return ext

    def spider_opened(self, spider):
        self.stats.set_value('spider_start_{}'.format(spider.name),
                             self.stats.get_value('start_time'))
        self.stats.set_value('crawl_id', spider.opts.crawl_id)
