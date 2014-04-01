# -*- coding: utf-8 -*-
'''
Persist items to db.
'''
from __future__ import unicode_literals

from scrapy import log
from scrapy.exceptions import DropItem


class DbPipelineDropItem(DropItem):

    pass


class DbPipeline(object):

    def __init__(self, crawler):
        self.settings = crawler.settings
        self.session = crawler.session

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)
        return ext

    def process_item(self, item, spider):

        self.session.add(item.instance())
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        else:
            log.msg(format='Persisted: Track - %(track_page_url)s',
                    level=log.DEBUG, spider=spider,
                    track_page_url=item['track_page_url'])

        return item
