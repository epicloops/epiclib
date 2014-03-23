# -*- coding: utf-8 -*-
'''
Scrapy extensions.
'''
from __future__ import unicode_literals

from twisted.internet import threads

from scrapy import log
from scrapy import signals
from scrapy.exceptions import NotConfigured

from epic.db import session_maker
from epic.db.models import Dropped


class DroppedItemsCsv(object):
    '''Writes dropped items to db.'''

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.settings = crawler.settings
        self.Session = None

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('PERSIST_DROPPED_ITEMS_ENABLED'):
            raise NotConfigured

        ext = cls(crawler)

        crawler.signals.connect(ext.spider_opened, signals.spider_opened)
        crawler.signals.connect(ext.item_dropped, signals.item_dropped)

        return ext

    def spider_opened(self, spider):
        self.Session = session_maker()

    def item_dropped(self, item, spider, exception):

        def _persist_item(item):
            item['dropped_item_exception'] = str(exception)

            item_record = dict([(k, v) for k, v in item.items() if k in Dropped.__table__.columns])

            session = self.Session()
            try:
                session.add(Dropped(**item_record))
            except:
                session.rollback()
                raise
            else:
                session.commit()
                log.msg(format='Persisted: Dropped - %(track_page_url)s',
                        level=log.DEBUG, spider=spider,
                        track_page_url=item_record['track_page_url'])
            finally:
                session.close()
            return item

        return threads.deferToThread(_persist_item, item)


class CrawlerStats(object):
    '''Writes dropped items to db.'''

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.settings = crawler.settings
        self.stats.set_value('start_time_str', '{:%Y-%m-%dT%H-%M-%S}'.format(
                                        self.stats.get_value('start_time')))

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('CRAWLER_STATS_ENABLED'):
            raise NotConfigured

        return cls(crawler)
